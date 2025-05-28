import pytest
import os
from moto import mock_aws
import boto3
import sys
from unittest.mock import MagicMock 

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

@pytest.fixture
def mock_event():
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"sub": "test_user_id"}}}}
    }


# mockar a tabela global para list_items_handler
@pytest.fixture
def mocked_list_items_table(monkeypatch):

    # Mocka a variável global 'table' no módulo list_items_handler.
    import lambdas.todo_list.list_items.list_items_handler as list_items_module

    mock_table_instance = MagicMock()

    # Configura o mock_table_instance para o método 'query'
    mock_table_instance.query.return_value = {
        "Items": [{"PK": "USER#test_user_id", "SK": "ITEM#123", "data": "sample"}]
    }

    # Aplica o mock na variável global 'table' do módulo list_items_handler
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
    
    os.environ["DYNAMODB_TABLE_NAME"] = "test-shopping-list-table"
    
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table_name = os.environ["DYNAMODB_TABLE_NAME"]

    yield dynamodb, table_name
    
    del os.environ["DYNAMODB_TABLE_NAME"]