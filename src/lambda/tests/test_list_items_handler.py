import pytest
import json
import importlib
import sys
import os
from botocore.exceptions import ClientError


class FakeTable:
    def query(self, KeyConditionExpression):
        return {"Items": [{"PK": "USER#123", "SK": "ITEM#001", "title": "Buy milk"}]}


def test_success(monkeypatch):
    fake_db = type("FakeDynamoDB", (), {"Table": lambda *args: FakeTable()})
    monkeypatch.setattr("boto3.resource", lambda *args, **kwargs: fake_db)

    from list_items_handler import lambda_handler

    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "123"}}}}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "tasks" in body
    assert any(item["title"] == "Buy milk" for item in body["tasks"])


def test_failure(monkeypatch):
    class FailureTable:
        def query(self, KeyConditionExpression):
            raise ClientError(
                {"Error": {"Code": "500", "Message": "Dynamo error"}}, "query"
            )

    monkeypatch.setattr(
        "boto3.resource",
        lambda *args, **kwargs: type(
            "FakeDB", (), {"Table": lambda *args: FailureTable()}
        )(),
    )

    if "list_items_handler" in sys.modules:
        del sys.modules["list_items_handler"]

    from list_items_handler import lambda_handler

    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "123"}}}}}
    response = lambda_handler(event, None)

    assert (
        response["statusCode"] == 500
    ), f"Expected 500 but got {response['statusCode']}. Response: {response}"
    assert (
        "Dynamo error" in response["body"]
    ), f"Error message not found in: {response['body']}"
