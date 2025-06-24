import json
import os
from unittest.mock import patch
from datetime import datetime
import pytest


from lambdas.shopping_list.add_item.add_item import  lambda_handler
import lambdas.shopping_list.add_item.add_item as add_item_module

TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]

@pytest.fixture(scope="function")
def mocked_add_item_table(dynamodb_resource): 

    table_mock = dynamodb_resource.Table(TABLE_NAME)

    with patch.object(add_item_module, 'table', new=table_mock):
        yield table_mock 


def test_lambda_handler_success(mock_event, mocked_add_item_table):
    events = [mock_event({"nome": "Tarefa de Teste"}), mock_event({"nome": "Tarefa de Teste", "data": "2024-12-31", "tipo_tarefa": "Item de Compra"})]
    
    context = {}
    
    for event in events:
        event_body = json.loads(event["body"])
        result = lambda_handler(event, context)
        body = json.loads(result["body"])
        assert result["statusCode"] == 200
        
        data = datetime.strptime(event_body["data"], "%Y-%m-%d") if "data" in event_body else datetime.today()
        
        expected_pk = f"LIST#{data.strftime('%Y%m%d')}"
        
        # Verifica o item que foi retornado no corpo da resposta
        item = body["item"]
        
        for key, value in event_body.items():
            if key == "data":
                # Verifica se a data está no formato correto
                assert item[key] == datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d, %H:%M:%S")
            else:
                assert value == item[key], f"Valor de {key} não corresponde: {value} != {item[key]}"
            
        assert item["PK"] == expected_pk
        assert item["SK"].startswith("ITEM#") 
        assert item["status"] == "TODO"
            
        
        saved_item = mocked_add_item_table.get_item(Key={"PK": item["PK"], "SK": item["SK"]}).get("Item")
        
        assert saved_item is not None
        assert saved_item["nome"] == event_body["nome"]
    
  
def test_lambda_handler_missing_fields(mock_event):
    event = mock_event({"data": "2024-12-31"})
    context = {}
    
    result = lambda_handler(event, context)
    
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert body["message"] == "nome é obrigatório"
    

def test_lambda_handler_unauthorized(mock_event):
    event = mock_event(body={"nome": "Tarefa de Teste", "data": "2024-12-31"}, user_id="")
    
    context = {}
    
    result = lambda_handler(event, context)
    
    assert result["statusCode"] == 401
    body = json.loads(result["body"])
    assert body["message"] == "Unauthorized"
    

def test_lambda_handler_dynamodb_client_error(mocked_add_item_table, mock_event):
    event = mock_event({"nome": "Tarefa de Teste", "data": "2024-12-31"})
    context = {}
    with patch.object(mocked_add_item_table, "put_item") as mock_put_item:
        from botocore.exceptions import ClientError
        mock_put_item.side_effect = ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Mocked ClientError"}},
            "PutItem",
        )
        result = lambda_handler(event, context)
        assert result["statusCode"] == 500
        body = json.loads(result["body"])
        assert "Erro no servidor:" in body["message"]


def test_lambda_handler_generic_exception(mocked_add_item_table, mock_event):
    event = mock_event({"nome": "Tarefa de Teste", "data": "2024-12-31"})
    context = {}
    with patch.object(mocked_add_item_table, "put_item") as mock_put_item:
        mock_put_item.side_effect = Exception("Erro genérico mockado")
        result = lambda_handler(event, context)
        assert result["statusCode"] == 500
        body = json.loads(result["body"])
        assert "Erro interno:" in body["message"]



