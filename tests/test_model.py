# tests/test_model.py

import pytest
from forecast import model

def test_model_main():
    result = model.main()
    assert result is not None
    assert isinstance(result, dict)