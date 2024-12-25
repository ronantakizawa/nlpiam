# Natural Language IAM Manager (nlpiam)

A command-line tool that allows you to manage AWS IAM using natural language commands.

## Installation

```bash
pip install nlpiam
```

## Configuration

Create a `.env` file in your home directory with your credentials:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
OPENAI_API_KEY=your_openai_key
```

Or set them using the CLI:

```bash
nlpiam config set aws-access-key YOUR_KEY
nlpiam config set aws-secret-key YOUR_SECRET
nlpiam config set aws-region us-east-1
nlpiam config set openai-key YOUR_OPENAI_KEY
```

## Usage

```bash
# Create a new user
nlpiam "Create a new user named john_doe"

# Add a policy
nlpiam "Add ReadOnlyAccess policy to john_doe"

# List users
nlpiam "List all users"

# Remove a policy
nlpiam "Remove ReadOnlyAccess policy from john_doe"

# Delete a user
nlpiam "Delete user john_doe"

# Get an explanation of what a command will do
nlpiam explain "Add AdminAccess policy to john_doe"
```

## Features

- Natural language interface for IAM management
- Secure credential management
- Command explanation before execution
- Support for all basic IAM operations