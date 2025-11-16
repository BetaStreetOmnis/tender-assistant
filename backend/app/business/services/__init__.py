"""
业务服务层 - 简化版
"""

from app.business.services.document_service import BiddingDocumentService, TenderAnalysisService

__all__ = [
    "BiddingDocumentService",
    "TenderAnalysisService"
]