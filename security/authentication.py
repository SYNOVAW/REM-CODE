"""
REM-CODE Authentication Manager
Multi-factor authentication and user management for enterprise security
"""

import hashlib
import secrets
import time
import jwt
import hmac  # ← 追加
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class UserStatus(Enum):
    """User account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    LOCKED = "locked"
    PENDING = "pending"

class MFAMethod(Enum):
    """Multi-factor authentication methods"""
    TOTP = "totp"  # Time-based One-Time Password
    SMS = "sms"     # SMS verification
    EMAIL = "email" # Email verification
    HARDWARE = "hardware" # Hardware token

@dataclass
class User:
    """User account information"""
    user_id: str
    username: str
    email: str
    password_hash: str
    roles: List[str] = field(default_factory=list)
    status: UserStatus = UserStatus.PENDING
    created_at: float = field(default_factory=time.time)
    last_login: Optional[float] = None
    mfa_enabled: bool = False
    mfa_method: Optional[MFAMethod] = None
    mfa_secret: Optional[str] = None
    failed_attempts: int = 0
    locked_until: Optional[float] = None

@dataclass
class Role:
    """Role definition with permissions"""
    role_id: str
    name: str
    description: str
    permissions: List[str] = field(default_factory=list)
    constitutional_level: Optional[str] = None

class AuthenticationManager:
    """
    Manages user authentication and multi-factor authentication
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """Initialize authentication manager"""
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.max_failed_attempts = 5
        self.lockout_duration = 1800  # 30 minutes
        
        # Initialize default roles
        self._initialize_default_roles()
        
        logger.info("🔐 Authentication Manager initialized")
    
    def _initialize_default_roles(self):
        """Initialize default roles for constitutional programming"""
        default_roles = {
            "admin": Role(
                role_id="admin",
                name="Administrator",
                description="Full system access",
                permissions=["*"],
                constitutional_level="Emergency"
            ),
            "developer": Role(
                role_id="developer", 
                name="Developer",
                description="Development and testing access",
                permissions=["read", "write", "execute", "test"],
                constitutional_level="Constitutional"
            ),
            "user": Role(
                role_id="user",
                name="User", 
                description="Basic user access",
                permissions=["read", "execute"],
                constitutional_level="General"
            ),
            "viewer": Role(
                role_id="viewer",
                name="Viewer",
                description="Read-only access",
                permissions=["read"],
                constitutional_level="General"
            )
        }
        
        for role in default_roles.values():
            self.roles[role.role_id] = role
    
    def _hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 for password hashing
        import hashlib
        import hmac
        
        # Generate key using PBKDF2
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100k iterations
        )
        
        return key.hex(), salt
    
    def _verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        expected_hash, _ = self._hash_password(password, salt)
        return hmac.compare_digest(password_hash, expected_hash)
    
    def create_user(self, username: str, email: str, password: str, 
                    roles: List[str] = None) -> User:
        """Create a new user account"""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        password_hash, salt = self._hash_password(password)
        
        user = User(
            user_id=secrets.token_urlsafe(16),
            username=username,
            email=email,
            password_hash=password_hash,
            roles=roles or ["user"],
            status=UserStatus.ACTIVE
        )
        
        self.users[username] = user
        logger.info(f"👤 Created user: {username}")
        return user
    
    def authenticate(self, username: str, password: str, 
                    mfa_code: Optional[str] = None) -> Optional[str]:
        """Authenticate user and return session token"""
        if username not in self.users:
            logger.warning(f"❌ Authentication failed: User {username} not found")
            return None
        
        user = self.users[username]
        
        # Check if account is locked
        if user.status == UserStatus.LOCKED:
            if user.locked_until and time.time() < user.locked_until:
                logger.warning(f"🔒 Account locked: {username}")
                return None
            else:
                # Unlock account
                user.status = UserStatus.ACTIVE
                user.failed_attempts = 0
                user.locked_until = None
        
        # Verify password
        if not self._verify_password(password, user.password_hash, user.mfa_secret or ""):
            user.failed_attempts += 1
            
            if user.failed_attempts >= self.max_failed_attempts:
                user.status = UserStatus.LOCKED
                user.locked_until = time.time() + self.lockout_duration
                logger.warning(f"🔒 Account locked due to failed attempts: {username}")
            else:
                logger.warning(f"❌ Failed login attempt: {username}")
            
            return None
        
        # Verify MFA if enabled
        if user.mfa_enabled and user.mfa_method:
            if not mfa_code:
                logger.warning(f"❌ MFA code required: {username}")
                return None
            
            if not self._verify_mfa(user, mfa_code):
                logger.warning(f"❌ Invalid MFA code: {username}")
                return None
        
        # Reset failed attempts on successful login
        user.failed_attempts = 0
        user.last_login = time.time()
        
        # Generate session token
        session_token = self._generate_session_token(user)
        self.sessions[session_token] = {
            "user_id": user.user_id,
            "username": user.username,
            "roles": user.roles,
            "created_at": time.time(),
            "expires_at": time.time() + 3600  # 1 hour
        }
        
        logger.info(f"✅ User authenticated: {username}")
        return session_token
    
    def _verify_mfa(self, user: User, mfa_code: str) -> bool:
        """Verify MFA code"""
        if user.mfa_method == MFAMethod.TOTP:
            return self._verify_totp(user.mfa_secret, mfa_code)
        elif user.mfa_method == MFAMethod.SMS:
            return self._verify_sms_code(user, mfa_code)
        elif user.mfa_method == MFAMethod.EMAIL:
            return self._verify_email_code(user, mfa_code)
        
        return False
    
    def _verify_totp(self, secret: str, code: str) -> bool:
        """Verify TOTP code"""
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(code)
        except ImportError:
            logger.error("pyotp library not available for TOTP verification")
            return False
    
    def _verify_sms_code(self, user: User, code: str) -> bool:
        """Verify SMS code (placeholder)"""
        # In production, integrate with SMS service
        return code == "123456"  # Placeholder
    
    def _verify_email_code(self, user: User, code: str) -> bool:
        """Verify email code (placeholder)"""
        # In production, integrate with email service
        return code == "123456"  # Placeholder
    
    def _generate_session_token(self, user: User) -> str:
        """Generate JWT session token"""
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "roles": user.roles,
            "exp": time.time() + 3600  # 1 hour expiration
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verify_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Verify session token and return user info"""
        try:
            payload = jwt.decode(session_token, self.secret_key, algorithms=["HS256"])
            
            # Check if session exists in memory
            if session_token in self.sessions:
                session = self.sessions[session_token]
                if time.time() < session["expires_at"]:
                    return session
            
            return None
        except jwt.InvalidTokenError:
            return None
    
    def enable_mfa(self, username: str, method: MFAMethod) -> str:
        """Enable MFA for user and return secret"""
        if username not in self.users:
            raise ValueError(f"User {username} not found")
        
        user = self.users[username]
        
        if method == MFAMethod.TOTP:
            import pyotp
            secret = pyotp.random_base32()
            user.mfa_secret = secret
            user.mfa_method = method
            user.mfa_enabled = True
            
            logger.info(f"🔐 MFA enabled for {username}: {method.value}")
            return secret
        else:
            # For SMS/Email, generate temporary code
            user.mfa_method = method
            user.mfa_enabled = True
            logger.info(f"🔐 MFA enabled for {username}: {method.value}")
            return "123456"  # Placeholder
    
    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        if session_token in self.sessions:
            del self.sessions[session_token]
            logger.info("👋 User logged out")
            return True
        return False
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)
    
    def update_user_roles(self, username: str, roles: List[str]) -> bool:
        """Update user roles"""
        if username not in self.users:
            return False
        
        self.users[username].roles = roles
        logger.info(f"👤 Updated roles for {username}: {roles}")
        return True
    
    def delete_user(self, username: str) -> bool:
        """Delete user account"""
        if username in self.users:
            del self.users[username]
            logger.info(f"🗑️ Deleted user: {username}")
            return True
        return False 