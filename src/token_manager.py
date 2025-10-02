import jwt
import requests
from datetime import datetime, timedelta, timezone
from .config import GITHUB_PRIVATE_KEY_PATH, CLIENT_ID, JWT_ALGORITHM, ENV
from .clients import get_ssm_client

class TokenManager:

    @staticmethod
    def get_jwt_token() -> str:
        private_key = None
        if ENV.lower() == 'local':
            with open(GITHUB_PRIVATE_KEY_PATH, 'r') as key_file:
                private_key = key_file.read()
        else:
            ssm_client = get_ssm_client()
            parameter = ssm_client.get_parameter(Name=GITHUB_PRIVATE_KEY_PATH, WithDecryption=True)
            private_key = parameter['Parameter']['Value']

        payload = {
            'iat': int(datetime.now(timezone.utc).timestamp()),
            'exp': int((datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp()),
            'iss': CLIENT_ID,
            'alg': JWT_ALGORITHM
        }

        jwt_token = jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM)
        return jwt_token
    
    @staticmethod
    def get_installation_access_token(jwt_token: str, installation_id: int) -> str:
        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github+json'
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json().get('token', None)
