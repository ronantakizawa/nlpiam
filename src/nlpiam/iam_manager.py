import boto3
import json
from typing import Dict, Tuple
from openai import OpenAI
from . import config

class NaturalLanguageIAMManager:
    def __init__(self):
        """Initialize the IAM manager with AWS client and OpenAI client."""
        self.iam_client = boto3.client('iam',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_DEFAULT_REGION
        )
        
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Define the supported actions and their required parameters
        self.supported_actions = {
            'create_user': ['username'],
            'delete_user': ['username'],
            'add_policy': ['username', 'policy_name'],
            'remove_policy': ['username', 'policy_name'],
            'list_users': [],
            'list_policies': [],
            'create_group': ['group_name'],
            'delete_group': ['group_name'],
            'add_user_to_group': ['username', 'group_name'],
            'remove_user_from_group': ['username', 'group_name'],
            'create_access_key': ['username'],
            'list_access_keys': ['username'],
            'rotate_access_key': ['username'],
            'audit_mfa': [],
            'audit_access_keys': [],
            'audit_admin_users': []
        }

    def parse_request(self, request: str) -> Tuple[str, Dict[str, str]]:
        """Parse natural language request using OpenAI API."""
        system_prompt = """
        You are an AWS IAM expert that helps parse natural language requests into structured commands.
        Return a JSON object with:
        1. "action": One of the supported actions
        2. "params": A dictionary containing relevant parameters

        Examples:
        - "Create a new user named john_doe" -> {"action": "create_user", "params": {"username": "john_doe"}}
        - "Add ReadOnlyAccess policy to john_doe" -> {"action": "add_policy", "params": {"username": "john_doe", "policy_name": "ReadOnlyAccess"}}
        - "Add policy ReadOnlyAccess to group developers" -> {"action": "add_policy_to_group", "params": {"group_name": "developers", "policy_name": "ReadOnlyAccess"}}
        - "Create access key for john_doe" -> {"action": "create_access_key", "params": {"username": "john_doe"}}
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            parsed = json.loads(response.choices[0].message.content)
            action = parsed['action']
            params = parsed['params']
            
            if action not in self.supported_actions:
                raise ValueError(f"Unsupported action: {action}")
                
            required_params = self.supported_actions[action]
            missing_params = [param for param in required_params if param not in params]
            
            if missing_params:
                raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
                
            return action, params
            
        except Exception as e:
            raise ValueError(f"Failed to parse request: {str(e)}")

    def process_request(self, request: str) -> Dict:
        """Process a natural language request from start to finish."""
        try:
            action, params = self.parse_request(request)
            result = self.execute_action(action, params)
            return result
        except Exception as e:
            return {'error': str(e)}

    def explain_action(self, request: str) -> str:
        """Use OpenAI to explain what action will be taken."""
        try:
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an AWS IAM expert. Explain what this IAM request will do in simple terms."},
                    {"role": "user", "content": request}
                ],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to explain request: {str(e)}"

    def execute_action(self, action: str, params: Dict[str, str]) -> Dict:
        """Execute the requested IAM action with given parameters."""
        if action not in self.supported_actions:
            raise ValueError(f"Unknown action: {action}")
            
        try:
            if action == 'create_user':
                return self.iam_client.create_user(
                    UserName=params['username'],
                    Path=config.DEFAULT_PATH
                )
                
            elif action == 'delete_user':
                return self._delete_user_with_cleanup(params['username'])
                
            elif action == 'add_policy':
                policies = self.iam_client.list_policies()
                policy_arn = None
                for policy in policies['Policies']:
                    if policy['PolicyName'].lower() == params['policy_name'].lower():
                        policy_arn = policy['Arn']
                        break
                
                if not policy_arn:
                    raise ValueError(f"Policy {params['policy_name']} not found")
                    
                return self.iam_client.attach_user_policy(
                    UserName=params['username'],
                    PolicyArn=policy_arn
                )
                
            elif action == 'remove_policy':
                policies = self.iam_client.list_policies()
                policy_arn = None
                for policy in policies['Policies']:
                    if policy['PolicyName'].lower() == params['policy_name'].lower():
                        policy_arn = policy['Arn']
                        break
                        
                if not policy_arn:
                    raise ValueError(f"Policy {params['policy_name']} not found")
                    
                return self.iam_client.detach_user_policy(
                    UserName=params['username'],
                    PolicyArn=policy_arn
                )
                
            elif action == 'list_users':
                return self.iam_client.list_users()
                
            elif action == 'list_policies':
                return self.iam_client.list_policies()
                
            elif action == 'create_group':
                return self.iam_client.create_group(GroupName=params['group_name'])
                
            elif action == 'delete_group':
                return self.iam_client.delete_group(GroupName=params['group_name'])
                
            elif action == 'add_user_to_group':
                return self.iam_client.add_user_to_group(
                    UserName=params['username'],
                    GroupName=params['group_name']
                )
                
            elif action == 'remove_user_from_group':
                return self.iam_client.remove_user_from_group(
                    UserName=params['username'],
                    GroupName=params['group_name']
                )
                
            elif action == 'create_access_key':
                return self.iam_client.create_access_key(UserName=params['username'])
                
            elif action == 'list_access_keys':
                return self.iam_client.list_access_keys(UserName=params['username'])
                
            elif action == 'rotate_access_key':
                return self._rotate_access_key(params['username'])
                
            else:
                raise ValueError(f"Action {action} not implemented")
                
        except Exception as e:
            return {'error': str(e)}

    def _delete_user_with_cleanup(self, username: str) -> Dict:
        """Delete a user and clean up their resources."""
        try:
            # Remove from groups
            groups = self.iam_client.list_groups_for_user(UserName=username)
            for group in groups['Groups']:
                self.iam_client.remove_user_from_group(
                    UserName=username,
                    GroupName=group['GroupName']
                )
                
            # Delete access keys
            keys = self.iam_client.list_access_keys(UserName=username)
            for key in keys['AccessKeyMetadata']:
                self.iam_client.delete_access_key(
                    UserName=username,
                    AccessKeyId=key['AccessKeyId']
                )
                
            # Detach policies
            attached_policies = self.iam_client.list_attached_user_policies(UserName=username)
            for policy in attached_policies['AttachedPolicies']:
                self.iam_client.detach_user_policy(
                    UserName=username,
                    PolicyArn=policy['PolicyArn']
                )
                
            # Finally delete the user
            return self.iam_client.delete_user(UserName=username)
            
        except Exception as e:
            return {'error': str(e)}

    def _rotate_access_key(self, username: str) -> Dict:
        """Create a new access key and delete the old one."""
        try:
            # Create new key
            new_key = self.iam_client.create_access_key(UserName=username)
            
            # List and delete old keys
            old_keys = self.iam_client.list_access_keys(UserName=username)
            for key in old_keys['AccessKeyMetadata']:
                if key['AccessKeyId'] != new_key['AccessKey']['AccessKeyId']:
                    self.iam_client.delete_access_key(
                        UserName=username,
                        AccessKeyId=key['AccessKeyId']
                    )
                    
            return new_key
            
        except Exception as e:
            return {'error': str(e)}