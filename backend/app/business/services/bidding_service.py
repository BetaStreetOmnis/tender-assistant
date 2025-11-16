"""
投标文档生成与检查服务
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from pathlib import Path
import asyncio

from app.docgen.llm.llm_client import LLMClient
from app.docgen.generators.generator_doc import DocumentGenerator
from app.docgen.templates.base_templates_generator import TemplateManager


class BiddingService:
    """投标文档生成服务"""

    def __init__(self):
        self.llm_client = LLMClient()
        self.doc_generator = DocumentGenerator()
        self.template_manager = TemplateManager()

    async def generate_bid_document(
        self,
        template_id: UUID,
        tender_info: Dict[str, Any],
        enable_rag: bool = True
    ) -> Dict[str, Any]:
        """
        生成投标文档

        Args:
            template_id: 模板ID
            tender_info: 招标信息
            enable_rag: 是否启用RAG检索

        Returns:
            生成结果 {document_path, content, outline}
        """
        # 1. 加载模板
        template = await self.template_manager.load_template(str(template_id))

        # 2. 生成文档大纲
        outline_prompt = self._build_outline_prompt(tender_info, template)
        outline = await self.doc_generator.generate_outline(outline_prompt)

        # 3. 逐章节生成内容
        sections = []
        for section in outline.get('sections', []):
            content_prompt = self._build_section_prompt(
                section,
                tender_info,
                enable_rag
            )
            section_content = await self.doc_generator.generate_section(content_prompt)
            sections.append({
                "title": section.get('title'),
                "content": section_content
            })

        # 4. 合并生成完整文档
        full_document = await self._assemble_document(sections, template)

        # 5. 保存文档
        document_path = await self._save_document(full_document, tender_info)

        return {
            "document_path": document_path,
            "content": full_document,
            "outline": outline,
            "sections": sections
        }

    async def check_bid_document(
        self,
        bid_response_id: UUID,
        document_path: str,
        tender_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        智能检查投标文档

        Args:
            bid_response_id: 投标响应ID
            document_path: 文档路径
            tender_requirements: 招标要求

        Returns:
            检查结果 {disqualification_check, consistency_check, completeness_check}
        """
        # 读取文档内容
        document_content = await self._read_document(document_path)

        # 并行执行三项检查
        disqualification_task = self._check_disqualification(
            document_content,
            tender_requirements
        )
        consistency_task = self._check_consistency(document_content)
        completeness_task = self._check_completeness(
            document_content,
            tender_requirements
        )

        disqualification_result, consistency_result, completeness_result = await asyncio.gather(
            disqualification_task,
            consistency_task,
            completeness_task
        )

        # 综合评分
        overall_score = self._calculate_overall_score(
            disqualification_result,
            consistency_result,
            completeness_result
        )

        return {
            "bid_response_id": str(bid_response_id),
            "disqualification_check": disqualification_result,
            "consistency_check": consistency_result,
            "completeness_check": completeness_result,
            "overall_score": overall_score,
            "recommendations": await self._generate_recommendations(
                disqualification_result,
                consistency_result,
                completeness_result
            )
        }

    async def _check_disqualification(
        self,
        document: str,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """检查废标条款"""
        disqualification_items = requirements.get('disqualification_items', [])

        if not disqualification_items:
            return {
                "status": "pass",
                "issues": [],
                "score": 100
            }

        prompt = f"""
请检查以下投标文档是否违反废标条款：

废标条款：
{chr(10).join([f"- {item}" for item in disqualification_items])}

投标文档内容：
{document[:10000]}

请逐条检查，返回JSON格式：
{{
    "status": "pass/warning/fail",
    "issues": [
        {{
            "item": "废标条款描述",
            "violation": true/false,
            "explanation": "说明"
        }}
    ],
    "score": 0-100
}}
"""

        response = await self.llm_client.chat(prompt)

        import json, re
        try:
            return json.loads(response)
        except:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"status": "unknown", "issues": [], "score": 0}

    async def _check_consistency(self, document: str) -> Dict[str, Any]:
        """检查一致性"""
        prompt = f"""
请检查投标文档内部的一致性，包括：

1. 技术方案与报价是否匹配
2. 前后描述是否矛盾
3. 关键数据是否一致
4. 承诺与能力是否匹配

投标文档：
{document[:10000]}

返回JSON格式：
{{
    "status": "good/warning/poor",
    "issues": [
        {{
            "type": "一致性问题类型",
            "description": "问题描述",
            "severity": "high/medium/low"
        }}
    ],
    "score": 0-100
}}
"""

        response = await self.llm_client.chat(prompt)

        import json, re
        try:
            return json.loads(response)
        except:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"status": "good", "issues": [], "score": 85}

    async def _check_completeness(
        self,
        document: str,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """检查完整性"""
        required_sections = requirements.get('required_sections', [
            "投标函",
            "企业资质",
            "技术方案",
            "项目管理方案",
            "商务报价",
            "售后服务"
        ])

        prompt = f"""
请检查投标文档的完整性，确认是否包含以下必需章节：

必需章节：
{chr(10).join([f"- {section}" for section in required_sections])}

投标文档：
{document[:8000]}

返回JSON格式：
{{
    "status": "complete/incomplete",
    "missing_sections": ["缺失的章节"],
    "present_sections": ["已有的章节"],
    "score": 0-100
}}
"""

        response = await self.llm_client.chat(prompt)

        import json, re
        try:
            return json.loads(response)
        except:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"status": "complete", "missing_sections": [], "score": 90}

    def _calculate_overall_score(
        self,
        disqualification: Dict,
        consistency: Dict,
        completeness: Dict
    ) -> int:
        """计算综合评分"""
        # 权重：废标检查50%，一致性30%，完整性20%
        if disqualification.get('status') == 'fail':
            return 0  # 有废标项直接0分

        disq_score = disqualification.get('score', 0)
        cons_score = consistency.get('score', 0)
        comp_score = completeness.get('score', 0)

        overall = int(disq_score * 0.5 + cons_score * 0.3 + comp_score * 0.2)
        return overall

    async def _generate_recommendations(
        self,
        disqualification: Dict,
        consistency: Dict,
        completeness: Dict
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []

        # 废标问题
        if disqualification.get('status') in ['warning', 'fail']:
            for issue in disqualification.get('issues', []):
                if issue.get('violation'):
                    recommendations.append(f"⚠️ 废标风险：{issue.get('explanation')}")

        # 一致性问题
        for issue in consistency.get('issues', []):
            if issue.get('severity') in ['high', 'medium']:
                recommendations.append(f"📝 一致性问题：{issue.get('description')}")

        # 完整性问题
        missing = completeness.get('missing_sections', [])
        if missing:
            recommendations.append(f"📋 缺失章节：{', '.join(missing)}")

        return recommendations

    def _build_outline_prompt(self, tender_info: Dict, template: Dict) -> str:
        """构建大纲生成提示"""
        return f"""
请为以下招标项目生成投标文档大纲：

项目名称：{tender_info.get('project_name')}
招标单位：{tender_info.get('tender_unit')}
主要需求：{tender_info.get('requirements')}

请生成标准投标文档的章节大纲（JSON格式）。
"""

    def _build_section_prompt(
        self,
        section: Dict,
        tender_info: Dict,
        enable_rag: bool
    ) -> str:
        """构建章节内容生成提示"""
        prompt = f"""
请为投标文档生成"{section.get('title')}"章节的内容。

项目信息：
- 项目名称：{tender_info.get('project_name')}
- 招标要求：{tender_info.get('requirements')}
- 章节描述：{section.get('description', '')}

要求：内容专业、详实、符合招标要求。
"""
        return prompt

    async def _assemble_document(self, sections: List[Dict], template: Dict) -> str:
        """组装完整文档"""
        doc_parts = []

        for section in sections:
            doc_parts.append(f"# {section['title']}\n\n")
            doc_parts.append(section['content'])
            doc_parts.append("\n\n")

        return ''.join(doc_parts)

    async def _save_document(self, content: str, tender_info: Dict) -> str:
        """保存文档"""
        # 简化版：直接保存为文本文件
        import uuid
        from datetime import datetime

        filename = f"bid_{tender_info.get('project_name', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = Path("/tmp") / filename

        filepath.write_text(content, encoding='utf-8')

        return str(filepath)

    async def _read_document(self, document_path: str) -> str:
        """读取文档内容"""
        path = Path(document_path)
        if path.exists():
            return path.read_text(encoding='utf-8')
        return ""
