from httpx import AsyncClient


class RepositoryHandler:
    def __init__(self, connection_timeout: float = 10.0, ca_certs: str = None):
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

    async def get_pr_diff(self, diff_url: str) -> str:
        response = await self.client.get(diff_url, follow_redirects=True)
        response.raise_for_status()
        return response.text
