import pytest
from security.authorization import AuthorizationManager, Permission

@pytest.fixture
def authz_manager():
    return AuthorizationManager()

def test_check_permission_granted(authz_manager):
    # Admin role should have system admin and constitutional permissions
    roles = ['admin']
    assert authz_manager.check_permission(roles, 'system', 'admin')
    assert authz_manager.check_permission(roles, 'constitutional.data', 'read')

def test_check_permission_denied(authz_manager):
    roles = ['user']
    assert not authz_manager.check_permission(roles, 'system', 'admin')
    assert not authz_manager.check_permission(roles, 'data', 'delete')

def test_get_user_permissions(authz_manager):
    roles = ['developer']
    perms = authz_manager.get_user_permissions(roles)
    assert isinstance(perms, list)

def test_create_policy(authz_manager):
    from security.authorization import Policy, PermissionLevel
    policy = Policy(
        policy_id="test_policy",
        name="Test Policy",
        description="Test policy for testing",
        permissions=[Permission("test.resource", "read", PermissionLevel.READ)]
    )
    result = authz_manager.create_policy(policy)
    assert result is True

def test_update_policy(authz_manager):
    from security.authorization import Policy, PermissionLevel
    policy = Policy(
        policy_id="update_test",
        name="Update Test",
        description="Test policy for update",
        permissions=[Permission("test.resource", "read", PermissionLevel.READ)]
    )
    authz_manager.create_policy(policy)
    
    updated_policy = Policy(
        policy_id="update_test",
        name="Updated Test",
        description="Updated test policy",
        permissions=[Permission("test.resource", "write", PermissionLevel.WRITE)]
    )
    result = authz_manager.update_policy("update_test", updated_policy)
    assert result is True

def test_delete_policy(authz_manager):
    from security.authorization import Policy, PermissionLevel
    policy = Policy(
        policy_id="delete_test",
        name="Delete Test",
        description="Test policy for deletion",
        permissions=[Permission("test.resource", "read", PermissionLevel.READ)]
    )
    authz_manager.create_policy(policy)
    result = authz_manager.delete_policy("delete_test")
    assert result is True

def test_assign_policy_to_role(authz_manager):
    from security.authorization import Policy, PermissionLevel
    policy = Policy(
        policy_id="assign_test",
        name="Assign Test",
        description="Test policy for assignment",
        permissions=[Permission("test.resource", "read", PermissionLevel.READ)]
    )
    authz_manager.create_policy(policy)
    result = authz_manager.assign_policy_to_role("user", "assign_test")
    assert result is True

def test_get_policy(authz_manager):
    policy = authz_manager.get_policy("constitutional_programming")
    assert policy is not None
    assert policy.name == "Constitutional Programming Access"

def test_list_policies(authz_manager):
    policies = authz_manager.list_policies()
    assert isinstance(policies, list)
    assert len(policies) > 0

def test_list_role_policies(authz_manager):
    policies = authz_manager.list_role_policies("admin")
    assert isinstance(policies, list)
    assert len(policies) > 0 