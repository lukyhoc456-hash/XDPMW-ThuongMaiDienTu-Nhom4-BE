import jwt
import bcrypt
import hashlib

from typing import Any, Union
from app.core.config import settings
from datetime import datetime, timedelta


def create_access_token(user_id: Union[int, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    to_encode = {
        "exp": expire, "user_id": str(user_id)
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 1. Thử đối chiếu theo cơ chế bảo mật mới (SHA-256 + bcrypt)
    sha256_password = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    try:
        if bcrypt.checkpw(sha256_password.encode("utf-8"), hashed_password.encode("utf-8")):
            return True
    except Exception:
        pass

    # 2. Thử đối chiếu theo cơ chế cũ (raw bcrypt) để tương thích ngược với các tài khoản cũ trong DB
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    # Băm mật khẩu bằng SHA-256 trước để đưa độ dài về cố định 32 bytes (64 ký tự hex),
    # từ đó giải quyết triệt để lỗi giới hạn 72 bytes của bcrypt.
    sha256_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    # Sử dụng trực tiếp thư viện bcrypt native thay vì passlib để tránh lỗi AttributesError do không tương thích
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(sha256_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")
