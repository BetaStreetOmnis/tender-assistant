"""
数据库初始化脚本
"""
from sqlalchemy import create_engine
from app.models.base import Base
from app.models.tender import TenderProject, TenderDocument, TenderRequirement
from app.models.bidding import BidResponse, BidTemplate, BidCheckResult
from app.models.document import Document, DocumentChunk
from app.models.user import User
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """初始化数据库表"""
    try:
        logger.info("开始初始化数据库...")

        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)

        # 创建所有表
        logger.info("创建数据库表...")
        Base.metadata.create_all(bind=engine)

        logger.info("✅ 数据库表创建成功")

        # 显示已创建的表
        tables = Base.metadata.tables.keys()
        logger.info(f"已创建 {len(tables)} 个表:")
        for table in tables:
            logger.info(f"  - {table}")

        return True

    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        return False


def create_demo_data():
    """创建演示数据"""
    try:
        from app.db.session import SessionLocal
        from uuid import uuid4
        from datetime import datetime, timedelta
        import bcrypt

        logger.info("开始创建演示数据...")

        db = SessionLocal()

        # 创建演示用户
        demo_user = User(
            id=uuid4(),
            username="demo",
            email="demo@example.com",
            hashed_password=bcrypt.hashpw("demo123".encode(), bcrypt.gensalt()).decode(),
            full_name="演示用户",
            is_active=True,
            created_at=datetime.now()
        )
        db.add(demo_user)

        # 创建演示招标项目
        demo_project = TenderProject(
            id=uuid4(),
            project_name="智慧园区管理平台建设项目",
            project_code="TEN-2024-001",
            tender_unit="某市科技园管理委员会",
            budget=5000000.00,
            deadline=datetime.now() + timedelta(days=30),
            status="analyzing",
            description="建设一套智慧园区综合管理平台，包含智能监控、能源管理、访客管理等功能",
            created_by=demo_user.id,
            created_at=datetime.now()
        )
        db.add(demo_project)

        # 创建演示投标模板
        demo_template = BidTemplate(
            id=uuid4(),
            template_name="软件开发项目投标模板",
            template_type="software_development",
            template_file="/templates/software_bidding_template.docx",
            description="适用于软件开发、系统集成类项目的投标文档模板",
            variables={
                "project_name": "项目名称",
                "company_name": "公司名称",
                "technical_approach": "技术方案",
                "timeline": "项目周期"
            },
            is_active=True,
            created_by=demo_user.id,
            created_at=datetime.now()
        )
        db.add(demo_template)

        db.commit()
        logger.info("✅ 演示数据创建成功")

        return True

    except Exception as e:
        logger.error(f"❌ 演示数据创建失败: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  AI标书助理系统 - 数据库初始化")
    print("=" * 60)

    # 初始化数据库表
    if init_database():
        print("\n✅ 数据库初始化成功")

        # 询问是否创建演示数据
        response = input("\n是否创建演示数据？(y/n): ")
        if response.lower() == 'y':
            if create_demo_data():
                print("\n✅ 演示数据创建成功")
                print("\n演示账号:")
                print("  用户名: demo")
                print("  密码: demo123")
            else:
                print("\n❌ 演示数据创建失败")
    else:
        print("\n❌ 数据库初始化失败")
