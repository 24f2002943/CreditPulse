from datetime import datetime, timedelta
from typing import Optional, Union, Any
import hashlib
import secrets
from jose import jwt
from backend.app.core.config import settings

def get_password_hash(password: str) -> str:
    """Secure salted SHA-256 hash."""
    salt = secrets.token_hex(8)
    pw_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${pw_hash}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if "$" not in hashed_password:
        return False
    salt, original_hash = hashed_password.split("$", 1)
    test_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
    return secrets.compare_digest(original_hash, test_hash)

def create_access_token(subject: Union[str, Any], role: str, company_id: Optional[int] = None, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "company_id": company_id
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
