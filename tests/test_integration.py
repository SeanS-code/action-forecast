# tests/test_integration.py

from unittest.mock import MagicMock
import pytest
from forecast import forecast, model

@pytest.fixture
def mock_model(mocker):
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[42]])
    mocker.patch('forecast.joblib.load', return_value=mock_model)
    return mock_model

def test_forecast_model_integration():
    forecast_result = forecast.main()
    model_result = model.main()
    
    assert forecast_result is not None
    assert model_result is not None
    assert isinstance(forecast_result, dict)
    assert isinstance(model_result, dict)