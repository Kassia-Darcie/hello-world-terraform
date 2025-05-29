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

os.environ["DYNAMODB_TABLE_NAME"] = "test-mock-table"   

@pytest.fixture
def mock_event():
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"sub": "test_user_id"}}}}
    }


@pytest.fixture
def mocked_list_items_table(monkeypatch):
    
    import lambdas.todo_list.list_items.list_items_handler as list_items_module

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
        
        try: # Adiciona um bloco try para lidar com a criação de tabela
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
        if "DYNAMODB_TABLE_NAME" in os.environ:
            del os.environ["DYNAMODB_TABLE_NAME"]