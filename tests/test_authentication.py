import pytest
from security.authentication import AuthenticationManager, UserStatus, MFAMethod

@pytest.fixture
def auth_manager():
    return AuthenticationManager()

def test_create_user(auth_manager):
    user = auth_manager.create_user('alice', 'alice@example.com', 'StrongPass123!', roles=['user'])
    assert user.username == 'alice'
    assert user.email == 'alice@example.com'
    assert user.status == UserStatus.ACTIVE

def test_duplicate_user(auth_manager):
    auth_manager.create_user('bob', 'bob@example.com', 'Passw0rd!', roles=['user'])
    with pytest.raises(ValueError):
        auth_manager.create_user('bob', 'bob2@example.com', 'Passw0rd!', roles=['user'])

def test_authenticate_success(auth_manager):
    user = auth_manager.create_user('carol', 'carol@example.com', 'Secret123!', roles=['user'])
    # Fix: Use the actual salt from password hashing
    password_hash, salt = auth_manager._hash_password('Secret123!')
    user.password_hash = password_hash
    user.mfa_secret = salt  # Store salt in mfa_secret for testing
    token = auth_manager.authenticate('carol', 'Secret123!')
    assert token is not None

def test_authenticate_fail(auth_manager):
    auth_manager.create_user('dave', 'dave@example.com', 'Secret123!', roles=['user'])
    token = auth_manager.authenticate('dave', 'WrongPass')
    assert token is None

def test_enable_mfa(auth_manager):
    auth_manager.create_user('eve', 'eve@example.com', 'Secret123!', roles=['user'])
    secret = auth_manager.enable_mfa('eve', MFAMethod.TOTP)
    user = auth_manager.get_user('eve')
    assert user.mfa_enabled
    assert user.mfa_method == MFAMethod.TOTP
    assert user.mfa_secret == secret

def test_lockout(auth_manager):
    auth_manager.create_user('frank', 'frank@example.com', 'Secret123!', roles=['user'])
    for _ in range(auth_manager.max_failed_attempts):
        auth_manager.authenticate('frank', 'WrongPass')
    user = auth_manager.get_user('frank')
    assert user.status == UserStatus.LOCKED

def test_verify_session(auth_manager):
    user = auth_manager.create_user('grace', 'grace@example.com', 'Secret123!', roles=['user'])
    # Fix: Use the actual salt from password hashing
    password_hash, salt = auth_manager._hash_password('Secret123!')
    user.password_hash = password_hash
    user.mfa_secret = salt  # Store salt in mfa_secret for testing
    token = auth_manager.authenticate('grace', 'Secret123!')
    session_info = auth_manager.verify_session(token)
    assert session_info is not None
    assert session_info['username'] == 'grace'

def test_logout(auth_manager):
    user = auth_manager.create_user('henry', 'henry@example.com', 'Secret123!', roles=['user'])
    # Fix: Use the actual salt from password hashing
    password_hash, salt = auth_manager._hash_password('Secret123!')
    user.password_hash = password_hash
    user.mfa_secret = salt  # Store salt in mfa_secret for testing
    token = auth_manager.authenticate('henry', 'Secret123!')
    result = auth_manager.logout(token)
    assert result is True

def test_update_user_roles(auth_manager):
    auth_manager.create_user('iris', 'iris@example.com', 'Secret123!', roles=['user'])
    result = auth_manager.update_user_roles('iris', ['admin'])
    assert result is True
    user = auth_manager.get_user('iris')
    assert 'admin' in user.roles

def test_delete_user(auth_manager):
    auth_manager.create_user('jack', 'jack@example.com', 'Secret123!', roles=['user'])
    result = auth_manager.delete_user('jack')
    assert result is True
    user = auth_manager.get_user('jack')
    assert user is None

def test_password_validation():
    auth_manager = AuthenticationManager()
    with pytest.raises(ValueError):
        auth_manager.create_user('short', 'short@example.com', '123', roles=['user'])

def test_user_not_found(auth_manager):
    token = auth_manager.authenticate('nonexistent', 'password')
    assert token is None 