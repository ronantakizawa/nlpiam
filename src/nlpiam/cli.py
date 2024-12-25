import os
import click
from .iam_manager import NaturalLanguageIAMManager
from .utils.credentials import CredentialManager

class NLPIamCLI:
    def __init__(self):
        self.cred_manager = CredentialManager()
        
@click.group()
def cli():
    """Natural Language Interface for AWS IAM"""
    pass

@cli.command()
@click.argument('text', required=False)
def iam(text):
    """Execute an IAM command using natural language"""
    if not text:
        click.echo("Please provide a command. Example: nlpiam iam 'Create a new user named john'")
        return
        
    try:
        manager = NaturalLanguageIAMManager()
        # First explain what will happen
        explanation = manager.explain_action(text)
        click.echo(f"This will: {explanation}")
        
        if click.confirm('Do you want to proceed?'):
            result = manager.process_request(text)
            if 'error' in result:
                click.echo(f"Error: {result['error']}", err=True)
            else:
                click.echo("Success!")
                click.echo(result)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('text')
def explain(text):
    """Explain what a command will do without executing it"""
    manager = NaturalLanguageIAMManager()
    explanation = manager.explain_action(text)
    click.echo(f"This command will: {explanation}")

@cli.group()
def config():
    """Manage credentials and configuration"""
    pass

@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration value (aws-access-key, aws-secret-key, aws-region, openai-key)"""
    cred_manager = CredentialManager()
    key_mapping = {
        'aws-access-key': 'AWS_ACCESS_KEY_ID',
        'aws-secret-key': 'AWS_SECRET_ACCESS_KEY',
        'aws-region': 'AWS_DEFAULT_REGION',
        'openai-key': 'OPENAI_API_KEY'
    }
    
    if key not in key_mapping:
        click.echo(f"Invalid key. Valid keys are: {', '.join(key_mapping.keys())}")
        return
        
    env_key = key_mapping[key]
    cred_manager.set_credential(env_key, value)
    click.echo(f"Successfully set {key}")

@config.command()
def show():
    """Show current configuration"""
    cred_manager = CredentialManager()
    config = cred_manager.get_all_credentials()
    for key, value in config.items():
        if value:
            masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '****'
            click.echo(f"{key}: {masked_value}")

@cli.group()
def audit():
    """Security audit commands"""
    pass

@audit.command()
def mfa():
    """Check for users without MFA"""
    manager = NaturalLanguageIAMManager()
    result = manager.execute_action('audit_mfa', {})
    if 'error' in result:
        click.echo(f"Error: {result['error']}", err=True)
    else:
        click.echo("MFA Audit Results:")
        click.echo(f"Total Users: {result['total_users']}")
        click.echo(f"Users with MFA: {result['users_with_mfa']}")
        click.echo("Users without MFA:")
        for user in result['users_without_mfa']:
            click.echo(f"  - {user}")

@audit.command()
def keys():
    """Check access key age and usage"""
    manager = NaturalLanguageIAMManager()
    result = manager.execute_action('audit_access_keys', {})
    if 'error' in result:
        click.echo(f"Error: {result['error']}", err=True)
    else:
        click.echo("Access Key Audit Results:")
        click.echo("\nOld Keys (>90 days):")
        for key in result['old_keys']:
            click.echo(f"  - User: {key['username']}, Key: {key['key_id']}, Age: {key['age_days']} days")

@audit.command()
def admin():
    """List users and roles with administrator access"""
    manager = NaturalLanguageIAMManager()
    result = manager.execute_action('audit_admin_users', {})
    if 'error' in result:
        click.echo(f"Error: {result['error']}", err=True)
    else:
        click.echo("Administrator Access Audit:")
        click.echo("\nUsers with admin access:")
        for user in result['admin_users']:
            click.echo(f"  - {user}")
        click.echo("\nRoles with admin access:")
        for role in result['admin_roles']:
            click.echo(f"  - {role}")

def main():
    cli()

if __name__ == '__main__':
    main()