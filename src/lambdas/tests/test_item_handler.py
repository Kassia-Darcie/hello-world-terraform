import json

from lambdas.todo_list.list_items.list_items_handler import lambda_handler

def test_lambda_handler_success(mock_event, mocked_list_items_table):
    
    response = lambda_handler(mock_event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "tasks" in body
    assert len(body["tasks"]) == 1


def test_lambda_handler_failure(monkeypatch, mock_event, mocked_list_items_table):
    # garante que ele não tente mockar um objeto que já foi substituído por outro mock
    mocked_list_items_table.query.side_effect = Exception("Database error")

    response = lambda_handler(mock_event, None)
    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "error" in body
    assert body["error"] == "Database error"