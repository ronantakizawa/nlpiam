import pytest
from unittest.mock import Mock, patch
from .iam_manager import NaturalLanguageIAMManager

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI response"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"action": "create_user", "params": {"username": "john_doe"}}'
    return mock_response

@pytest.fixture
def iam_manager():
    """Create a mock IAM manager with mocked AWS and OpenAI clients"""
    with patch('boto3.client') as mock_boto, \
         patch('openai.OpenAI') as mock_openai:
        
        manager = NaturalLanguageIAMManager()
        manager.iam_client = Mock()
        
        # Mock OpenAI client
        mock_openai_instance = Mock()
        mock_openai_instance.chat.completions.create = Mock()
        manager.openai_client = mock_openai_instance
        
        yield manager

def test_parse_create_user_request(iam_manager, mock_openai_response):
    # Mock OpenAI response
    iam_manager.openai_client.chat.completions.create.return_value = mock_openai_response
    
    request = "Create a new user named john_doe"
    action, params = iam_manager.parse_request(request)
    
    assert action == 'create_user'
    assert params['username'] == 'john_doe'
    
    # Verify OpenAI was called with correct parameters
    iam_manager.openai_client.chat.completions.create.assert_called_once()
    call_args = iam_manager.openai_client.chat.completions.create.call_args[1]
    assert call_args['temperature'] == 0
    assert call_args['response_format'] == {"type": "json_object"}

def test_parse_add_policy_request(iam_manager):
    # Mock OpenAI response for add policy
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"action": "add_policy", "params": {"username": "john_doe", "policy_name": "ReadOnlyAccess"}}'
    
    iam_manager.openai_client.chat.completions.create.return_value = mock_response
    
    request = "Add ReadOnlyAccess policy to john_doe"
    action, params = iam_manager.parse_request(request)
    
    assert action == 'add_policy'
    assert params['username'] == 'john_doe'
    assert params['policy_name'] == 'ReadOnlyAccess'

def test_execute_create_user(iam_manager):
    iam_manager.iam_client.create_user.return_value = {'User': {'UserName': 'john_doe'}}
    result = iam_manager.execute_action('create_user', {'username': 'john_doe'})
    assert result['User']['UserName'] == 'john_doe'
    iam_manager.iam_client.create_user.assert_called_once()

def test_execute_add_policy(iam_manager):
    # Mock list_policies response
    iam_manager.iam_client.list_policies.return_value = {
        'Policies': [
            {'PolicyName': 'ReadOnlyAccess', 'Arn': 'arn:aws:iam::aws:policy/ReadOnlyAccess'}
        ]
    }
    
    result = iam_manager.execute_action('add_policy', {
        'username': 'john_doe',
        'policy_name': 'ReadOnlyAccess'
    })
    
    iam_manager.iam_client.attach_user_policy.assert_called_once_with(
        UserName='john_doe',
        PolicyArn='arn:aws:iam::aws:policy/ReadOnlyAccess'
    )

def test_explain_action(iam_manager):
    # Mock OpenAI response for explanation
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "This will create a new IAM user named john_doe"
    
    iam_manager.openai_client.chat.completions.create.return_value = mock_response
    
    explanation = iam_manager.explain_action("Create a new user named john_doe")
    assert explanation == "This will create a new IAM user named john_doe"

def test_invalid_action(iam_manager):
    with pytest.raises(ValueError, match="Unknown action: invalid_action"):
        iam_manager.execute_action('invalid_action', {})

def test_missing_parameters(iam_manager):
    # Mock OpenAI response with missing parameters
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"action": "add_policy", "params": {"username": "john_doe"}}'
    
    iam_manager.openai_client.chat.completions.create.return_value = mock_response
    
    with pytest.raises(ValueError, match="Missing required parameters"):
        iam_manager.parse_request("Add policy to john_doe")