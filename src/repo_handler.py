from httpx import AsyncClient


client = AsyncClient(
    timeout=10.0, 
    verify=True,
    headers={
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
       'Accept': 'text/plain, */*',
       'Accept-Encoding': 'gzip, deflate',
       'Connection': 'keep-alive'
   }
)

async def main():
    response = await client.get(
        "https://github.com/agulati02/sample-service/pull/4.diff",
        follow_redirects=True
    )
    print(response.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
