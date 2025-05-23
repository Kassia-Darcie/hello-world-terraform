import json
import pytest
from todo_list.list_items.list_items_handler import lambda_handler


@pytest.fixture
def mock_event():
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"sub": "test_user_id"}}}}
    }


@pytest.fixture
def mock_dynamodb_response(monkeypatch):
    def mock_query(*args, **kwargs):
        return {
            "Items": [{"PK": "USER#test_user_id", "SK": "ITEM#123", "data": "sample"}]
        }

    monkeypatch.setattr(
        "todo_list.list_items.list_items_handler.table.query", mock_query
    )


def test_lambda_handler_success(mock_event, mock_dynamodb_response):
    response = lambda_handler(mock_event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "tasks" in body
    assert len(body["tasks"]) == 1


def test_lambda_handler_failure(monkeypatch, mock_event):
    def mock_query(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(
        "todo_list.list_items.list_items_handler.table.query", mock_query
    )

    response = lambda_handler(mock_event, None)
    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "error" in body
    assert body["error"] == "Database error"
