from typing import Any
from commons.utils.dependencies import get_repository_service   # type: ignore
from commons.models.enums import UserAction  # type: ignore
from ..config import AWS_REGION_NAME, GITHUB_PRIVATE_KEY_PATH, CLIENT_ID
from ..bootstrap import push_to_sqs


def handle_review_request(payload: dict[str, Any]) -> dict[str, Any]:
    if not GITHUB_PRIVATE_KEY_PATH:
        print("GITHUB_PRIVATE_KEY_PATH is not set. Cannot proceed with review request handling.")
        return {
            'statusCode': 500,
            'body': 'Server configuration error.'
        }
    repo_service = get_repository_service(
        aws_region_name=AWS_REGION_NAME,
        repo_private_key_path=GITHUB_PRIVATE_KEY_PATH,
    )
    repo_service.post_issue_comment(
        comments_url=payload['pull_request']['comments_url'], 
        installation_id=payload['installation']['id'],
        content="Thanks for requesting a review!\nI'll get to it shortly. :nerd:",
        app_client_id=CLIENT_ID
    )
    push_to_sqs({**payload, "trigger": UserAction.REVIEW_REQUESTED})
    return {
        'statusCode': 200,
        'body': 'PR review process initiated successfully.'
    }
