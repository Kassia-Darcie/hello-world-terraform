import json
from unittest.mock import patch
from datetime import date
import pytest
from moto import mock_aws

from lambdas.shopping_list.add_item.add_item import lambda_handler, generate_list_id, response
import lambdas.shopping_list.add_item.add_item as add_item_module


@pytest.fixture(scope="function")
def mocked_add_item_table(aws_credentials, dynamodb_resource_and_name): 
    """
    Esta fixture ativa o moto, cria a tabela e mocka a variável global 'table'
    no módulo add_item.py para apontar para a tabela mockada.
    """
    dynamodb_resource, table_name = dynamodb_resource_and_name 
    
    with mock_aws(): 
        table_mock = dynamodb_resource.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table_mock.wait_until_exists()

        with patch.object(add_item_module, 'table', new=table_mock):
            yield table_mock 


def test_lambda_handler_success(mocked_add_item_table):
    event = {"nome": "Tarefa de Teste", "data": "2024-12-31"}
    context = {}
    result = lambda_handler(event, context)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert "item" in body
    assert body["item"]["nome"] == "Tarefa de Teste"
    item_from_db = mocked_add_item_table.get_item(Key={"PK": body["item"]["PK"], "SK": body["item"]["SK"]})
    assert "Item" in item_from_db
    assert item_from_db["Item"]["nome"] == "Tarefa de Teste"


def test_lambda_handler_missing_fields():
    event = {"nome": "Tarefa de Teste"}
    context = {}
    result = lambda_handler(event, context)
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert body["message"] == "nome e data são obrigatórios"


def test_lambda_handler_dynamodb_client_error(mocked_add_item_table):
    event = {"nome": "Tarefa de Teste", "data": "2024-12-31"}
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


def test_lambda_handler_generic_exception(mocked_add_item_table):
    event = {"nome": "Tarefa de Teste", "data": "2024-12-31"}
    context = {}
    with patch.object(mocked_add_item_table, "put_item") as mock_put_item:
        mock_put_item.side_effect = Exception("Erro genérico mockado")
        result = lambda_handler(event, context)
        assert result["statusCode"] == 500
        body = json.loads(result["body"])
        assert "Erro interno:" in body["message"]


def test_generate_list_id():
    today = date.today()
    expected_id = today.strftime("%Y%m%d")
    assert generate_list_id() == expected_id


def test_response_function():
    status_code = 201
    body_content = {"status": "created"}
    expected_response = {
        "statusCode": status_code,
        "body": json.dumps(body_content),
        "headers": {"Content-Type": "application/json"},
    }
    assert response(status_code, body_content) == expected_response