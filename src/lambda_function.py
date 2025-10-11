import sys
sys.path.append('/opt/site-packages')

import json
import asyncio
import logging

from .repo_handler import RepositoryHandler
from .dto import UserAction, Event
from .constants import AppConstants


def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        payload = json.loads(event['body'])
        action = classify_user_action(payload, event['headers'])

        print(f"Received event: {event['headers'].get('x-github-event', 'unknown')} with action: {action.value}")

        if action == UserAction.REVIEW_REQUESTED:
            return handle_review_request(payload)
        elif action == UserAction.DISCUSSION_COMMENT:
            return handle_discussion_comment(payload)
        
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

def classify_user_action(payload: dict, headers: dict) -> UserAction:
    if headers.get('x-github-event') not in Event._value2member_map_:
        return UserAction.UNKNOWN
    
    event = Event(headers['x-github-event'])
    action = payload['action']
    
    if event == Event.PULL_REQUEST and action == 'review_requested':
        reviewers = [
            reviewer['login'] 
            for reviewer in payload['pull_request']['requested_reviewers']
        ]
        return UserAction.REVIEW_REQUESTED if AppConstants.TGRAFY in reviewers else UserAction.UNKNOWN
    
    if event == Event.ISSUE_COMMENT and action in ['created', 'edited']:
        comment_body = payload['comment']['body'].strip().lower()
        return UserAction.DISCUSSION_COMMENT if f'@{AppConstants.TGRAFY.value}' in comment_body else UserAction.UNKNOWN

    return UserAction.UNKNOWN

def handle_review_request(payload: dict) -> dict:
    repo_handler = RepositoryHandler(connection_timeout=10.0)
    asyncio.run(
        repo_handler.post_greeting_comment(
            comments_url=payload['pull_request']['comments_url'], 
            installation_id=payload['installation']['id']
        )
    )
    # TODO: Push to SQS for async processing
    return {
        'statusCode': 200,
        'body': 'PR review process initiated successfully.'
    }

def handle_discussion_comment(payload: dict) -> dict:
    # TODO: Push to SQS for async processing
    return {
        'statusCode': 200,
        'body': 'Discussion comment received. No action taken yet.'
    }
