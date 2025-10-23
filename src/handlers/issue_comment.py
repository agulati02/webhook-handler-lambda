from typing import Any
from commons.models.enums import UserAction # type: ignore
from ..bootstrap import push_to_sqs


def handle_discussion_comment(payload: dict[str, Any]) -> dict[str, Any]:
    push_to_sqs({**payload, "trigger": UserAction.DISCUSSION_COMMENT})
    return {
        'statusCode': 200,
        'body': 'Discussion comment received. No action taken yet.'
    }
