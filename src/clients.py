import boto3
from functools import lru_cache
from .config import AWS_REGION_NAME


@lru_cache(maxsize=1)
def get_ssm_client():
    return boto3.client('ssm', region_name=AWS_REGION_NAME)

@lru_cache(maxsize=1)
def get_sqs_client():
    return boto3.client('sqs', region_name=AWS_REGION_NAME, config=boto3.session.Config(retries={'max_attempts': 10}))
