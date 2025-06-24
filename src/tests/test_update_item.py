import json
import pytest
from lambdas.shopping_list.update_item.update_item import lambda_handler


def extract_message(result):
    """ Helper para decodificar body e extrair mensagem """
    return json.loads(result["body"]).get("message", "")


def test_missing_id_do_item(mock_event):
    event = {
        "pathParameters": {},
        "body": json.dumps({"nome": "Nova tarefa"})
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 400
    assert "id_do_item" in extract_message(result)


def test_empty_body(mock_event):
    event = {
        "pathParameters": {"id_do_item": "123"},
        "body": "{}"
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 400
    assert "Corpo da requisição" in extract_message(result)


def test_missing_all_fields(mock_event):
    event = {
        "pathParameters": {"id_do_item": "123"},
        "body": json.dumps({})  # vazio → cairá no if not body
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 400
    assert "Corpo da requisição" in extract_message(result)


def test_update_status_only(mock_event, mock_dynamodb):
    event = {
        "pathParameters": {"id_do_item": "11338bc0-004e-42fa-bdb8-f3989a641612"},
        "body": json.dumps({"status": "DONE"})
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["item"]["status"] == "DONE"


def test_update_nome_and_status(mock_event, mock_dynamodb):
    event = {
        "pathParameters": {"id_do_item": "11338bc0-004e-42fa-bdb8-f3989a641612"},
        "body": json.dumps({"nome": "Nova Tarefa", "status": "TODO"})
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["item"]["nome"] == "Nova Tarefa"


def test_invalid_status_value(mock_event, mock_dynamodb):
    event = {
        "pathParameters": {"id_do_item": "11338bc0-004e-42fa-bdb8-f3989a641612"},
        "body": json.dumps({"status": "INVALID"})
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 400
    assert "Status deve ser" in extract_message(result)


def test_item_not_found(mock_event, monkeypatch):
    from lambdas.shopping_list.update_item import update_item as update_item_module

    def not_found_get_item(Key):
        return {}

    mock_table = update_item_module.table
    monkeypatch.setattr(mock_table, "get_item", not_found_get_item)

    event = {
        "pathParameters": {"id_do_item": "nao_existe"},
        "body": json.dumps({"nome": "Qualquer coisa"})
    }
    result = lambda_handler(event, {})
    assert result["statusCode"] == 404
    assert "Item não encontrado" in extract_message(result)
