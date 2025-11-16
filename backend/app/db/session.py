"""
数据库会话管理 - 同步版本
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# 创建数据库引擎（同步版本）
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=settings.DATABASE_ECHO
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    数据库会话依赖
    用于FastAPI路由中注入数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()