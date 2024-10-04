import pytest
from unittest.mock import patch
from forecast import redis

# src/forecast/test_redis.py


@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('redis.loadredis.redis.Redis')

def test_createreq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = 'test_request'
    req = 'test_data'

    result = redis.createreq(requestid, req)

    mock_redis_instance.set.assert_called_once_with(requestid, req)
    mock_redis_instance.save.assert_called_once()
    assert result == mock_redis_instance.save.return_value

def test_savereq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = 'test_request'
    req = 'test_data'

    result = redis.savereq(requestid, req)

    mock_redis_instance.set.assert_called_once_with(requestid, req)
    mock_redis_instance.save.assert_called_once()
    assert result == mock_redis_instance.save.return_value

def test_returnreq(mock_redis):
    mock_redis_instance = mock_redis.return_value
    requestid = 'test_request'
    expected_data = b'test_data'
    mock_redis_instance.get.return_value = expected_data

    result = redis.returnreq(requestid)

    mock_redis_instance.get.assert_called_once_with(requestid)
    assert result == expected_data

def test_returnkeys(mock_redis):
    mock_redis_instance = mock_redis.return_value
    expected_keys = [b'req1', b'req2', b'req3']
    mock_redis_instance.keys.return_value = expected_keys

    result = redis.returnkeys()

    mock_redis_instance.keys.assert_called_once()
    assert result == expected_keys