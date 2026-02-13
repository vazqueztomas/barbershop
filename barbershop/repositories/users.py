from datetime import datetime, timedelta
from uuid import UUID, uuid4
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
import os

from barbershop.models import User, UserCreate, UserBase
from .handler_errors import NotFoundResponse

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
PASSWORD_RESET_EXPIRE_MINUTES = 60  # 1 hour

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, connection):
        self.connection = connection
        self._ensure_users_table()

    def _ensure_users_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                full_name VARCHAR(255),
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                password_reset_token VARCHAR(255),
                password_reset_expires TIMESTAMP
            )
        """)
        self.connection.commit()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_user(self, user_data: UserCreate) -> User:
        cursor = self.connection.cursor()
        user_id = uuid4()
        hashed_password = self.get_password_hash(user_data.password)
        
        cursor.execute(
            """INSERT INTO users (id, email, username, full_name, hashed_password, is_active)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
            (str(user_id), user_data.email, user_data.username, 
             user_data.full_name, hashed_password, True)
        )
        self.connection.commit()
        row = cursor.fetchone()
        return self._row_to_user(row)

    def _row_to_user(self, row) -> User:
        return User(
            id=UUID(row["id"]),
            email=row["email"],
            username=row["username"],
            full_name=row["full_name"],
            hashed_password=row["hashed_password"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def get_user_by_username(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def get_user_by_email(self, email: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def get_user_by_id(self, user_id: UUID) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
        row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_password_reset_token(self, email: str) -> str | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        
        reset_token = secrets.token_urlsafe(32)
        expires = datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
        
        cursor.execute(
            """UPDATE users SET password_reset_token = %s, password_reset_expires = %s 
               WHERE email = %s""",
            (reset_token, expires, email)
        )
        self.connection.commit()
        return reset_token

    def reset_password(self, token: str, new_password: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT id FROM users WHERE password_reset_token = %s 
               AND password_reset_expires > CURRENT_TIMESTAMP""",
            (token,)
        )
        row = cursor.fetchone()
        if not row:
            return False
        
        hashed_password = self.get_password_hash(new_password)
        cursor.execute(
            """UPDATE users SET hashed_password = %s, password_reset_token = NULL, 
               password_reset_expires = NULL WHERE id = %s""",
            (hashed_password, row["id"])
        )
        self.connection.commit()
        return True

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
