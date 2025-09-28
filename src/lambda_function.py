import json
import urllib.parse
from base64 import b64decode


def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        # Decode the incoming payload
        payload = json.loads(event['body'])
        print(f"Received payload: {json.dumps(payload, indent=2)}")

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