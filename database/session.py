from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import AsyncSessionLocal, get_db
import logging

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    """
    Manager for database sessions
    """

    def __init__(self):
        self.session: Optional[AsyncSession] = None

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager for database session
        """
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Session error: {str(e)}")
                raise
            finally:
                await session.close()

    async def execute(self, statement):
        """
        Execute a statement and return the result
        """
        async with self.session() as session:
            return await session.execute(statement)

    async def commit(self):
        """
        Commit the current transaction
        """
        if self.session:
            await self.session.commit()

    async def rollback(self):
        """
        Rollback the current transaction
        """
        if self.session:
            await self.session.rollback()


db_manager = DatabaseSessionManager()