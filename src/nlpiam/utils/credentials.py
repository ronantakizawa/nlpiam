import os
from pathlib import Path
from dotenv import load_dotenv, set_key
import click

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

    def setup_wizard(self):
        """Interactive setup wizard for credentials"""
        click.echo("Welcome to NLPIAM Setup Wizard!")
        click.echo("We'll help you configure your AWS and OpenAI credentials.\n")

        # AWS Credentials
        click.echo("First, let's set up your AWS credentials:")
        aws_key = click.prompt("Enter your AWS Access Key ID", type=str)
        aws_secret = click.prompt("Enter your AWS Secret Access Key", type=str, hide_input=True)
        aws_region = click.prompt("Enter your AWS Region", type=str, default="us-east-1")

        self.set_credential('AWS_ACCESS_KEY_ID', aws_key)
        self.set_credential('AWS_SECRET_ACCESS_KEY', aws_secret)
        self.set_credential('AWS_DEFAULT_REGION', aws_region)

        # OpenAI Credentials
        click.echo("\nNow, let's set up your OpenAI credentials:")
        openai_key = click.prompt("Enter your OpenAI API Key", type=str, hide_input=True)
        self.set_credential('OPENAI_API_KEY', openai_key)

        click.echo("\nCredentials have been saved successfully!")
        
    def load_from_aws_credentials(self):
        """Load credentials from AWS credentials file"""
        aws_creds_path = os.path.join(str(Path.home()), '.aws', 'credentials')
        if os.path.exists(aws_creds_path):
            click.echo("Found AWS credentials file. Loading credentials...")
            with open(aws_creds_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if '[default]' in line:
                        for j in range(i+1, min(i+4, len(lines))):
                            if 'aws_access_key_id' in lines[j].lower():
                                key = lines[j].split('=')[1].strip()
                                self.set_credential('AWS_ACCESS_KEY_ID', key)
                            elif 'aws_secret_access_key' in lines[j].lower():
                                secret = lines[j].split('=')[1].strip()
                                self.set_credential('AWS_SECRET_ACCESS_KEY', secret)
            click.echo("AWS credentials loaded successfully!")
            return True
        return False