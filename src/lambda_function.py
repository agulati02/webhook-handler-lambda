import sys
sys.path.append('/opt/site-packages')

import json
import asyncio
import logging

from .repo_handler import RepositoryHandler
from .dto import UserAction


def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        payload = json.loads(event['body'])
        action = classify_user_action(payload)

        if action == UserAction.REVIEW_REQUESTED:
            return handle_review_request(payload)
        
        return {
            'statusCode': 200,
            'body': 'Event not actionable, no further processing.'
        }
    
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': f"Missing key in payload: {e}"
        }

    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError: {e}")
        return {
            'statusCode': 400,
            'body': "Invalid JSON payload"
        }

    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }

def handle_review_request(payload: dict) -> dict:
    repo_handler = RepositoryHandler(connection_timeout=10.0)
    asyncio.run(
        repo_handler.post_greeting_comment(
            comments_url=payload['pull_request']['comments_url'], 
            installation_id=payload['installation']['id']
        )
    )
    return {
        'statusCode': 200,
        'body': 'PR review process initiated successfully.'
    }

def classify_user_action(payload: dict) -> UserAction:
    action = payload['action']
    reviewers = [
        reviewer['login'] 
        for reviewer in payload['pull_request']['requested_reviewers']
    ]
    if action == 'review_requested' and 'tgrafy' in reviewers:
        return UserAction.REVIEW_REQUESTED
    return UserAction.UNKNOWN
