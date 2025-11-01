import time
import logging
from typing import Any
from commons.models.enums import UserAction # type: ignore
from commons.utils.dependencies import get_database_service, get_secrets_manager, get_repository_service    # type: ignore
from ..bootstrap import push_to_sqs
from ..models.dto import EventStatus
from ..config import SECRET_GITHUB_PRIVATE_KEY_PATH, DATABASE_CONNECTION_STRING, SECRET_DATABASE_USERNAME_PATH, SECRET_DATABASE_PASSWORD_PATH, DATABASE_NAME, EVENTS_COLLECTION, AWS_REGION_NAME, CLIENT_ID


def handle_discussion_comment(payload: dict[str, Any]) -> dict[str, Any]:
    if not (SECRET_GITHUB_PRIVATE_KEY_PATH and SECRET_DATABASE_USERNAME_PATH and SECRET_DATABASE_PASSWORD_PATH and DATABASE_NAME and EVENTS_COLLECTION):
        print(
            "GITHUB_PRIVATE_KEY_PATH / SECRET_DATABASE_USERNAME_PATH / SECRET_DATABASE_PASSWORD_PATH / DATABASE_NAME / EVENTS_COLLECTION not set. Cannot proceed with review request handling."
        )
        return {
            'statusCode': 500,
            'body': 'Server configuration error.'
        }
    repo_service = get_repository_service(
        aws_region_name=AWS_REGION_NAME,
        repo_private_key_path=SECRET_GITHUB_PRIVATE_KEY_PATH,
    )
    db_username, db_password = tuple(get_secrets_manager(AWS_REGION_NAME).get_secrets(
        [SECRET_DATABASE_USERNAME_PATH, SECRET_DATABASE_PASSWORD_PATH]
    ))  # type: ignore
    with get_database_service(
        conn_string=DATABASE_CONNECTION_STRING,
        database_name=DATABASE_NAME,
        username=db_username,
        password=db_password
    ) as db_client:
        start = time.time()
        response = db_client.query(
            collection=EVENTS_COLLECTION,
            filter={
                "installation_id": payload['installation']['id'],
                "pull_request_id": payload['pull_request']['id'],
                "status": {"$nin": [EventStatus.COMPLETED, EventStatus.EXCEPTION]}
            },
            select={"_id": 1}
        )
        end = time.time()
        logging.info(f"DB query time: {end - start} seconds")
        if len(response) > 0:
            start = time.time()
            repo_service.post_issue_comment(
                comments_url=payload['pull_request']['comments_url'],
                installation_id=payload['installation']['id'],
                content="In the middle of another task regarding this PR, please wait for 5 minutes before requesting a new task.",
                app_client_id=CLIENT_ID
            )
            end = time.time()
            logging.info(f"Repository comment call: {end - start} seconds")
            return {
                'statusCode': 200,
                'body': 'Another task in progress.'
            }
    push_to_sqs({**payload, "trigger": UserAction.DISCUSSION_COMMENT})
    return {
        'statusCode': 200,
        'body': 'Discussion comment received. No action taken yet.'
    }
