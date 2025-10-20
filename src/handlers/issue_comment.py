from ..bootstrap import push_to_sqs
from ..dto import UserAction


def handle_discussion_comment(payload: dict) -> dict:
    push_to_sqs({**payload, "trigger": UserAction.DISCUSSION_COMMENT})
    return {
        'statusCode': 200,
        'body': 'Discussion comment received. No action taken yet.'
    }
