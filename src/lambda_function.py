import json
import asyncio
from repo_handler import RepositoryHandler

async def lambda_handler(event, context):
    """
    Receives the GitHub webhook call and orchestrates the code review process  
    """
    try:
        repo_handler = RepositoryHandler(connection_timeout=10.0)

        # Decode the incoming payload
        payload = json.loads(event['body'])
        diff_url = payload['pull_request']['diff_url']

        # Fetch the PR diff
        response = await repo_handler.get_pr_diff(diff_url)
        print(response)

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