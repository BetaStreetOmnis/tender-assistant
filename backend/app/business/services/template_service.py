"""
模板管理服务
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from pathlib import Path
import json


class TemplateService:
    """投标模板管理服务"""

    def __init__(self):
        self.template_base_path = Path("/app/storage/templates")
        self.template_base_path.mkdir(parents=True, exist_ok=True)

    async def list_templates(
        self,
        template_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取模板列表

        Args:
            template_type: 模板类型过滤

        Returns:
            模板列表
        """
        # 这里返回预定义的模板列表
        templates = [
            {
                "id": "software-dev-001",
                "name": "软件开发项目投标模板",
                "type": "software_development",
                "description": "适用于软件开发、系统集成类项目",
                "sections": [
                    "投标函",
                    "企业资质与业绩",
                    "技术方案",
                    "项目管理方案",
                    "质量保证措施",
                    "商务报价",
                    "售后服务承诺"
                ],
                "variables": {
                    "project_name": "项目名称",
                    "company_name": "公司名称",
                    "project_budget": "项目预算",
                    "timeline": "项目周期",
                    "technical_lead": "技术负责人"
                }
            },
            {
                "id": "hardware-integration-001",
                "name": "软硬一体项目投标模板",
                "type": "hardware_integration",
                "description": "适用于包含硬件采购和软件开发的综合项目",
                "sections": [
                    "投标函",
                    "企业资质与业绩",
                    "技术方案",
                    "硬件配置清单",
                    "软件功能说明",
                    "项目管理方案",
                    "商务报价",
                    "售后服务"
                ],
                "variables": {
                    "project_name": "项目名称",
                    "company_name": "公司名称",
                    "hardware_list": "硬件清单",
                    "software_features": "软件功能"
                }
            },
            {
                "id": "consulting-service-001",
                "name": "咨询服务投标模板",
                "type": "consulting_service",
                "description": "适用于技术咨询、培训等服务类项目",
                "sections": [
                    "投标函",
                    "企业资质",
                    "服务方案",
                    "专家团队",
                    "服务承诺",
                    "商务报价"
                ],
                "variables": {
                    "project_name": "项目名称",
                    "service_scope": "服务范围",
                    "expert_team": "专家团队"
                }
            }
        ]

        if template_type:
            templates = [t for t in templates if t["type"] == template_type]

        return templates

    async def get_template_detail(self, template_id: str) -> Dict[str, Any]:
        """
        获取模板详情

        Args:
            template_id: 模板ID

        Returns:
            模板详情
        """
        templates = await self.list_templates()

        for template in templates:
            if template["id"] == template_id:
                return template

        raise ValueError(f"模板不存在: {template_id}")

    async def create_custom_template(
        self,
        name: str,
        template_type: str,
        sections: List[str],
        variables: Dict[str, str],
        template_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建自定义模板

        Args:
            name: 模板名称
            template_type: 模板类型
            sections: 章节列表
            variables: 变量定义
            template_content: 模板内容（可选）

        Returns:
            创建的模板信息
        """
        import uuid

        template_id = str(uuid.uuid4())

        template = {
            "id": template_id,
            "name": name,
            "type": template_type,
            "sections": sections,
            "variables": variables,
            "custom": True
        }

        # 保存模板配置
        template_config_file = self.template_base_path / f"{template_id}.json"
        template_config_file.write_text(
            json.dumps(template, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        # 如果提供了模板内容，保存模板文件
        if template_content:
            template_file = self.template_base_path / f"{template_id}.docx"
            # 这里应该调用python-docx生成Word文档
            # 简化版：直接保存文本
            template_file.write_text(template_content, encoding='utf-8')

        return template

    async def update_template(
        self,
        template_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新模板

        Args:
            template_id: 模板ID
            updates: 更新内容

        Returns:
            更新后的模板信息
        """
        template_config_file = self.template_base_path / f"{template_id}.json"

        if not template_config_file.exists():
            raise ValueError(f"模板不存在: {template_id}")

        template = json.loads(template_config_file.read_text(encoding='utf-8'))

        # 更新模板配置
        template.update(updates)

        # 保存更新
        template_config_file.write_text(
            json.dumps(template, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        return template

    async def delete_template(self, template_id: str) -> bool:
        """
        删除模板

        Args:
            template_id: 模板ID

        Returns:
            是否成功
        """
        template_config_file = self.template_base_path / f"{template_id}.json"
        template_file = self.template_base_path / f"{template_id}.docx"

        deleted = False

        if template_config_file.exists():
            template_config_file.unlink()
            deleted = True

        if template_file.exists():
            template_file.unlink()

        return deleted

    async def render_template(
        self,
        template_id: str,
        variables: Dict[str, Any]
    ) -> str:
        """
        渲染模板

        Args:
            template_id: 模板ID
            variables: 变量值

        Returns:
            渲染后的内容
        """
        template = await self.get_template_detail(template_id)

        # 简化版：生成Markdown格式的文档
        content_parts = [f"# {variables.get('project_name', '项目名称')}\n\n"]

        for section in template.get("sections", []):
            content_parts.append(f"## {section}\n\n")
            content_parts.append(f"[此处填写 {section} 的具体内容]\n\n")

        return ''.join(content_parts)
