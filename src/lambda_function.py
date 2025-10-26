import sys
sys.path.append('/opt/site-packages')

import json
import orjson
import logging
from typing import Any
from commons.models.enums import UserAction  # type: ignore
from .handlers import handle_review_request, handle_discussion_comment
from .models.dto import Event
from .models.constants import AppConstants


# Configure logging with DEBUG level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

class WebhookEventRouter:
    handlers = {
        UserAction.REVIEW_REQUESTED: handle_review_request,
        UserAction.DISCUSSION_COMMENT: handle_discussion_comment
    }

    def _classify_user_action(self, payload: dict[str, Any], headers: dict[str, Any]) -> UserAction:
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
    
    def _default_handler(self, _payload: dict[str, Any]) -> dict[str, Any]:
        return {
            'statusCode': 200,
            'body': 'Event not actionable'
        }
    
    def route_event(self, event: dict[str, Any]) -> dict[str, Any]:
        payload = orjson.loads(event['body'])
        action = self._classify_user_action(payload, event['headers'])
        
        handler = self.handlers.get(action, self._default_handler)
        return handler(payload)

def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        webhook_handler = WebhookEventRouter()
        return webhook_handler.route_event(event)
    
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
