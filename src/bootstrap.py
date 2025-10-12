import json
import logging

from .config import SQS_QUEUE_URL
from .clients import get_sqs_client


def push_to_sqs(message: dict):
    sqs_client = get_sqs_client()
    response = sqs_client.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    logging.info(f"SQS message sent with ID: {response.get('MessageId')}")
    return response