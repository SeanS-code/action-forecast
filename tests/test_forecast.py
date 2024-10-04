# tests/test_forecast.py

import pytest
import json
import base64
import numpy as np
import joblib
import datetime

from forecast import forecast
from unittest.mock import MagicMock

@pytest.fixture
def mock_uuid(mocker):
    return mocker.patch('uuid.uuid4', return_value='1234-abcd')

@pytest.fixture
def mock_createreq(mocker):
    return mocker.patch('forecast.redis.createreq')

@pytest.fixture
def mock_returnreq(mocker):
    return mocker.patch('forecast.redis.returnreq')

@pytest.fixture
def mock_savereq(mocker):
    return mocker.patch('forecast.redis.savereq')

@pytest.fixture
def mock_model(mocker):
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[42]])
    mocker.patch('forecast.joblib.load', return_value=mock_model)
    return mock_model


@pytest.fixture
def mock_returnkeys(mocker):
    return mocker.patch('forecast.redis.returnkeys')

def test_submitreq(mock_createreq):
    requestid = 'test_request'
    data = {'features': [1, 2, 3]}
    forecast.submitreq(requestid, data)

    # Verify createreq was called with correct parameters
    encoded_data = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
    current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")
    expected_request_json = {
        "requestid": requestid,
        "message": "In Progress",
        "request": {
            "reqdate": current_date,
            "data": {
                "args": encoded_data
            }
        },
        "response": {
            "resdate": 0,
            "restime": 0,
            "data": {}
        }
    }

    mock_createreq.assert_called_once_with(requestid, json.dumps(expected_request_json))

def test_predictmodel(mock_returnreq, mock_model, mock_savereq):
    # Mock returnreq to return a specific request format
    mock_returnreq.return_value = json.dumps({
        "request": {
            "data": {
                "args": base64.b64encode(json.dumps({'features': [1, 2, 3]}).encode('utf-8')).decode('utf-8')
            }
        },
        "response": {
            "resdate": 0,
            "restime": 0,
            "data": {}
        }
    })

    requestid = 'test_request'
    response_json = forecast.predictmodel(requestid)

    # Check if the prediction was encoded correctly
    predicted_value = base64.b64encode(json.dumps(42).encode('utf-8')).decode('utf-8')
    assert response_json["response"]["data"]["result"] == predicted_value

def test_predictres(mock_returnreq):
    # Mock returnreq response
    mock_returnreq.return_value = json.dumps({
        "requestid": "test_request",
        "message": "Complete"
    })

    requestid = 'test_request'
    result = forecast.predictres(requestid)
    assert result['requestid'] == 'test_request'
    assert result['message'] == 'Complete'

def test_returnallreq(mock_returnkeys):
    # Mock returnkeys response
    mock_returnkeys.return_value = ['req1', 'req2', 'req3']

    result = forecast.returnallreq()
    assert result == ['req1', 'req2', 'req3']
