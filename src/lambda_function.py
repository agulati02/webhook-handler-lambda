import json
import urllib.parse
from base64 import b64decode


def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        print(event)
        # # Decode base64 body and convert bytes to string
        # event_body_decoded = b64decode(event['body']).decode('utf-8')
        
        # # URL decode the payload
        # payload = urllib.parse.unquote(event_body_decoded)

        # # Remove 'payload=' prefix if present
        # if payload.startswith('payload='):
        #     payload = payload[8:]

        # # Parse JSON payload
        # payload_dict = json.loads(payload)
        
        # # Extract repository information
        # repository_name = payload_dict['repository']['name']
        # print(f"Repository name: {repository_name}")

        # count_of_stars = payload_dict['repository']['stargazers_count']
        # print(f"Count of stars: {count_of_stars}")

        # # Extract sender information
        # starring_user = payload_dict['sender']['login']
        # print(f"Starring user: {starring_user}")

        # starring_user_url = payload_dict['sender']['html_url']
        # print(f"Starring user profile URL: {starring_user_url}")

        # # Get the action type to understand what triggered the webhook
        # action = payload_dict.get('action', 'unknown')
        # print(f"Webhook action: {action}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Webhook processed successfully',
            })
        }
        
    except KeyError as e:
        print(f"Missing key in payload: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing required field: {e}'})
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON payload'})
        }
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }