# src/forecast/test_redis.py

import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
import forecast


@pytest.fixture
def mock_redis(mocker):

    # Create a mock Redis instance
    mock_redis_instance = MagicMock()

    # Patch redis.Redis to return the mock instance
    mocker.patch('redis.Redis', return_value=mock_redis_instance)

    return mock_redis_instance

# Test loadredis function
def test_loadredis(mock_redis):
    # Act
    mock_redis_instance = forecast.redis.loadredis()
    
    # Assert
    # Verify that the Redis instance was created
    assert mock_redis_instance == mock_redis


def test_createreq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = '1234'
    req = 'test_data'

    result = forecast.redis.createreq(requestid, req)

    mock_redis_instance.set.assert_called_once_with(requestid, req)
    mock_redis_instance.save.assert_called_once()
    assert result == mock_redis_instance.save.return_value


def test_savereq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = '1234'
    req = 'test_data'

    result = forecast.redis.savereq(requestid, req)

    mock_redis_instance.set.assert_called_once_with(requestid, req)
    mock_redis_instance.save.assert_called_once()
    assert result == mock_redis_instance.save.return_value


def test_returnreq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = '1234'
    expected_data = b'test_data'
    mock_redis_instance.get.return_value = expected_data

    result = forecast.redis.returnreq(requestid)

    mock_redis_instance.get.assert_called_once_with(requestid)
    assert result == expected_data


def test_returnkeys(mock_redis):
    mock_redis_instance = mock_redis.return_value
    expected_keys = [b'req1', b'req2', b'req3']
    mock_redis_instance.keys.return_value = expected_keys

    result = forecast.redis.returnkeys()

    mock_redis_instance.keys.assert_called_once()
    assert result == expected_keys

