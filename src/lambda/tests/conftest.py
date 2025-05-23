# conftest.py
import os
import sys
import pytest


def pytest_configure():
    os.environ["DYNAMODB_TABLE_NAME"] = "fake-table"

    sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "todo_list", "list_items")
        ),
    )
