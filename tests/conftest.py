# tests/conftest.py

import pytest

@pytest.fixture
def sample_data():
    return {
        "key1": "value1",
        "key2": "value2"
    }