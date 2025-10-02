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
        diff_url = payload['pull_request']['diff_url']

        repo_handler = RepositoryHandler(connection_timeout=10.0)
        response = asyncio.run(
            repo_handler.post_greeting_comment(
                comments_url=payload['pull_request']['comments_url'], 
                installation_id=payload['installation']['id']
            )
        )

        return {
            'statusCode': 200,
            'body': response
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
