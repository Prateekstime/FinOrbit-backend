from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from services.customer_service import CustomerService
from dependencies import get_current_active_user, require_permissions
from models.employee import Employee

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Loan Officer", "Admin"]))
):
    """
    Get all customers with pagination
    """
    service = CustomerService(db)
    customers = await service.get_customers(skip=skip, limit=limit, search=search)
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Loan Officer", "Admin"]))
):
    """
    Get customer by ID
    """
    service = CustomerService(db)
    customer = await service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Loan Officer", "Admin"]))
):
    """
    Create a new customer
    """
    service = CustomerService(db)
    customer = await service.create_customer(customer_data)
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Admin"]))
):
    """
    Update customer details
    """
    service = CustomerService(db)
    customer = await service.update_customer(customer_id, customer_data)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Admin"]))
):
    """
    Delete a customer
    """
    service = CustomerService(db)
    deleted = await service.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return None