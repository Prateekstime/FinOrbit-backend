from fastapi import APIRouter

# Use relative imports or imports from the project root
from api.auth import routes as auth_routes
from api.customers import customer_routes
from api.loans import  loan_routes
from api.repayments import  repayment_routes
from api.branches import routes as branch_routes
from api.employees import routes as employee_routes
from api.guarantors import routes as guarantor_routes
from api.collateral import routes as collateral_routes
from api.documents import routes as document_routes
from api.notifications import routes as notification_routes
from api.reports import routes as report_routes
from api.dashboard import routes as dashboard_routes

router = APIRouter()

# Auth routes
router.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Customer routes
router.include_router(
    customer_routes.router,
    prefix="/customers",
    tags=["Customers"]
)

# Branch routes
router.include_router(
    branch_routes.router,
    prefix="/branches",
    tags=["Branches"]
)

# Employee routes
router.include_router(
    employee_routes.router,
    prefix="/employees",
    tags=["Employees"]
)

# Loan routes
router.include_router(
    loan_routes.router,
    prefix="/loans",
    tags=["Loans"]
)

# Repayment routes
router.include_router(
    repayment_routes.router,
    prefix="/repayments",
    tags=["Repayments"]
)

# Guarantor routes
router.include_router(
    guarantor_routes.router,
    prefix="/guarantors",
    tags=["Guarantors"]
)

# Collateral routes
router.include_router(
    collateral_routes.router,
    prefix="/collateral",
    tags=["Collateral"]
)

# Document routes
router.include_router(
    document_routes.router,
    prefix="/documents",
    tags=["Documents"]
)

# Notification routes
router.include_router(
    notification_routes.router,
    prefix="/notifications",
    tags=["Notifications"]
)

# Report routes
router.include_router(
    report_routes.router,
    prefix="/reports",
    tags=["Reports"]
)

# Dashboard routes
router.include_router(
    dashboard_routes.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)