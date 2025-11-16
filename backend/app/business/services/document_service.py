"""
基于DocuGen的投标文档服务 - 真实实现版本
"""
from .real_document_service import RealBiddingDocumentService, RealDocumentGenerator
from .real_llm_client import RealLLMClient
from typing import Dict, Any, List, Optional

# 使用真实的实现
BiddingDocumentService = RealBiddingDocumentService


class TenderAnalysisService:
    """招标文档分析服务 - 真实LLM版本"""

    def __init__(self):
        self.llm_client = RealLLMClient()

    async def analyze_requirements(self, tender_content: str) -> Dict[str, Any]:
        """分析招标需求"""

        prompt = f"""
请详细分析以下招标文档内容：

{tender_content}

请按照以下结构进行分析：

## 1. 项目概述
- 项目名称和背景
- 项目目标和意义
- 项目规模和预算范围

## 2. 技术要求分析
- 核心技术要求
- 系统架构要求
- 性能指标要求
- 安全要求

## 3. 商务要求分析
- 投标保证金
- 履约保证金
- 付款方式
- 合同期限

## 4. 评分标准分析
- 技术分评分要点
- 商务分评分要点
- 资信分评分要点

## 5. 关键时间节点
- 投标截止时间
- 开标时间
- 项目实施周期

## 6. 废标条款识别
- 必须避免的废标情况
- 关键注意事项

请提供详细、专业的分析。
        """

        messages = [
            {"role": "system", "content": "你是专业的招标文档分析专家，具有丰富的招投标经验。"},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.llm_client.chat(messages=messages)
            analysis = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"analysis": analysis}
        except Exception as e:
            return {"analysis": f"分析过程中遇到问题: {str(e)}"}

    async def extract_key_points(self, tender_content: str) -> List[str]:
        """提取招标文档关键要点"""

        prompt = f"""
请从以下招标文档中提取最重要的关键要点，每个要点一行：

{tender_content}

关键要点应包括：
- 核心技术要求
- 重要商务条件
- 关键评分项目
- 必须注意的条款
- 废标风险点

请只列出要点，不要解释。
        """

        messages = [
            {"role": "system", "content": "你是专业的需求分析师，擅长提取文档关键信息。"},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.llm_client.chat(messages=messages)
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            # 解析成列表
            key_points = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # 清理可能的序号
                    if line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                        line = line[2:].strip()
                    if line:
                        key_points.append(line)

            return key_points[:10]  # 返回前10个要点

        except Exception as e:
            return [
                f"关键要点提取遇到问题: {str(e)}",
                "建议检查招标文档格式",
                "确保满足基本技术要求",
                "注意投标截止时间"
            ]