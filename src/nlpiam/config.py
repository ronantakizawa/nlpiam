import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS credentials configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# IAM configuration
DEFAULT_PATH = '/'
FORCE_DESTROY = True  # Whether to force delete users even if they have attached resources

# OpenAI configuration
OPENAI_MODEL = "gpt-4o"