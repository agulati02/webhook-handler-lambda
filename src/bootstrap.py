import orjson
import logging
from typing import Any

from .config import SQS_QUEUE_URL
from .utils.clients import get_sqs_client # type: ignore


def push_to_sqs(message: dict[str, Any]) -> None:
    try:
        sqs_client = get_sqs_client()   # type: ignore
        response: dict[str, Any] = sqs_client.send_message( # type: ignore
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=orjson.dumps(message)
        )
        logging.info(f"SQS message sent with ID: {response["MessageId"]}")
    except KeyError as e:
        logging.error(f"KeyError while pushing to SQS: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while pushing to SQS: {e}")
