"""
依赖注入模块
"""
from functools import lru_cache
from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.business.services.document_service import BiddingDocumentService, TenderAnalysisService


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_bidding_service() -> BiddingDocumentService:
    """获取投标文档服务（单例）"""
    return BiddingDocumentService()


@lru_cache()
def get_tender_analysis_service() -> TenderAnalysisService:
    """获取招标分析服务（单例）"""
    return TenderAnalysisService()
