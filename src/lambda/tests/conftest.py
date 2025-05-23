import pytest


@pytest.fixture(autouse=True)
def disable_env_variables(monkeypatch):
    monkeypatch.delenv("DYNAMODB_TABLE_NAME", raising=False)


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
