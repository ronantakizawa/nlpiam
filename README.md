# Natural Language IAM Manager

This tool allows you to manage AWS IAM resources using natural language commands.

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Configure AWS credentials:
   - Create a `.env` file based on `.env.example`
   - Or set up AWS credentials using AWS CLI: `aws configure`

## Usage

```python
from src.iam_manager import NaturalLanguageIAMManager

# Initialize the manager
iam_manager = NaturalLanguageIAMManager()

# Process a request
result = iam_manager.process_request("Create a new user named john_doe")
print(result)
```

## Supported Commands

- Create user: "Create a new user named {username}"
- Delete user: "Delete user {username}"
- Add policy: "Add {policy_name} policy to {username}"
- Remove policy: "Remove {policy_name} policy from {username}"
- List users: "List all users"
- List policies: "List all policies"

## Running Tests

```bash
pytest src/test_iam_manager.py
```