import os
from pathlib import Path
from dotenv import load_dotenv, set_key

class CredentialManager:
    def __init__(self):
        """Initialize the credential manager"""
        self.env_path = os.path.join(str(Path.home()), '.env')
        self._ensure_env_file()
        load_dotenv(self.env_path)

    def _ensure_env_file(self):
        """Ensure .env file exists in home directory"""
        if not os.path.exists(self.env_path):
            with open(self.env_path, 'w') as f:
                f.write("# AWS and OpenAI Credentials\n")

    def set_credential(self, key: str, value: str):
        """Set a credential in the .env file"""
        set_key(self.env_path, key, value)
        os.environ[key] = value

    def get_credential(self, key: str) -> str:
        """Get a credential value"""
        return os.getenv(key)

    def get_all_credentials(self) -> dict:
        """Get all credentials"""
        return {
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION'),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
        }