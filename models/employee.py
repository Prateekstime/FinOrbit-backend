from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Date, Numeric, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List

from database.base import Base, TimestampMixin, SoftDeleteMixin


class Employee(Base, TimestampMixin, SoftDeleteMixin):
    """
    Employee Model - Stores employee information
    """
    __tablename__ = "employees"
    __table_args__ = {"schema": "loan_mgmt_schema"}

    employee_id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_code = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), unique=True, nullable=True, index=True)
    designation = Column(String(100))

    # Foreign Keys
    branch_id = Column(BigInteger, ForeignKey("loan_mgmt_schema.branches.branch_id"), nullable=False)
    role_id = Column(BigInteger, ForeignKey("loan_mgmt_schema.employee_roles.role_id"), nullable=False)

    # Employee details
    joining_date = Column(Date)
    salary = Column(Numeric(12, 2))
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    branch = relationship("Branch", back_populates="employees")
    role = relationship("EmployeeRole", back_populates="employees")

    # One-to-Many relationships
    loan_applications_assigned = relationship(
        "LoanApplication",
        foreign_keys="LoanApplication.assigned_employee_id",
        back_populates="assigned_employee"
    )
    loan_disbursements = relationship(
        "LoanDisbursement",
        foreign_keys="LoanDisbursement.disbursed_by",
        back_populates="disbursed_by_employee"
    )
    loan_verifications = relationship(
        "LoanVerification",
        foreign_keys="LoanVerification.conducted_by",
        back_populates="conducted_by_employee"
    )
    audit_logs = relationship(
        "AuditLog",
        foreign_keys="AuditLog.performed_by",
        back_populates="employee"
    )
    notifications_sent = relationship(
        "Notification",
        foreign_keys="Notification.sent_by",
        back_populates="sender"
    )

    def __repr__(self):
        return f"<Employee {self.employee_code} - {self.first_name} {self.last_name or ''}>"

    @property
    def full_name(self) -> str:
        """Get full name of employee"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def display_name(self) -> str:
        """Get display name with employee code"""
        return f"{self.employee_code} - {self.full_name}"


class EmployeeRole(Base, TimestampMixin):
    """
    Employee Role Model - Stores role definitions
    """
    __tablename__ = "employee_roles"
    __table_args__ = {"schema": "loan_mgmt_schema"}

    role_id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Relationships
    employees = relationship("Employee", back_populates="role")

    def __repr__(self):
        return f"<EmployeeRole {self.role_name}>"


class Branch(Base, TimestampMixin, SoftDeleteMixin):
    """
    Branch Model - Stores branch/office information
    """
    __tablename__ = "branches"
    __table_args__ = {"schema": "loan_mgmt_schema"}

    branch_id = Column(BigInteger, primary_key=True, autoincrement=True)
    branch_code = Column(String(20), unique=True, nullable=False, index=True)
    branch_name = Column(String(100), nullable=False)
    address = Column(Text)
    city = Column(String(100), index=True)
    state = Column(String(100), index=True)
    country = Column(String(100), default="India")
    pincode = Column(String(10))
    phone = Column(String(15))
    email = Column(String(100))
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    employees = relationship("Employee", back_populates="branch")
    customers = relationship("Customer", back_populates="branch")
    loan_applications = relationship("LoanApplication", back_populates="branch")
    loans = relationship("Loan", back_populates="branch")
    regulatory_filings = relationship("RegulatoryFiling", back_populates="branch")

    def __repr__(self):
        return f"<Branch {self.branch_code} - {self.branch_name}>"

    @property
    def full_address(self) -> str:
        """Get complete address"""
        parts = [self.address, self.city, self.state, self.country, self.pincode]
        return ", ".join([p for p in parts if p])