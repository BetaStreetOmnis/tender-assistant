"""
招标项目数据模型
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class TenderProject(Base):
    """招标项目表"""
    __tablename__ = "tender_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String(255), nullable=False, comment="项目名称")
    tender_unit = Column(String(255), comment="招标单位")
    tender_no = Column(String(100), comment="招标编号")
    deadline = Column(DateTime, comment="投标截止时间")
    budget = Column(Numeric(15, 2), comment="项目预算")
    document_id = Column(UUID(as_uuid=True), comment="关联文档ID")
    status = Column(String(50), default="draft", comment="状态：draft/analyzing/completed")
    metadata = Column(JSON, comment="元数据")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TenderProject {self.project_name}>"


class TenderDocument(Base):
    """招标文件表"""
    __tablename__ = "tender_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_project_id = Column(UUID(as_uuid=True), comment="招标项目ID")
    file_name = Column(String(255), comment="文件名")
    file_path = Column(String(500), comment="文件路径")
    file_type = Column(String(50), comment="文件类型")
    file_size = Column(Numeric, comment="文件大小")
    parsed_content = Column(Text, comment="解析内容")
    metadata = Column(JSON, comment="元数据")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TenderDocument {self.file_name}>"


class TenderRequirement(Base):
    """招标需求表"""
    __tablename__ = "tender_requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_project_id = Column(UUID(as_uuid=True), comment="招标项目ID")
    requirement_type = Column(String(100), comment="需求类型")
    requirement_content = Column(Text, comment="需求内容")
    priority = Column(String(20), comment="优先级")
    is_mandatory = Column(Boolean, default=True, comment="是否必填")
    extracted_by = Column(String(50), comment="提取方式")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TenderRequirement {self.requirement_type}>"