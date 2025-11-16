"""
招标相关的Pydantic数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class TenderProjectBase(BaseModel):
    """招标项目基础模型"""
    title: str = Field(..., description="招标项目标题")
    description: Optional[str] = Field(None, description="项目描述")
    budget: Optional[float] = Field(None, description="项目预算")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    contact_person: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")


class TenderProjectCreate(TenderProjectBase):
    """创建招标项目的请求模型"""
    pass


class TenderProjectUpdate(BaseModel):
    """更新招标项目的请求模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    deadline: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None


class TenderProjectResponse(TenderProjectBase):
    """招标项目响应模型"""
    id: UUID
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TenderDocumentBase(BaseModel):
    """招标文档基础模型"""
    filename: str = Field(..., description="文件名")
    file_type: str = Field(..., description="文件类型")
    file_size: Optional[int] = Field(None, description="文件大小")
    description: Optional[str] = Field(None, description="文档描述")


class TenderDocumentCreate(TenderDocumentBase):
    """创建招标文档的请求模型"""
    tender_id: UUID = Field(..., description="招标项目ID")


class TenderDocumentResponse(TenderDocumentBase):
    """招标文档响应模型"""
    id: UUID
    tender_id: UUID
    file_path: str
    upload_time: datetime

    class Config:
        from_attributes = True


class TenderRequirementBase(BaseModel):
    """招标需求基础模型"""
    requirement_type: str = Field(..., description="需求类型")
    content: str = Field(..., description="需求内容")
    priority: Optional[str] = Field("medium", description="优先级")
    is_mandatory: bool = Field(True, description="是否必需")


class TenderRequirementCreate(TenderRequirementBase):
    """创建招标需求的请求模型"""
    tender_id: UUID = Field(..., description="招标项目ID")


class TenderRequirementResponse(TenderRequirementBase):
    """招标需求响应模型"""
    id: UUID
    tender_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TenderAnalysisResult(BaseModel):
    """招标文档分析结果"""
    project_overview: Optional[str] = Field(None, description="项目概述")
    technical_requirements: List[str] = Field(default_factory=list, description="技术要求")
    business_requirements: List[str] = Field(default_factory=list, description="商务要求")
    evaluation_criteria: List[str] = Field(default_factory=list, description="评分标准")
    key_deadlines: List[str] = Field(default_factory=list, description="关键时间节点")
    disqualification_items: List[str] = Field(default_factory=list, description="废标条款")
    analysis_summary: Optional[str] = Field(None, description="分析总结")


class TenderListResponse(BaseModel):
    """招标列表响应"""
    items: List[TenderProjectResponse]
    total: int
    page: int
    page_size: int