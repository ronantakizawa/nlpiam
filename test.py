from nlpiam.iam_manager import NaturalLanguageIAMManager

manager = NaturalLanguageIAMManager()

# Add a read-only policy
print("\nAdding ReadOnlyAccess policy:")
add_policy = manager.process_request("Add ReadOnlyAccess policy to test-user1")
print(f"Add policy result: {add_policy}")

# List user's policies
print("\nListing users:")
list_result = manager.process_request("List all users")
print(f"Current users: {list_result}")

# Remove the policy
print("\nRemoving policy:")
remove_policy = manager.process_request("Remove ReadOnlyAccess policy from test-user1")
print(f"Remove policy result: {remove_policy}")

# Delete the user
print("\nDeleting user:")
delete_result = manager.process_request("Delete user test-user1")
print(f"Delete result: {delete_result}")