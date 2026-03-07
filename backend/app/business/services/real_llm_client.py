"""
真实的DocuGen LLM客户端
"""
import os
import logging
from typing import Dict, List, Any
import requests
import json

logger = logging.getLogger(__name__)


class RealLLMClient:
    """使用真实API密钥的LLM客户端"""

    def __init__(self):
        # 从环境变量读取 API 配置（安全实践）
        self.dashscope_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.glm_key = os.getenv("GLM_API_KEY", "")
        self.glm_base_url = os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
        
        # OpenAI 兼容接口
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # DeepSeek
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # 优先级顺序
        self.api_priority = []
        self._setup_api_priority()

    def _setup_api_priority(self):
        """设置 API 优先级"""
        if self.openai_key:
            self.api_priority.append("openai")
        if self.deepseek_key:
            self.api_priority.append("deepseek")
        if self.glm_key:
            self.api_priority.append("glm")
        if self.dashscope_key:
            self.api_priority.append("dashscope")
        
        if not self.api_priority:
            logger.warning("⚠️ 未配置任何 LLM API Key，将使用降级模式")
        else:
            logger.info(f"✅ 可用 API: {', '.join(self.api_priority)}")

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """智能选择可用的 API 进行对话"""
        
        # 按优先级尝试不同的 API
        for api_name in self.api_priority:
            try:
                if api_name == "openai":
                    return self._chat_openai(messages, **kwargs)
                elif api_name == "deepseek":
                    return self._chat_deepseek(messages, **kwargs)
                elif api_name == "glm":
                    return self._chat_glm(messages, **kwargs)
                elif api_name == "dashscope":
                    return self._chat_dashscope(messages, **kwargs)
            except Exception as e:
                logger.warning(f"API {api_name} 调用失败: {str(e)}")
                continue
        
        # 所有 API 都失败，使用降级响应
        logger.warning("⚠️ 所有 API 调用失败，使用降级响应")
        return self._fallback_response(messages)

    def _chat_openai(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """使用 OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.openai_model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        response = requests.post(
            f"{self.openai_base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"OpenAI API 错误: {response.status_code}")
    
    def _chat_deepseek(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """使用 DeepSeek API"""
        headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json"
            }
        
        data = {
                "model": self.deepseek_model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2000)
            }
        
            response = requests.post(
                f"{self.deepseek_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
        
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"DeepSeek API 错误: {response.status_code}")
    
    def _chat_glm(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """使用智谱 GLM API"""
        headers = {
                "Authorization": f"Bearer {self.glm_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "glm-4-flash",
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2000)
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
                raise Exception(f"GLM API 错误: {response.status_code}")
    
    def _chat_dashscope(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """使用通义千问 API（DashScope）"""
        headers = {
            "Authorization": f"Bearer {self.dashscope_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "qwen-plus",
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2000)
            }
        }
        
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"DashScope API 错误: {response.status_code}")

    def _fallback_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """降级响应（当所有 API 不可用时）"""
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

⚠️ **提示**: 当前为降级模式（未配置有效的 LLM API Key）。
请在环境变量中配置以下任意一个：
- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `GLM_API_KEY`
- `DASHSCOPE_API_KEY`
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
