import os
import json
import pytest
from list_items_handler import lambda_handler


def test_success(monkeypatch):
    os.environ["DYNAMODB_TABLE_NAME"] = "fake-table"

    class FakeTable:
        def query(self, KeyConditionExpression):
            return {
                "Items": [{"PK": "USER#123", "SK": "ITEM#001", "title": "Buy milk"}]
            }

    class FakeDynamoDB:
        def Table(self, name):
            return FakeTable()

    monkeypatch.setattr(
        "list_items_handler.boto3.resource", lambda service: FakeDynamoDB()
    )

    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "123"}}}}}

    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert "Buy milk" in response["body"]


def test_failure(monkeypatch):
    os.environ["DYNAMODB_TABLE_NAME"] = "fake-table"

    class FakeTable:
        def query(self, KeyConditionExpression):
            raise Exception("Dynamo error")

    class FakeDynamoDB:
        def Table(self, name):
            return FakeTable()

    monkeypatch.setattr(
        "list_items_handler.boto3.resource", lambda service: FakeDynamoDB()
    )

    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "123"}}}}}

    response = lambda_handler(event, None)
    assert response["statusCode"] == 500
    assert "Dynamo error" in response["body"]
