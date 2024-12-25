import boto3
import json
from typing import Dict, Tuple
from openai import OpenAI
import nlpiam.config as config

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
            'list_policies': []
        }

    def parse_request(self, request: str) -> Tuple[str, Dict[str, str]]:
        """
        Parse natural language request using OpenAI API to determine action and parameters.
        """
        system_prompt = """
        You are an AWS IAM expert that helps parse natural language requests into structured commands.
        You should return a JSON object with two fields:
        1. "action": One of ["create_user", "delete_user", "add_policy", "remove_policy", "list_users", "list_policies"]
        2. "params": A dictionary containing relevant parameters (username, policy_name)
        
        Example responses:
        For "Create a new user named john_doe":
        {"action": "create_user", "params": {"username": "john_doe"}}
        
        For "Add ReadOnlyAccess policy to john_doe":
        {"action": "add_policy", "params": {"username": "john_doe", "policy_name": "ReadOnlyAccess"}}
        
        Only return the JSON object, nothing else.
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
            
            # Validate the action and parameters
            if action not in self.supported_actions:
                raise ValueError(f"Unsupported action: {action}")
                
            required_params = self.supported_actions[action]
            missing_params = [param for param in required_params if param not in params]
            
            if missing_params:
                raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
                
            return action, params
            
        except Exception as e:
            raise ValueError(f"Failed to parse request: {str(e)}")

    def execute_action(self, action: str, params: Dict[str, str]) -> Dict:
        """Execute the requested IAM action with given parameters."""
        # First validate the action
        if action not in self.supported_actions:
            raise ValueError(f"Unknown action: {action}")
            
        try:
            if action == 'create_user':
                return self.iam_client.create_user(
                    UserName=params['username'],
                    Path=config.DEFAULT_PATH
                )
                
            elif action == 'delete_user':
                if config.FORCE_DESTROY:
                    # First remove all attached policies
                    attached_policies = self.iam_client.list_attached_user_policies(
                        UserName=params['username']
                    )
                    for policy in attached_policies.get('AttachedPolicies', []):
                        self.iam_client.detach_user_policy(
                            UserName=params['username'],
                            PolicyArn=policy['PolicyArn']
                        )
                
                return self.iam_client.delete_user(UserName=params['username'])
                
            elif action == 'add_policy':
                # First get the policy ARN
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
                
        except Exception as e:
            return {'error': str(e)}

    def process_request(self, request: str) -> Dict:
        """Process a natural language request from start to finish."""
        try:
            action, params = self.parse_request(request)
            result = self.execute_action(action, params)
            return result
        except Exception as e:
            return {'error': str(e)}

    def explain_action(self, request: str) -> str:
        """
        Use OpenAI to explain what action will be taken before executing it.
        Useful for confirming the intended action with users.
        """
        system_prompt = """
        You are an AWS IAM expert. Explain what the following IAM request will do in simple terms.
        Be concise but precise. Focus on the practical impact of the action.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request}
                ],
                temperature=0
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Failed to explain request: {str(e)}"