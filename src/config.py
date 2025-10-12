import os
from dotenv import load_dotenv

ENV = os.getenv('ENV', 'local')
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'resources', f'.env.{ENV}'))

GITHUB_PRIVATE_KEY_PATH = os.getenv('GITHUB_PRIVATE_KEY_PATH')
CLIENT_ID = 'Iv23liHKhbBXLoJvAoC7'
JWT_ALGORITHM = 'RS256'
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'ap-southeast-2')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')