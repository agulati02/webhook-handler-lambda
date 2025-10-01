import pytest


@pytest.fixture(scope="module")
def mock_installation_access_token_response():
    return {
        "token": "mocked_installation_access_token",
        "expires_at": "2024-12-31T23:59:59Z"
    }
