import asyncio
from ..bootstrap import push_to_sqs
from ..services import GitHubService


def handle_review_request(payload: dict) -> dict:
    repo_handler = GitHubService(connection_timeout=10.0)
    asyncio.run(
        repo_handler.post_greeting_comment(
            comments_url=payload['pull_request']['comments_url'], 
            installation_id=payload['installation']['id']
        )
    )
    push_to_sqs(payload)
    return {
        'statusCode': 200,
        'body': 'PR review process initiated successfully.'
    }