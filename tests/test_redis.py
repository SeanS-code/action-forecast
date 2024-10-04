# src/forecast/test_redis.py
from unittest.mock import MagicMock
import forecast.redis as redis_module

def test_createreq(mocker):
    # Mock the loadredis function to always return a mocked Redis instance
    mock_instance = MagicMock()
    mocker.patch('forecast.redis.loadredis', return_value=mock_instance)

    # Mock Redis methods
    mock_instance.set = MagicMock(return_value=True)
    mock_instance.get = MagicMock(return_value=b'testvalue')
    mock_instance.save = MagicMock(return_value=True)

    # Call the function
    redis_module.createreq("testid", "testvalue")

    # Assert Redis `set` and `get` were called
    mock_instance.set.assert_called_once_with("testid", "testvalue")
    assert redis_module.returnreq("testid") == b'testvalue'


def test_savereq(mocker):
    # Mock the loadredis function to always return a mocked Redis instance
    mock_instance = MagicMock()
    mocker.patch('forecast.redis.loadredis', return_value=mock_instance)

    # Mock Redis methods
    mock_instance.set = MagicMock(return_value=True)
    mock_instance.get = MagicMock(return_value=b'newvalue')
    mock_instance.save = MagicMock(return_value=True)

    # Call the function
    redis_module.savereq("testid", "newvalue")

    # Assert Redis `set` was called
    mock_instance.set.assert_called_once_with("testid", "newvalue")
    assert redis_module.returnreq("testid") == b'newvalue'


def test_returnreq(mocker):
    # Mock the loadredis function to always return a mocked Redis instance
    mock_instance = MagicMock()
    mocker.patch('my_redis.redis.loadredis', return_value=mock_instance)

    # Mock Redis `get` method
    mock_instance.get = MagicMock(return_value=b'retrieved_value')

    # Call the function
    result = redis_module.returnreq("testid")

    # Assert Redis `get` was called with the correct requestid
    mock_instance.get.assert_called_once_with("testid")
    
    # Assert the correct value is returned
    assert result == b'retrieved_value'


def test_returnkeys(mocker):
    # Mock the loadredis function to always return a mocked Redis instance
    mock_instance = MagicMock()
    mocker.patch('forecast.redis.loadredis', return_value=mock_instance)

    # Mock Redis methods
    mock_instance.keys = MagicMock(return_value=[b'testid', b'anotherid'])
    mock_instance.set = MagicMock(return_value=True)

    # Call the function
    redis_module.createreq("anotherid", "anothervalue")

    # Assert Redis `keys` were called and return the expected keys
    keys = redis_module.returnkeys()
    mock_instance.keys.assert_called_once()  # Check that `keys` was called
    assert b"testid" in keys
    assert b"anotherid" in keys
