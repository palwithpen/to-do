# api/task.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schema.tasks import TaskCreate, TaskUpdate, TaskResponse
from service.tasks import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task,
    bulk_update_tasks,
    bulk_delete_tasks
)
from db.session import get_db
from utils.jwt import get_current_user
from utils.common_utils import API_RESPONSE

router = APIRouter()

@router.post("/")
async def create_task_endpoint(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_task(db, task, owner_id=current_user.username)

@router.get("/{task_id}")
async def get_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task(db, task_id)
    if not task or task.owner_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=API_RESPONSE("TASK_NOT_FOUND",404))
    return task

@router.get("/", response_model=List[TaskResponse])
async def get_tasks_endpoint(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_tasks(db, owner_id=current_user.username)

@router.put("/{task_id}")
async def update_task_endpoint(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task(db, task_id)
    if not task or task.owner_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=API_RESPONSE("TASK_NOT_FOUND",404))
    return await update_task(db, task_id, task_update)

@router.delete("/{task_id}")
async def delete_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task(db, task_id)
    if not task or task.owner_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=API_RESPONSE("TASK_NOT_FOUND",404))
    return await delete_task(db, task_id)
    

@router.put("/bulk_update", response_model=dict)
async def bulk_update_tasks_endpoint(tasks: List[TaskUpdate], db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    for task in tasks:
        existing_task = await get_task(db, task.id)
        if not existing_task or existing_task.owner_id != current_user.username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=API_RESPONSE("TASK_NOT_FOUND",404))
    return await bulk_update_tasks(db, tasks)

@router.delete("/bulk_delete", response_model=dict)
async def bulk_delete_tasks_endpoint(task_ids: List[int], db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    for task_id in task_ids:
        task = await get_task(db, task_id)
        if not task or task.owner_id != current_user.username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=API_RESPONSE("TASK_NOT_FOUND",404))
    return await bulk_delete_tasks(db, task_ids)
