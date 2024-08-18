from schema.user import UserCreate, Login
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from utils.jwt import get_password_hash, create_access_token, verify_password
from utils.common_utils import API_RESPONSE
from datetime import timedelta
import uuid

ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_user(db: AsyncSession, user: UserCreate):
    try:
        """
            - Check if user exists
            - if not then add a user to DB
        """
        result = await db.execute(select(User).filter(User.username == user.username))
        user_count = result.scalars().all()
        user_exists = len(user_count) > 0

        if not user_exists:
            db_user = User(
                id=str(uuid.uuid4()),
                username=user.username,
                hashed_password=get_password_hash(user.password),
                email=user.email
            )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return API_RESPONSE(status="USER_ADDED_SUCCESSFULLY", statusCode=201)
        
        return API_RESPONSE(status="USER_ALREADY_EXISTS", statusCode=400)

    except Exception as e:
        return API_RESPONSE(status="EXCEPTION_OCCURRED", statusCode=500, data=str(e))

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def verify_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def generate_token(db: AsyncSession, body:Login):
    user = await verify_user(db, body.username, body.password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return API_RESPONSE(
            status="LOGIN_SUCCESSFUL",
            statusCode=200,
            data={"access_token": access_token, "token_type": "bearer"}
        )
    return API_RESPONSE(status="INVALID_CREDENTIALS", statusCode=400)
