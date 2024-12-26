import os
import click
from .iam_manager import NaturalLanguageIAMManager
from .utils.credentials import CredentialManager

class CLI:
    def __init__(self):
        self.cred_manager = CredentialManager()

    def init_credentials(self):
        """Initialize credentials check"""
        try:
            config = self.cred_manager.get_all_credentials()
            return all(config.values())
        except:
            return False

@click.command()
@click.argument('command', required=False)
@click.pass_context
def main_command(ctx, command):
    """Natural Language Interface for AWS IAM
    
    Direct Commands:
        nlpiam "Create a new user named john_doe"
        nlpiam "Add ReadOnlyAccess policy to john_doe"
        nlpiam "List all users"
    
    Setup:
        nlpiam setup              - Run setup wizard
    """
    cli = CLI()
    # If no credentials, force setup
    if not cli.init_credentials() and command != 'setup':
        click.echo("No credentials found. Running setup wizard...")
        setup_wizard()
        return

    if not command:
        click.echo(ctx.get_help())
        return

    if command == 'setup':
        setup_wizard()
    else:
        handle_command(command)

def setup_wizard():
    """Run the interactive setup wizard"""
    try:
        click.echo("Welcome to NLPIAM Setup Wizard!")
        click.echo("We'll help you configure your AWS and OpenAI credentials.\n")

        cred_manager = CredentialManager()

        # AWS Credentials
        click.echo("First, let's set up your AWS credentials:")
        aws_key = click.prompt("Enter your AWS Access Key ID", type=str)
        aws_secret = click.prompt("Enter your AWS Secret Access Key", type=str, hide_input=True)
        aws_region = click.prompt("Enter your AWS Region", type=str, default="us-east-1")

        # OpenAI Credentials
        click.echo("\nNow, let's set up your OpenAI credentials:")
        openai_key = click.prompt("Enter your OpenAI API Key", type=str, hide_input=True)

        # Save all credentials
        cred_manager.set_credential('AWS_ACCESS_KEY_ID', aws_key)
        cred_manager.set_credential('AWS_SECRET_ACCESS_KEY', aws_secret)
        cred_manager.set_credential('AWS_DEFAULT_REGION', aws_region)
        cred_manager.set_credential('OPENAI_API_KEY', openai_key)

        click.echo("\n✅ Credentials saved successfully to ~/.env")
        click.echo("You can now use NLPIAM commands!")
    except Exception as e:
        click.echo(f"❌ Error during setup: {str(e)}", err=True)

def handle_command(command):
    """Handle all IAM commands and subcommands"""
    try:
        # Process as IAM command if in quotes
        if command.startswith('"') or command.startswith("'"):
            command = command.strip('"\'')
            execute_iam_command(command)
            return

        # Handle subcommands
        parts = command.split()
        if parts[0] == 'audit':
            if len(parts) < 2:
                click.echo("Please specify audit type: mfa, keys, or admin")
                return
            handle_audit(parts[1])
        elif parts[0] == 'config':
            if len(parts) < 2:
                click.echo("Please specify config action: show")
                return
            handle_config(parts[1:])
        elif parts[0] == 'explain':
            if len(parts) < 2:
                click.echo("Please provide a command to explain")
                return
            handle_explain(' '.join(parts[1:]))
        else:
            click.echo(f"Unknown command: {command}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

def execute_iam_command(command):
    """Execute an IAM command"""
    try:
        manager = NaturalLanguageIAMManager()
        explanation = manager.explain_action(command)
        click.echo(f"This will: {explanation}")
        
        if click.confirm('Do you want to proceed?'):
            result = manager.process_request(command)
            if 'error' in result:
                click.echo(f"❌ Error: {result['error']}", err=True)
            else:
                click.echo("✅ Success!")
                click.echo(result)
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

def handle_audit(audit_type):
    """Handle audit commands"""
    try:
        manager = NaturalLanguageIAMManager()
        if audit_type == 'mfa':
            result = manager.execute_action('audit_mfa', {})
            if 'error' in result:
                click.echo(f"❌ Error: {result['error']}", err=True)
                return
            
            click.echo("\n📊 MFA Audit Results:")
            click.echo(f"Total Users: {result['total_users']}")
            click.echo(f"Users with MFA: {result['users_with_mfa']}")
            if result.get('users_without_mfa'):
                click.echo("\n⚠️  Users without MFA:")
                for user in result['users_without_mfa']:
                    click.echo(f"  • {user}")
            else:
                click.echo("\n✅ All users have MFA enabled!")

        elif audit_type == 'keys':
            result = manager.execute_action('audit_access_keys', {})
            if 'error' in result:
                click.echo(f"❌ Error: {result['error']}", err=True)
                return

            click.echo("\n📊 Access Key Audit:")
            if not result.get('old_keys'):
                click.echo("✅ No old keys found")
            else:
                click.echo("\n⚠️  Keys older than 90 days:")
                for key in result['old_keys']:
                    click.echo(f"  • User: {key['username']}")
                    click.echo(f"    Key ID: {key['key_id']}")
                    click.echo(f"    Age: {key['age_days']} days")

        elif audit_type == 'admin':
            result = manager.execute_action('audit_admin_users', {})
            if 'error' in result:
                click.echo(f"❌ Error: {result['error']}", err=True)
                return

            click.echo("\n📊 Administrator Access Audit:")
            if not result.get('admin_users') and not result.get('admin_roles'):
                click.echo("✅ No administrators found")
            else:
                if result.get('admin_users'):
                    click.echo("\n⚠️  Users with admin access:")
                    for user in result['admin_users']:
                        click.echo(f"  • {user}")
                if result.get('admin_roles'):
                    click.echo("\n⚠️  Roles with admin access:")
                    for role in result['admin_roles']:
                        click.echo(f"  • {role}")
        else:
            click.echo(f"Unknown audit type: {audit_type}")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

def handle_config(args):
    """Handle config commands"""
    try:
        if args[0] == 'show':
            cred_manager = CredentialManager()
            config = cred_manager.get_all_credentials()
            
            click.echo("\n📊 Current Configuration:")
            for key, value in config.items():
                if value:
                    masked = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '****'
                    click.echo(f"{key}: {masked}")
                else:
                    click.echo(f"{key}: Not set")
        else:
            click.echo(f"Unknown config command: {args[0]}")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

def handle_explain(command):
    """Handle explain command"""
    try:
        manager = NaturalLanguageIAMManager()
        explanation = manager.explain_action(command)
        click.echo(f"This command will: {explanation}")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

def main():
    main_command()

if __name__ == '__main__':
    main()