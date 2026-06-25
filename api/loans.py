from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.loan import LoanCreate, LoanResponse, LoanUpdate, LoanApplicationResponse
from services.loan_service import LoanService
from dependencies import require_permissions
from models.employee import Employee

router = APIRouter()

@router.get("/", response_model=List[LoanResponse])
async def get_loans(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    status_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Loan Officer", "Admin"]))
):
    """
    Get all loans with filters
    """
    service = LoanService(db)
    loans = await service.get_loans(skip=skip, limit=limit, customer_id=customer_id, status_id=status_id)
    return loans

@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Loan Officer", "Admin"]))
):
    """
    Get loan by ID
    """
    service = LoanService(db)
    loan = await service.get_loan_by_id(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan

@router.post("/apply", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_loan(
    loan_data: LoanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Loan Officer", "Relationship Manager", "Admin"]))
):
    """
    Apply for a new loan
    """
    service = LoanService(db)
    application = await service.apply_for_loan(loan_data, current_user.employee_id)
    return application

@router.put("/{loan_id}/approve", response_model=LoanResponse)
async def approve_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Admin"]))
):
    """
    Approve a loan application
    """
    service = LoanService(db)
    loan = await service.approve_loan(loan_id, current_user.employee_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan

@router.put("/{loan_id}/reject", response_model=LoanResponse)
async def reject_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Admin"]))
):
    """
    Reject a loan application
    """
    service = LoanService(db)
    loan = await service.reject_loan(loan_id, current_user.employee_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan

@router.post("/{loan_id}/disburse", response_model=LoanResponse)
async def disburse_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Employee = Depends(require_permissions(["Branch Manager", "Admin"]))
):
    """
    Disburse an approved loan
    """
    service = LoanService(db)
    loan = await service.disburse_loan(loan_id, current_user.employee_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan