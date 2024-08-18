from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from db.models import Task
from schema.tasks import TaskCreate, TaskUpdate
from typing import List
from utils.common_utils import API_RESPONSE

async def create_task(db: AsyncSession, task: TaskCreate, owner_id: str):
    new_task = Task(**task.dict(), owner_id=owner_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return API_RESPONSE("TASK_ADDED_SUCCESSFULLY",200,new_task)
    

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()

async def get_tasks(db: AsyncSession, owner_id: str):
    result = await db.execute(select(Task).filter(Task.owner_id == owner_id))
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate):
    try:
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(**task_update.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()
        return API_RESPONSE("UPDATED_SUCCESSFULLY",200)
    except Exception as e:
        return API_RESPONSE("EXCEPTION_OCCURRED",500,str(e))

async def delete_task(db: AsyncSession, task_id: int):
    try:
        query = delete(Task).where(Task.id == task_id)
        await db.execute(query)
        await db.commit()

        return API_RESPONSE("DELETED_SUCCESSFULLY",200)
    except Exception as e:
        return API_RESPONSE("EXCEPTION_OCCURRED",500,str(e))

async def bulk_update_tasks(db: AsyncSession, tasks: List[TaskUpdate]):
    for task in tasks:
        await update_task(db, task.id, task)
    return {"status": "Bulk update successful"}

async def bulk_delete_tasks(db: AsyncSession, task_ids: List[int]):
    query = delete(Task).where(Task.id.in_(task_ids))
    await db.execute(query)
    await db.commit()
    return {"status": "Bulk delete successful"}
