"""
投标响应数据模型
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, JSON, Boolean
from app.models.base import Base


class BidResponse(Base):
    """投标响应文档表"""
    __tablename__ = "bid_responses"

    # 使用String类型存储UUID，兼容MySQL
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tender_id = Column(String(100), comment="招标项目ID")  # 修改字段名以匹配API
    title = Column(String(255), nullable=False, comment="项目标题")  # 新增字段
    content = Column(Text, comment="项目内容")  # 新增字段
    status = Column(String(50), default="draft", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BidResponse {self.title}>"


class BidTemplate(Base):
    """投标模板表"""
    __tablename__ = "bid_templates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    template_name = Column(String(255), nullable=False, comment="模板名称")
    template_type = Column(String(100), comment="模板类型")
    template_file = Column(String(500), comment="模板文件路径")
    variables = Column(JSON, comment="变量定义")
    description = Column(Text, comment="描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BidTemplate {self.template_name}>"


class CheckRule(Base):
    """检查规则表"""
    __tablename__ = "check_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_name = Column(String(255), nullable=False, comment="规则名称")
    rule_type = Column(String(100), comment="规则类型")
    rule_config = Column(JSON, comment="规则配置")
    severity = Column(String(20), comment="严重程度")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CheckRule {self.rule_name}>"


class CheckResult(Base):
    """检查结果表"""
    __tablename__ = "check_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bid_response_id = Column(String(36), comment="投标响应ID")
    rule_id = Column(String(36), comment="规则ID")
    check_status = Column(String(50), comment="检查状态")
    issues = Column(JSON, comment="问题列表")
    suggestions = Column(Text, comment="建议")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CheckResult {self.check_status}>"