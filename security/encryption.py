"""
REM-CODE Encryption Manager
End-to-end encryption and key management for enterprise security
"""

import base64
import hashlib
import secrets
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms"""
    AES_256_GCM = "aes-256-gcm"
    AES_256_CBC = "aes-256-cbc"
    CHACHA20_POLY1305 = "chacha20-poly1305"

class KeyType(Enum):
    """Key types for different purposes"""
    DATA_ENCRYPTION = "data_encryption"
    COMMUNICATION = "communication"
    SIGNING = "signing"
    MASTER = "master"

@dataclass
class EncryptionKey:
    """Encryption key information"""
    key_id: str
    key_type: KeyType
    algorithm: EncryptionAlgorithm
    key_data: bytes
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EncryptedData:
    """Encrypted data structure"""
    data: bytes
    iv: bytes
    algorithm: EncryptionAlgorithm
    key_id: str
    tag: Optional[bytes] = None
    encrypted_at: float = field(default_factory=time.time)

class EncryptionManager:
    """
    Manages encryption and decryption operations
    """
    
    def __init__(self, master_key: Optional[bytes] = None):
        """Initialize encryption manager"""
        self.master_key = master_key or secrets.token_bytes(32)
        self.keys: Dict[str, EncryptionKey] = {}
        self.key_rotation_interval = 86400 * 30  # 30 days
        
        # Initialize default keys
        self._initialize_default_keys()
        
        logger.info("🔐 Encryption Manager initialized")
    
    def _initialize_default_keys(self):
        """Initialize default encryption keys"""
        # Data encryption key
        data_key = EncryptionKey(
            key_id="data_encryption_key",
            key_type=KeyType.DATA_ENCRYPTION,
            algorithm=EncryptionAlgorithm.AES_256_GCM,
            key_data=secrets.token_bytes(32),
            expires_at=time.time() + self.key_rotation_interval
        )
        
        # Communication key
        comm_key = EncryptionKey(
            key_id="communication_key",
            key_type=KeyType.COMMUNICATION,
            algorithm=EncryptionAlgorithm.CHACHA20_POLY1305,
            key_data=secrets.token_bytes(32),
            expires_at=time.time() + self.key_rotation_interval
        )
        
        # Signing key
        signing_key = EncryptionKey(
            key_id="signing_key",
            key_type=KeyType.SIGNING,
            algorithm=EncryptionAlgorithm.AES_256_GCM,
            key_data=secrets.token_bytes(32),
            expires_at=time.time() + self.key_rotation_interval
        )
        
        self.keys[data_key.key_id] = data_key
        self.keys[comm_key.key_id] = comm_key
        self.keys[signing_key.key_id] = signing_key
    
    def encrypt_data(self, data: Union[str, bytes], key_id: str = "data_encryption_key") -> EncryptedData:
        """
        Encrypt data using specified key
        
        Args:
            data: Data to encrypt
            key_id: Key ID to use for encryption
            
        Returns:
            EncryptedData: Encrypted data structure
        """
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        key = self.keys[key_id]
        
        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate IV
        iv = secrets.token_bytes(16)
        
        # Encrypt data
        encrypted_data, tag = self._encrypt_with_algorithm(data, key.key_data, iv, key.algorithm)
        
        return EncryptedData(
            data=encrypted_data,
            iv=iv,
            tag=tag,
            algorithm=key.algorithm,
            key_id=key_id
        )
    
    def decrypt_data(self, encrypted_data: EncryptedData) -> bytes:
        """
        Decrypt data using the key specified in encrypted_data
        
        Args:
            encrypted_data: EncryptedData structure
            
        Returns:
            bytes: Decrypted data
        """
        if encrypted_data.key_id not in self.keys:
            raise ValueError(f"Key {encrypted_data.key_id} not found")
        
        key = self.keys[encrypted_data.key_id]
        
        # Decrypt data
        decrypted_data = self._decrypt_with_algorithm(
            encrypted_data.data,
            key.key_data,
            encrypted_data.iv,
            encrypted_data.tag,
            encrypted_data.algorithm
        )
        
        return decrypted_data
    
    def _encrypt_with_algorithm(self, data: bytes, key: bytes, iv: bytes, 
                               algorithm: EncryptionAlgorithm) -> tuple[bytes, Optional[bytes]]:
        """Encrypt data with specified algorithm"""
        try:
            if algorithm == EncryptionAlgorithm.AES_256_GCM:
                return self._encrypt_aes_256_gcm(data, key, iv)
            elif algorithm == EncryptionAlgorithm.AES_256_CBC:
                return self._encrypt_aes_256_cbc(data, key, iv)
            elif algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
                return self._encrypt_chacha20_poly1305(data, key, iv)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def _decrypt_with_algorithm(self, data: bytes, key: bytes, iv: bytes, 
                               tag: Optional[bytes], algorithm: EncryptionAlgorithm) -> bytes:
        """Decrypt data with specified algorithm"""
        try:
            if algorithm == EncryptionAlgorithm.AES_256_GCM:
                return self._decrypt_aes_256_gcm(data, key, iv, tag)
            elif algorithm == EncryptionAlgorithm.AES_256_CBC:
                return self._decrypt_aes_256_cbc(data, key, iv)
            elif algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
                return self._decrypt_chacha20_poly1305(data, key, iv, tag)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def _encrypt_aes_256_gcm(self, data: bytes, key: bytes, iv: bytes) -> tuple[bytes, bytes]:
        """Encrypt using AES-256-GCM"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(iv, data, None)
            return ciphertext, b""  # Tag is included in ciphertext
        except ImportError:
            logger.error("cryptography library not available for AES-256-GCM")
            raise
    
    def _decrypt_aes_256_gcm(self, data: bytes, key: bytes, iv: bytes, tag: Optional[bytes]) -> bytes:
        """Decrypt using AES-256-GCM"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(iv, data, None)
            return plaintext
        except ImportError:
            logger.error("cryptography library not available for AES-256-GCM")
            raise
    
    def _encrypt_aes_256_cbc(self, data: bytes, key: bytes, iv: bytes) -> tuple[bytes, None]:
        """Encrypt using AES-256-CBC"""
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives import padding
            
            # Pad data
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            
            # Encrypt
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            return ciphertext, None
        except ImportError:
            logger.error("cryptography library not available for AES-256-CBC")
            raise
    
    def _decrypt_aes_256_cbc(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt using AES-256-CBC"""
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives import padding
            
            # Decrypt
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(data) + decryptor.finalize()
            
            # Unpad
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_data) + unpadder.finalize()
            
            return plaintext
        except ImportError:
            logger.error("cryptography library not available for AES-256-CBC")
            raise
    
    def _encrypt_chacha20_poly1305(self, data: bytes, key: bytes, iv: bytes) -> tuple[bytes, bytes]:
        """Encrypt using ChaCha20-Poly1305"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
            chacha = ChaCha20Poly1305(key)
            ciphertext = chacha.encrypt(iv, data, None)
            return ciphertext, b""  # Tag is included in ciphertext
        except ImportError:
            logger.error("cryptography library not available for ChaCha20-Poly1305")
            raise
    
    def _decrypt_chacha20_poly1305(self, data: bytes, key: bytes, iv: bytes, tag: Optional[bytes]) -> bytes:
        """Decrypt using ChaCha20-Poly1305"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
            chacha = ChaCha20Poly1305(key)
            plaintext = chacha.decrypt(iv, data, None)
            return plaintext
        except ImportError:
            logger.error("cryptography library not available for ChaCha20-Poly1305")
            raise
    
    def create_key(self, key_id: str, key_type: KeyType, 
                   algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM) -> EncryptionKey:
        """Create a new encryption key"""
        if key_id in self.keys:
            raise ValueError(f"Key {key_id} already exists")
        
        key = EncryptionKey(
            key_id=key_id,
            key_type=key_type,
            algorithm=algorithm,
            key_data=secrets.token_bytes(32),
            expires_at=time.time() + self.key_rotation_interval
        )
        
        self.keys[key_id] = key
        logger.info(f"🔑 Created key: {key_id}")
        return key
    
    def rotate_key(self, key_id: str) -> bool:
        """Rotate encryption key"""
        if key_id not in self.keys:
            logger.warning(f"Key {key_id} not found")
            return False
        
        old_key = self.keys[key_id]
        
        # Create new key
        new_key = EncryptionKey(
            key_id=f"{key_id}_rotated_{int(time.time())}",
            key_type=old_key.key_type,
            algorithm=old_key.algorithm,
            key_data=secrets.token_bytes(32),
            expires_at=time.time() + self.key_rotation_interval
        )
        
        self.keys[new_key.key_id] = new_key
        logger.info(f"🔄 Rotated key: {key_id} -> {new_key.key_id}")
        return True
    
    def delete_key(self, key_id: str) -> bool:
        """Delete encryption key"""
        if key_id in self.keys:
            del self.keys[key_id]
            logger.info(f"🗑️ Deleted key: {key_id}")
            return True
        return False
    
    def get_key(self, key_id: str) -> Optional[EncryptionKey]:
        """Get key by ID"""
        return self.keys.get(key_id)
    
    def list_keys(self) -> List[EncryptionKey]:
        """List all keys"""
        return list(self.keys.values())
    
    def export_key(self, key_id: str) -> str:
        """Export key as base64 string"""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        key = self.keys[key_id]
        key_data = {
            "key_id": key.key_id,
            "key_type": key.key_type.value,
            "algorithm": key.algorithm.value,
            "key_data": base64.b64encode(key.key_data).decode('utf-8'),
            "created_at": key.created_at,
            "expires_at": key.expires_at
        }
        
        return base64.b64encode(str(key_data).encode('utf-8')).decode('utf-8')
    
    def import_key(self, key_data: str) -> bool:
        """Import key from base64 string"""
        try:
            import json
            decoded_data = base64.b64decode(key_data).decode('utf-8')
            key_info = eval(decoded_data)  # In production, use json.loads
            
            key = EncryptionKey(
                key_id=key_info["key_id"],
                key_type=KeyType(key_info["key_type"]),
                algorithm=EncryptionAlgorithm(key_info["algorithm"]),
                key_data=base64.b64decode(key_info["key_data"]),
                created_at=key_info["created_at"],
                expires_at=key_info["expires_at"]
            )
            
            self.keys[key.key_id] = key
            logger.info(f"📥 Imported key: {key.key_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to import key: {e}")
            return False

class KeyManager:
    """
    Manages key lifecycle and rotation
    """
    
    def __init__(self, encryption_manager: EncryptionManager):
        """Initialize key manager"""
        self.encryption_manager = encryption_manager
        self.rotation_schedule: Dict[str, float] = {}
        
        logger.info("🔑 Key Manager initialized")
    
    def schedule_key_rotation(self, key_id: str, rotation_interval: float = 86400 * 30):
        """Schedule key rotation"""
        self.rotation_schedule[key_id] = time.time() + rotation_interval
        logger.info(f"📅 Scheduled key rotation for {key_id}")
    
    def check_key_expiration(self) -> List[str]:
        """Check for expired keys"""
        expired_keys = []
        current_time = time.time()
        
        for key_id, key in self.encryption_manager.keys.items():
            if key.expires_at and current_time > key.expires_at:
                expired_keys.append(key_id)
        
        return expired_keys
    
    def rotate_expired_keys(self) -> List[str]:
        """Rotate all expired keys"""
        expired_keys = self.check_key_expiration()
        rotated_keys = []
        
        for key_id in expired_keys:
            if self.encryption_manager.rotate_key(key_id):
                rotated_keys.append(key_id)
        
        return rotated_keys
    
    def backup_keys(self) -> Dict[str, str]:
        """Backup all keys"""
        backup = {}
        for key_id in self.encryption_manager.keys:
            backup[key_id] = self.encryption_manager.export_key(key_id)
        
        logger.info(f"💾 Backed up {len(backup)} keys")
        return backup
    
    def restore_keys(self, backup: Dict[str, str]) -> int:
        """Restore keys from backup"""
        restored_count = 0
        
        for key_id, key_data in backup.items():
            if self.encryption_manager.import_key(key_data):
                restored_count += 1
        
        logger.info(f"📥 Restored {restored_count} keys")
        return restored_count 