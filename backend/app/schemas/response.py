"""
统一响应模型
"""
from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    code: int = 200
    data: Optional[T] = None
    message: str = "操作成功"
    
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def pages(self) -> int:
        """总页数"""
        return (self.total + self.page_size - 1) // self.page_size


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int
    detail: str
    error_type: Optional[str] = None


class TemplateInfo(BaseModel):
    """模板信息"""
    name: str
    variables: List[str] = []
    description: Optional[str] = None


class TenderAnalysisResult(BaseModel):
    """招标分析结果"""
    analysis: str
    key_points: List[str]
    requirements: Optional[List[str]] = None
    budget: Optional[str] = None
    deadline: Optional[str] = None


class OutlineResult(BaseModel):
    """大纲生成结果"""
    outline: str
    sections: List[str]
    estimated_pages: Optional[int] = None


class DocumentResult(BaseModel):
    """文档生成结果"""
    file_path: str
    download_url: str
    file_size: Optional[int] = None
    created_at: Optional[str] = None
