import os
from dotenv import load_dotenv

ENV = os.getenv('ENV', 'local')
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'resources', f'.env.{ENV}'))

SECRET_GITHUB_PRIVATE_KEY_PATH = os.getenv('SECRET_GITHUB_PRIVATE_KEY_PATH')
SECRET_DATABASE_USERNAME_PATH = os.getenv('SECRET_DATABASE_USERNAME_PATH')
SECRET_DATABASE_PASSWORD_PATH = os.getenv('SECRET_DATABASE_PASSWORD_PATH')

CLIENT_ID = "Iv23liHKhbBXLoJvAoC7"
JWT_ALGORITHM = 'RS256'

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'ap-southeast-2')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')
DATABASE_NAME = os.getenv('DATABASE_NAME')
EVENTS_COLLECTION = os.getenv('EVENTS_COLLECTION')
