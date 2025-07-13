import pytest
from security.encryption import EncryptionManager, EncryptionAlgorithm, KeyType

@pytest.fixture
def enc_manager():
    return EncryptionManager()

def test_encrypt_decrypt(enc_manager):
    data = "secret data"
    encrypted = enc_manager.encrypt_data(data)
    decrypted = enc_manager.decrypt_data(encrypted)
    assert decrypted.decode('utf-8') == data

def test_create_key(enc_manager):
    key = enc_manager.create_key('test_key', KeyType.DATA_ENCRYPTION)
    assert key.key_id == 'test_key'
    assert key.key_type == KeyType.DATA_ENCRYPTION
    assert key.algorithm == EncryptionAlgorithm.AES_256_GCM

def test_list_keys(enc_manager):
    keys = enc_manager.list_keys() if hasattr(enc_manager, 'list_keys') else list(enc_manager.keys.values())
    assert isinstance(keys, list)

def test_get_key(enc_manager):
    key = enc_manager.get_key('data_encryption_key')
    assert key is not None
    assert key.key_id == 'data_encryption_key'

def test_rotate_key(enc_manager):
    result = enc_manager.rotate_key('data_encryption_key')
    assert result is True

def test_delete_key(enc_manager):
    # Create a test key first
    enc_manager.create_key('delete_test', KeyType.DATA_ENCRYPTION)
    result = enc_manager.delete_key('delete_test')
    assert result is True

def test_export_key(enc_manager):
    exported = enc_manager.export_key('data_encryption_key')
    assert isinstance(exported, str)
    assert len(exported) > 0

def test_import_key(enc_manager):
    # Export a key first
    exported = enc_manager.export_key('data_encryption_key')
    result = enc_manager.import_key(exported)
    assert result is True

def test_encrypt_with_specific_key(enc_manager):
    # Create a specific key
    enc_manager.create_key('specific_key', KeyType.DATA_ENCRYPTION)
    data = "test data"
    encrypted = enc_manager.encrypt_data(data, 'specific_key')
    decrypted = enc_manager.decrypt_data(encrypted)
    assert decrypted.decode('utf-8') == data

def test_key_not_found():
    enc_manager = EncryptionManager()
    with pytest.raises(ValueError):
        enc_manager.encrypt_data("data", "nonexistent_key") 