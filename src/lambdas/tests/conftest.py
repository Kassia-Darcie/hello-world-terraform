import os
import sys
import pytest
import boto3
from moto import mock_aws
from unittest.mock import MagicMock

# Adiciona o diretório 'src/' ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Define variável de ambiente usada no código
os.environ["DYNAMODB_TABLE_NAME"] = "test-mock-table"

@pytest.fixture
def mock_event():
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"sub": "test_user_id"}}}}
    }

@pytest.fixture
def mocked_list_items_table(monkeypatch):
    import lambdas.shopping_list.list_items.list_items_handler as list_items_module

    mock_table_instance = MagicMock()
    mock_table_instance.query.return_value = {
        "Items": [{"PK": "USER#test_user_id", "SK": "ITEM#123", "data": "sample"}]
    }

    monkeypatch.setattr(list_items_module, "table", mock_table_instance)
    yield mock_table_instance

@pytest.fixture(scope="session")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def dynamodb_resource_and_name(aws_credentials):
    original_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    moto_table_name = "test-shopping-list-table"
    os.environ["DYNAMODB_TABLE_NAME"] = moto_table_name

    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        try:
            table = dynamodb.create_table(
                TableName=moto_table_name,
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
            table.wait_until_exists()
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            table = dynamodb.Table(moto_table_name)

        yield dynamodb, moto_table_name

    if original_table_name is not None:
        os.environ["DYNAMODB_TABLE_NAME"] = original_table_name
    else:
        os.environ.pop("DYNAMODB_TABLE_NAME", None)

@pytest.fixture
def mock_dynamodb(monkeypatch):
    from lambdas.shopping_list.update_item import update_item as update_item_module

    mock_table = MagicMock()

    def mock_get_item(Key):
        if Key["SK"] == "ITEM#11338bc0-004e-42fa-bdb8-f3989a641612":
            return {
                "Item": {
                    "PK": Key["PK"],
                    "SK": Key["SK"],
                    "nome": "Tarefa Teste",
                    "data": "2025-05-29",
                    "status": "TODO"
                }
            }
        return {}

    def mock_get_item_not_found(Key):
        return {}

    def mock_update_item(**kwargs):
        values = kwargs.get("ExpressionAttributeValues", {})
        pk = kwargs["Key"]["PK"]
        sk = kwargs["Key"]["SK"]

        # Dados simulados do item atual no banco
        current_item = {
            "PK": pk,
            "SK": sk,
            "nome": "Tarefa Teste",
            "data": "2025-05-29",
            "status": "TODO"
        }

        # Aplica os novos valores enviados
        for key_alias, value in values.items():
            field = key_alias[1:]
            if field == "n":
                current_item["nome"] = value
            elif field == "d":
                current_item["data"] = value
            elif field == "s":
                current_item["status"] = value

        return {"Attributes": current_item}

    mock_table.get_item.side_effect = mock_get_item
    mock_table.update_item.side_effect = mock_update_item

    monkeypatch.setattr(update_item_module, "table", mock_table)

    return {
        "table": mock_table,
        "get_item_not_found": mock_get_item_not_found
    }
