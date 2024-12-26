# Natural Language IAM Manager (nlpiam)

Manage AWS IAM using natural language commands. Powered by OpenAI's GPT models.

## Quick Start
```bash
# Install
pip install git+https://github.com/yourusername/nlpiam.git

# Setup
nlpiam setup

# Start using
nlpiam "Create a new user named john_doe"
```

## Features
- Natural language interface for AWS IAM
- Automatic credential management
- Security auditing and best practices
- Command previews and confirmations
- Comprehensive error handling

## Installation

1. Clone and install:
```bash
git clone https://github.com/yourusername/nlpiam.git
cd nlpiam
pip install -e .
```

2. Run setup:
```bash
nlpiam setup
```

## Usage

### IAM Commands
Always use quotes for IAM commands:
```bash
# User Management
nlpiam "Create a new user named john_doe"
nlpiam "Add ReadOnlyAccess policy to john_doe"
nlpiam "List all users"

# Group Management
nlpiam "Create a group named developers"
nlpiam "Add john_doe to developers group"

# Policy Management
nlpiam "Add S3ReadOnly policy to developers group"
nlpiam "Remove AdminAccess policy from john_doe"
```

### Security Audits
No quotes needed for audit commands:
```bash
# Check MFA status
nlpiam audit mfa

# Check access keys
nlpiam audit keys

# Check admin access
nlpiam audit admin
```

### Helper Commands
```bash
# Preview a command
nlpiam explain "Add AdminAccess policy to john_doe"

# Show configuration
nlpiam config show
```

## Available Commands

### User Operations
- Create user: `"Create a new user named {username}"`
- Delete user: `"Delete user {username}"`
- List users: `"List all users"`

### Policy Operations
- Attach policy: `"Add {policy} policy to {username}"`
- Detach policy: `"Remove {policy} policy from {username}"`
- List policies: `"List all policies"`

### Group Operations
- Create group: `"Create a group named {groupname}"`
- Add to group: `"Add {username} to {groupname} group"`
- List groups: `"List all groups"`

### Access Key Operations
- Create key: `"Create access key for {username}"`
- List keys: `"List access keys for {username}"`
- Rotate key: `"Rotate access key for {username}"`

## Security Best Practices

1. Always review command previews before confirming
2. Run regular security audits:
   ```bash
   nlpiam audit mfa    # Check MFA status
   nlpiam audit keys   # Check old access keys
   nlpiam audit admin  # Check admin privileges
   ```
3. Use least privilege when assigning permissions
4. Enable MFA for all users
5. Rotate access keys regularly

## Error Handling

The tool provides clear feedback:
- ✅ Success messages
- ❌ Error details
- ⚠️ Warning alerts
- 📊 Audit results

## Testing

Run the test suite:
```bash
# All tests
python test.py

# Specific tests
python test_specific.py
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details.