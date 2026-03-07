"""
单元测试配置
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db


# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# 测试数据
@pytest.fixture
def sample_tender_content():
    """示例招标内容"""
    return """
    招标公告
    
    项目名称：XX系统开发项目
    预算金额：100万元
    投标截止时间：2026年4月15日
    
    资格要求：
    1. 具有独立法人资格
    2. 近3年内完成过类似项目
    3. 团队规模不少于10人
    
    技术要求：
    1. 采用微服务架构
    2. 支持高并发
    3. 提供完整的技术文档
    """
