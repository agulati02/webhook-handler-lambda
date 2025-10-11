import sys
sys.path.append('/opt/site-packages')

import json
import asyncio

import logging
from .repo_handler import RepositoryHandler

def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        payload = json.loads(event['body'])

        if not is_actionable_event(payload):
            return {
                'statusCode': 200,
                'body': 'Event not actionable, no further processing.'
            }

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


def is_actionable_event(payload: dict) -> bool:
    action = payload['action']
    reviewers = [
        reviewer['login'] 
        for reviewer in payload['pull_request']['requested_reviewers']
    ]
    if action in ['review_requested'] and 'tgrafy' in reviewers:
        return True
