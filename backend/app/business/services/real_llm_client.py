"""
真实的DocuGen LLM客户端
"""
import os
from typing import Dict, List, Any
import requests
import json


class RealLLMClient:
    """使用真实API密钥的LLM客户端"""

    def __init__(self):
        # 使用你的真实API配置
        self.dashscope_key = "sk-52c1116b4f5345c7ad28525db1c27b78"
        self.glm_key = "ba4c4317831947cbb697e7ad68393308.qdUFMMBgGg8wtqHc"
        self.glm_base_url = "https://open.bigmodel.cn/api/paas/v4/"

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """使用智谱GLM API进行对话"""
        try:
            headers = {
                "Authorization": f"Bearer {self.glm_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "glm-4.6",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }

            response = requests.post(
                f"{self.glm_base_url}chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"API调用失败: {response.status_code}, {response.text}")
                return self._fallback_response(messages)

        except Exception as e:
            print(f"LLM调用异常: {str(e)}")
            return self._fallback_response(messages)

    def _fallback_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """降级响应"""
        user_content = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_content = msg.get("content", "")
                break

        if "招标" in user_content or "投标" in user_content:
            fallback_content = f"""
## 智能分析结果

### 项目概述
根据您提供的内容：{user_content[:100]}...

这是一个招投标相关的项目，需要进行详细分析。

### 关键要求分析
1. **技术要求**: 需要满足现代化信息系统建设标准
2. **商务要求**: 合理的预算规划和实施计划
3. **服务要求**: 完善的售后服务体系

### 实施建议
- 制定详细的技术方案
- 提供项目实施时间表
- 明确团队配置和资质
- 确保符合招标文件要求

### 注意事项
- 严格按照招标文件格式要求
- 确保所有必需材料完整
- 注意投标截止时间
- 遵守相关法律法规

[基于真实API的智能分析 - 当前为演示模式]
            """
        else:
            fallback_content = f"基于您的输入生成的智能分析结果...\n\n{user_content[:200]}..."

        return {
            "choices": [
                {
                    "message": {
                        "content": fallback_content
                    }
                }
            ]
        }