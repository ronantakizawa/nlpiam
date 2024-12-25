# Natural Language IAM Manager (nlpiam)

A powerful command-line tool that lets you manage AWS IAM using natural language commands. Powered by OpenAI's GPT models for natural language understanding.

## Features

- Natural language interface for AWS IAM management
- User management (create, delete, list users)
- Policy management (attach, detach policies)
- Group management (create groups, add users)
- Access key management (create, list, rotate keys)
- Security auditing (MFA, access keys, admin access)
- Command explanation before execution
- Interactive confirmation for safety

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nlpiam.git
cd nlpiam

# Install the package
pip install -e .
```

## Configuration

Set up your credentials using either method:

1. Environment file:
```bash
# Create .env in your home directory
echo "AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
OPENAI_API_KEY=your_openai_key" > ~/.env
```

2. CLI configuration:
```bash
nlpiam configure aws-access-key YOUR_KEY
nlpiam configure aws-secret-key YOUR_SECRET
nlpiam configure aws-region us-east-1
nlpiam configure openai-key YOUR_OPENAI_KEY
```

## Usage

### Basic IAM Commands
```bash
# Create a new user
nlpiam iam "Create a new user named john_doe"

# Add a policy
nlpiam iam "Add ReadOnlyAccess policy to john_doe"

# Create a group and add user
nlpiam iam "Create a new group named developers"
nlpiam iam "Add john_doe to developers group"

# List resources
nlpiam iam "List all users"
nlpiam iam "List access keys for john_doe"
```

### Security Audits
```bash
# Check MFA status
nlpiam audit mfa

# Check access key age
nlpiam audit keys

# List users with admin access
nlpiam audit admin
```

### Command Explanation
```bash
# Explain what a command will do
nlpiam explain "Add AdminAccess policy to john_doe"
```

## Running Tests

The package includes comprehensive tests:

```bash
# Run all tests
python test.py

# Or run the individual test script
python -m pytest src/test_iam_manager.py
```

## Common Commands Reference

1. User Management:
```bash
nlpiam iam "Create a new user named {username}"
nlpiam iam "Delete user {username}"
nlpiam iam "Add {policy_name} policy to {username}"
nlpiam iam "Remove {policy_name} policy from {username}"
```

2. Group Management:
```bash
nlpiam iam "Create a new group named {groupname}"
nlpiam iam "Add {username} to {groupname} group"
nlpiam iam "Add {policy_name} policy to {groupname} group"
```

3. Access Keys:
```bash
nlpiam iam "Create access key for {username}"
nlpiam iam "List access keys for {username}"
nlpiam iam "Rotate access key for {username}"
```

4. Security:
```bash
nlpiam audit mfa
nlpiam audit keys
nlpiam audit admin
```

## Security Best Practices

1. Always review the command explanation before confirming execution
2. Use the principle of least privilege when assigning permissions
3. Regularly audit user access and permissions using the audit commands
4. Rotate access keys periodically
5. Enable MFA for all IAM users

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.