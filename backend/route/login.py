from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from schema.user import UserCreate, Login
from sqlalchemy.ext.asyncio import AsyncSession
from service.users import create_user, generate_token

router = APIRouter()

@router.post('/token')
async def fetch_token(body: Login, db:AsyncSession = Depends(get_db)):
    return await generate_token(db,body)

@router.post('/user')
async def add_user(user:UserCreate, db:AsyncSession = Depends(get_db)):
    return await create_user(db,user)