# tests/test_integration.py

import pytest
from forecast import forecast, model

def test_forecast_model_integration():
    forecast_result = forecast.main()
    model_result = model.main()
    
    assert forecast_result is not None
    assert model_result is not None
    assert isinstance(forecast_result, dict)
    assert isinstance(model_result, dict)