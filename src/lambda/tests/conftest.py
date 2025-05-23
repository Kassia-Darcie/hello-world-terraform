import pytest


@pytest.fixture(autouse=True)
def disable_env_variables(monkeypatch):
    monkeypatch.delenv("DYNAMODB_TABLE_NAME", raising=False)
