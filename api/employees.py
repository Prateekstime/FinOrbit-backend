from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from dependencies import require_permissions
from models.employee import Employee

router = APIRouter()

@router.get("/")
async def get_employees(
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Admin"]))
):
    return {"message": "Employees endpoint"}