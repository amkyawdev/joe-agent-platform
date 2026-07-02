"""PostgreSQL - PostgreSQL database integration."""

from typing import Any, Optional, List, Dict
from contextlib import contextmanager
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class PostgresDatabase:
    """PostgreSQL database wrapper."""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://joe:joe@localhost:5432/joe_db"
        )
        self.engine = create_engine(self.database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope for operations."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def execute(self, query: str, params: Dict = None) -> Any:
        """Execute a query."""
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            return result
    
    def fetch_one(self, query: str, params: Dict = None) -> Optional[Dict]:
        """Fetch one row."""
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            row = result.fetchone()
            return dict(row._mapping) if row else None
    
    def fetch_all(self, query: str, params: Dict = None) -> List[Dict]:
        """Fetch all rows."""
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
    
    def create_tables(self) -> None:
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)