from httpx import AsyncClient
from .token_manager import TokenManager


class GitHubService:
    def __init__(self, connection_timeout: float = 10.0, ca_certs: str = None) -> None:
        self.client = AsyncClient(
            timeout=connection_timeout, 
            verify=ca_certs if ca_certs else True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
        )

    async def post_greeting_comment(self, comments_url: str, installation_id: int) -> dict:
        jwt_token = TokenManager.get_jwt_token()
        access_token = TokenManager.get_installation_access_token(jwt_token, installation_id)

        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github+json'
        }
        payload = {
            'body': "Hey there! Thanks for the PR! \n Let me review the code and get back to you shortly. 🤓"
        }
        
        response = await self.client.post(comments_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
