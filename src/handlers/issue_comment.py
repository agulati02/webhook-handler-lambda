from ..bootstrap import push_to_sqs


def handle_discussion_comment(payload: dict) -> dict:
    push_to_sqs(payload)
    return {
        'statusCode': 200,
        'body': 'Discussion comment received. No action taken yet.'
    }
