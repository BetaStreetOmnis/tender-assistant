"""
投标相关的Pydantic数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class BidResponseBase(BaseModel):
    """投标响应基础模型"""
    title: str = Field(..., description="投标响应标题")
    tender_id: UUID = Field(..., description="关联的招标项目ID")
    template_type: Optional[str] = Field(None, description="使用的模板类型")
    status: str = Field(default="draft", description="状态")
    content: Optional[str] = Field(None, description="投标内容")


class BidResponseCreate(BidResponseBase):
    """创建投标响应的请求模型"""
    pass


class BidResponseUpdate(BaseModel):
    """更新投标响应的请求模型"""
    title: Optional[str] = None
    template_type: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None


class BidResponseResponse(BidResponseBase):
    """投标响应响应模型"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BidTemplateBase(BaseModel):
    """投标模板基础模型"""
    name: str = Field(..., description="模板名称")
    template_type: str = Field(..., description="模板类型")
    description: Optional[str] = Field(None, description="模板描述")
    variables: Optional[Dict[str, Any]] = Field(default_factory=dict, description="模板变量")


class BidTemplateCreate(BidTemplateBase):
    """创建投标模板的请求模型"""
    pass


class BidTemplateResponse(BidTemplateBase):
    """投标模板响应模型"""
    id: UUID
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class BidCheckResult(BaseModel):
    """投标检查结果"""
    check_type: str = Field(..., description="检查类型")
    status: str = Field(..., description="检查状态")
    issues: List[str] = Field(default_factory=list, description="发现的问题")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")
    score: Optional[float] = Field(None, description="检查得分")


class BidCheckResultResponse(BaseModel):
    """投标检查结果响应"""
    id: UUID
    bid_response_id: UUID
    disqualification_check: BidCheckResult = Field(..., description="废标项检查")
    consistency_check: BidCheckResult = Field(..., description="一致性检查")
    completeness_check: BidCheckResult = Field(..., description="完整性检查")
    overall_score: float = Field(..., description="总体得分")
    recommendations: List[str] = Field(default_factory=list, description="总体建议")
    check_time: datetime = Field(..., description="检查时间")

    class Config:
        from_attributes = True


class DocumentGenerationRequest(BaseModel):
    """文档生成请求"""
    tender_requirements: str = Field(..., description="招标需求")
    key_points: Optional[str] = Field(None, description="关键要点")
    rag_content: Optional[str] = Field(None, description="参考内容")
    template_name: Optional[str] = Field(None, description="模板名称")


class DocumentGenerationResponse(BaseModel):
    """文档生成响应"""
    file_path: str = Field(..., description="生成的文件路径")
    download_url: str = Field(..., description="下载链接")
    generation_time: float = Field(..., description="生成耗时（秒）")
    word_count: Optional[int] = Field(None, description="字数")


class OutlineGenerationRequest(BaseModel):
    """大纲生成请求"""
    tender_requirements: str = Field(..., description="招标需求")
    key_points: Optional[str] = Field(None, description="关键要点")
    rag_content: Optional[str] = Field(None, description="参考内容")


class OutlineGenerationResponse(BaseModel):
    """大纲生成响应"""
    outline: str = Field(..., description="生成的大纲")
    generation_time: float = Field(..., description="生成耗时（秒）")


class TemplateUploadResponse(BaseModel):
    """模板上传响应"""
    template_name: str = Field(..., description="模板名称")
    file_path: str = Field(..., description="文件路径")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(..., description="上传时间")


class BidResponseListResponse(BaseModel):
    """投标响应列表响应"""
    items: List[BidResponseResponse]
    total: int
    page: int
    page_size: int