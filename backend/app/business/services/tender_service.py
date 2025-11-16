"""
招标文件处理服务
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from pathlib import Path
import asyncio

from app.knowledge.parsers.pdf_parser import PDFParser
from app.knowledge.parsers.docx_parser import DocxParser
from app.knowledge.llm.llm_client import LLMClient


class TenderService:
    """招标文件分析服务"""

    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DocxParser()
        self.llm_client = LLMClient()

    async def parse_tender_document(self, file_path: str) -> Dict[str, Any]:
        """
        解析招标文件，提取文本内容

        Args:
            file_path: 文件路径

        Returns:
            解析结果 {content: str, metadata: dict}
        """
        file_path_obj = Path(file_path)
        suffix = file_path_obj.suffix.lower()

        if suffix == '.pdf':
            result = await self.pdf_parser.parse(file_path)
        elif suffix in ['.docx', '.doc']:
            result = await self.docx_parser.parse(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")

        return result

    async def extract_tender_info(self, content: str) -> Dict[str, Any]:
        """
        使用LLM从招标文件中提取关键信息

        Args:
            content: 文档内容

        Returns:
            提取的信息 {project_name, tender_unit, budget, deadline, requirements, etc.}
        """
        prompt = f"""
请从以下招标文件中提取关键信息，以JSON格式返回：

1. project_name: 项目名称
2. tender_unit: 招标单位
3. budget: 预算金额（数字）
4. deadline: 截止时间
5. contact_info: 联系方式
6. requirements: 主要需求（列表）
7. technical_specs: 技术规格要求（列表）
8. qualification: 资质要求（列表）
9. disqualification_items: 废标条款（列表）

招标文件内容：
{content[:8000]}

请严格按照JSON格式返回，不要包含其他内容。
"""

        response = await self.llm_client.chat(prompt)

        # 解析JSON响应
        import json
        try:
            info = json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                info = json.loads(json_match.group())
            else:
                raise ValueError("LLM返回的内容不是有效的JSON格式")

        return info

    async def analyze_requirements(self, project_id: UUID, content: str) -> Dict[str, Any]:
        """
        深度分析招标需求

        Args:
            project_id: 项目ID
            content: 招标文件内容

        Returns:
            需求分析结果
        """
        # 提取关键信息
        basic_info = await self.extract_tender_info(content)

        # 需求分类分析
        requirements_analysis = await self._analyze_requirements_detail(content)

        # 风险评估
        risk_assessment = await self._assess_risks(content)

        return {
            "project_id": str(project_id),
            "basic_info": basic_info,
            "requirements_analysis": requirements_analysis,
            "risk_assessment": risk_assessment,
            "analysis_summary": await self._generate_summary(basic_info, requirements_analysis, risk_assessment)
        }

    async def _analyze_requirements_detail(self, content: str) -> Dict[str, List[str]]:
        """详细需求分析"""
        prompt = f"""
请对以下招标需求进行详细分析，分类整理：

1. functional_requirements: 功能性需求
2. technical_requirements: 技术性需求
3. performance_requirements: 性能要求
4. security_requirements: 安全要求
5. compliance_requirements: 合规要求

招标文件：
{content[:6000]}

以JSON格式返回。
"""
        response = await self.llm_client.chat(prompt)

        import json, re
        try:
            return json.loads(response)
        except:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}

    async def _assess_risks(self, content: str) -> Dict[str, Any]:
        """风险评估"""
        prompt = f"""
请评估该招标项目的风险，包括：

1. technical_risks: 技术实现风险（列表）
2. timeline_risks: 时间风险
3. cost_risks: 成本风险
4. compliance_risks: 合规风险
5. overall_risk_level: 整体风险等级 (low/medium/high)

招标文件：
{content[:4000]}

以JSON格式返回。
"""
        response = await self.llm_client.chat(prompt)

        import json, re
        try:
            return json.loads(response)
        except:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"overall_risk_level": "medium"}

    async def _generate_summary(self, basic_info: Dict, requirements: Dict, risks: Dict) -> str:
        """生成分析摘要"""
        prompt = f"""
根据以下信息生成招标项目分析摘要（200-300字）：

基本信息：{basic_info}
需求分析：{requirements}
风险评估：{risks}

请生成简洁专业的摘要。
"""
        return await self.llm_client.chat(prompt)
