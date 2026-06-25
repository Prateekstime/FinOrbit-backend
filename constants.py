from enum import Enum

class LoanStatus(str, Enum):
    APPLIED = "Applied"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISBURSED = "Disbursed"
    CLOSED = "Closed"
    DEFAULTED = "Defaulted"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    FAILED = "Failed"
    OVERDUE = "Overdue"
    PARTIAL = "Partial"

class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    WHATSAPP = "WHATSAPP"

class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    READ = "READ"

class UserRole(str, Enum):
    BRANCH_MANAGER = "Branch Manager"
    LOAN_OFFICER = "Loan Officer"
    RELATIONSHIP_MANAGER = "Relationship Manager"
    CREDIT_ANALYST = "Credit Analyst"
    COLLECTION_OFFICER = "Collection Officer"
    ADMIN = "Admin"

class DocumentType(str, Enum):
    AADHAAR = "Aadhaar"
    PAN = "PAN"
    PASSPORT = "Passport"
    DRIVING_LICENSE = "Driving License"
    SALARY_SLIP = "Salary Slip"
    BANK_STATEMENT = "Bank Statement"
    PHOTO = "Photo"
    ELECTRICITY_BILL = "Electricity Bill"
    RENTAL_AGREEMENT = "Rental Agreement"

class EmploymentType(str, Enum):
    SALARIED = "Salaried"
    SELF_EMPLOYED = "Self Employed"
    BUSINESS = "Business"
    GOVERNMENT_EMPLOYEE = "Government Employee"
    PRIVATE_EMPLOYEE = "Private Employee"
    STUDENT = "Student"
    RETIRED = "Retired"

class RelationshipType(str, Enum):
    FATHER = "Father"
    MOTHER = "Mother"
    BROTHER = "Brother"
    SISTER = "Sister"
    SPOUSE = "Spouse"
    SON = "Son"
    DAUGHTER = "Daughter"
    FRIEND = "Friend"
    RELATIVE = "Relative"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"

class PaymentMode(str, Enum):
    CASH = "Cash"
    CHEQUE = "Cheque"
    NEFT = "NEFT"
    RTGS = "RTGS"
    IMPS = "IMPS"
    UPI = "UPI"
    BANK_TRANSFER = "Bank Transfer"

# API Response Constants
SUCCESS_MESSAGE = "Success"
ERROR_MESSAGE = "Error"
UNAUTHORIZED_MESSAGE = "Unauthorized access"
FORBIDDEN_MESSAGE = "Access forbidden"
NOT_FOUND_MESSAGE = "Resource not found"
VALIDATION_ERROR_MESSAGE = "Validation error"
INTERNAL_ERROR_MESSAGE = "Internal server error"

# Database Constants
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_PAGE = 1

# File Upload Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
ALLOWED_DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xlsx", ".txt"]

# Cache Constants
CACHE_TTL = 300  # 5 minutes
CACHE_PREFIX = "lendcore"

# Report Constants
REPORT_OUTPUT_DIR = "reports"
REPORT_FORMATS = ["PDF", "EXCEL", "CSV", "JSON"]