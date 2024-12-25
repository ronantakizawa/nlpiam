from nlpiam.iam_manager import NaturalLanguageIAMManager
import time

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}")

def execute_command(manager, description, command):
    print(f"\n> {description}")
    try:
        result = manager.process_request(command)
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    manager = NaturalLanguageIAMManager()

    # User Management Tests
    print_section("Basic User and Policy Management")
    
    # Create and manage users
    execute_command(manager, "Creating a test user", 
                   "Create a new user named test-user1")
    time.sleep(1)  # Add small delay between operations
    
    execute_command(manager, "Adding ReadOnly policy", 
                   "Add ReadOnlyAccess policy to test-user1")
    time.sleep(1)
    
    execute_command(manager, "Listing all users", 
                   "List all users")
    time.sleep(1)

    # Group Management Tests
    print_section("Group Management")
    
    execute_command(manager, "Creating developers group", 
                   "Create a new group named developers")
    time.sleep(1)
    
    execute_command(manager, "Adding user to group", 
                   "Add test-user1 to developers group")
    time.sleep(1)
    
    execute_command(manager, "Adding CodeCommit policy to group", 
                   "Add AWSCodeCommitPowerUser policy to developers group")
    time.sleep(1)

    # Access Key Tests
    print_section("Access Key Management")
    
    execute_command(manager, "Creating access key", 
                   "Create access key for test-user1")
    time.sleep(1)
    
    execute_command(manager, "Listing access keys", 
                   "List access keys for test-user1")
    time.sleep(1)

    # Security Audit Tests
    print_section("Security Audit")
    
    execute_command(manager, "Checking MFA usage", 
                   "Audit users without MFA")
    time.sleep(1)
    
    execute_command(manager, "Checking access keys", 
                   "Audit old access keys")
    time.sleep(1)

    # Cleanup
    print_section("Cleanup")
    
    execute_command(manager, "Removing user from group", 
                   "Remove test-user1 from developers group")
    time.sleep(1)
    
    execute_command(manager, "Removing ReadOnly policy", 
                   "Remove ReadOnlyAccess policy from test-user1")
    time.sleep(1)
    
    execute_command(manager, "Deleting test user", 
                   "Delete user test-user1")
    time.sleep(1)
    
    execute_command(manager, "Deleting group", 
                   "Delete group developers")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")