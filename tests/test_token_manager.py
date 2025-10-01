import pytest
from unittest.mock import Mock, patch
from src.token_manager import TokenManager


def test_get_jwt_token():
    jwt_token = TokenManager.get_jwt_token()
    assert jwt_token is not None
    assert isinstance(jwt_token, str)
    assert len(jwt_token) > 0

def test_get_installation_access_token(mock_installation_access_token_response):
    jwt_token = TokenManager.get_jwt_token()
    installation_id = 87178034

    with patch('src.token_manager.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = mock_installation_access_token_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        access_token = TokenManager.get_installation_access_token(jwt_token, installation_id)
        assert access_token == "mocked_installation_access_token"
        mock_post.assert_called_once()
