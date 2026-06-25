from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    """
    Mixin to add created_at and updated_at fields
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class SoftDeleteMixin:
    """
    Mixin to add soft delete functionality
    """
    is_deleted = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = datetime.now()

    def restore(self):
        self.is_deleted = None