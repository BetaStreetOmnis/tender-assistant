"""
基于真实DocuGen的文档生成服务
"""
import os
import json
import time
import uuid
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import requests

from .real_llm_client import RealLLMClient


class RealDocumentGenerator:
    """真正的文档生成器 - 基于DocuGen实现"""

    def __init__(self):
        self.llm_client = RealLLMClient()
        self.active_generations = {}

        # 创建必要的目录
        Path("storage/downloads").mkdir(parents=True, exist_ok=True)
        Path("storage/generated").mkdir(parents=True, exist_ok=True)
        Path("storage/templates").mkdir(parents=True, exist_ok=True)

    def generate_outline(self, topic: str, key_points: str = None, rag_content: str = None) -> Dict[str, Any]:
        """根据主题生成大纲"""
        if not topic:
            raise ValueError("主题不能为空")

        # 构建提示，基于DocuGen的实现
        prompt = f"请为主题'{topic}'生成一个详细的、结构化的大纲。大纲应包含章节标题和子章节，以及每个部分的简要说明。请确保大纲逻辑清晰，结构合理。格式要求：1.使用Markdown格式编写，2.使用#、##、###表示不同层级的标题，3.每个子章节可以用1-2句话描述其内容要点。"

        # 如果有重点提要，加入提示
        if key_points and key_points.strip():
            prompt += f"\n\n请务必确保大纲围绕以下关键点展开：\n{key_points}\n\n这些要点必须体现在大纲的相应章节中。"

        # 如果有RAG参考内容，加入提示
        if rag_content and rag_content.strip():
            prompt += f"\n\n请参考以下内容来丰富大纲：\n{rag_content}\n\n请确保大纲内容与参考内容保持一致性和连贯性。"

        messages = [
            {"role": "system", "content": "你是一个专业的大纲生成助手，擅长创建结构化、有逻辑性的大纲。"},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.llm_client.chat(messages=messages)
            outline_text = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not outline_text:
                raise ValueError("模型返回内容为空")

            return {"outline": outline_text}

        except Exception as e:
            raise Exception(f"生成大纲时出错: {str(e)}")

    def start_document_generation(self, topic: str, outline: str, key_points: str = None, rag_content: str = None) -> str:
        """开始生成文档，返回任务ID"""
        task_id = str(uuid.uuid4())

        # 解析大纲为各个部分
        sections = self._parse_outline(outline)

        # 创建生成任务
        self.active_generations[task_id] = {
            "topic": topic,
            "outline": outline,
            "key_points": key_points,
            "rag_content": rag_content,
            "sections": sections,
            "sections_total": len(sections),
            "sections_completed": 0,
            "full_text": f"# {topic}\n\n",
            "progress": 0,
            "status": "in_progress",
            "created_at": time.time()
        }

        return task_id

    def process_next_section(self, task_id: str) -> Dict[str, Any]:
        """处理下一个大纲部分 - 基于DocuGen的真实实现"""
        if task_id not in self.active_generations:
            raise ValueError("生成任务不存在")

        task = self.active_generations[task_id]

        # 检查是否已完成所有部分
        if task["sections_completed"] >= task["sections_total"]:
            # 生成Word文档
            doc_path = self._create_word_document(task)
            return {
                "completed": True,
                "progress": 100,
                "status": "completed",
                "full_text": task["full_text"],
                "document_path": doc_path
            }

        # 获取下一个待处理部分
        section_index = task["sections_completed"]
        current_section = task["sections"][section_index]

        try:
            # 提取部分标题作为提示
            section_title = current_section.split("\n")[0] if "\n" in current_section else current_section

            # 构建提示，基于DocuGen的实现
            prompt = f"请根据以下大纲部分生成详细的文章内容。生成的内容应包含完整的段落，有充分的论述、解释和例子，而不仅仅是重复大纲内容。\n\n大纲部分:\n{current_section}\n\n"

            # 添加重点提要以确保内容不偏题
            if task.get("key_points") and task["key_points"].strip():
                prompt += f"\n重要：请确保生成的内容与以下关键点/核心要求相符合：\n{task['key_points']}\n\n请将这些要点自然地融入到内容中，确保内容紧扣主题而不偏离。\n\n"

            # 添加RAG参考内容
            if task.get("rag_content") and task["rag_content"].strip():
                prompt += f"\n参考内容:\n{task['rag_content']}\n\n请确保生成的内容与参考内容保持一致。\n\n"

            # 添加上下文以保持连贯性
            if task["full_text"]:
                # 提取最后一部分作为上下文
                last_part = task["full_text"].split("\n\n")[-3:] if "\n\n" in task["full_text"] else task["full_text"]
                last_part = "\n\n".join(last_part) if isinstance(last_part, list) else last_part
                prompt += f"已有内容作为上下文参考:\n{last_part}\n\n请确保新内容与已有内容保持连贯性。"

            messages = [
                {"role": "system", "content": "你是一位专业的内容撰写专家，擅长将大纲扩展为详细的文章内容。生成的内容应该结构清晰、论述充分、内容翔实。你会确保内容紧扣主题要点，不偏离核心内容。"},
                {"role": "user", "content": prompt}
            ]

            # 调用LLM生成内容
            response = self.llm_client.chat(messages=messages)
            section_text = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not section_text:
                section_text = "系统无法生成此部分内容，请稍后重试。"

            # 更新全文
            heading_level = section_title.count("#")
            formatted_title = section_title.replace("#", "").strip()

            # 格式化标题
            if heading_level == 1:
                formatted_section = f"\n\n## {formatted_title}\n\n{section_text}"
            elif heading_level == 2:
                formatted_section = f"\n\n### {formatted_title}\n\n{section_text}"
            else:
                formatted_section = f"\n\n#### {formatted_title}\n\n{section_text}"

            # 添加到全文
            task["full_text"] += formatted_section

            # 更新进度
            task["sections_completed"] += 1
            task["progress"] = int((task["sections_completed"] / task["sections_total"]) * 100)

            return {
                "completed": task["sections_completed"] >= task["sections_total"],
                "progress": task["progress"],
                "status": "completed" if task["sections_completed"] >= task["sections_total"] else "in_progress",
                "section_text": formatted_section,
                "current_section": current_section
            }

        except Exception as e:
            # 出错时，将状态设为错误
            task["status"] = "error"
            raise Exception(f"处理部分生成时出错: {str(e)}")

    def _parse_outline(self, outline: str) -> List[str]:
        """解析大纲为各个部分"""
        sections = []
        current_section = ""

        for line in outline.split('\n'):
            line = line.strip()
            if not line:
                continue

            # 检查是否是标题行
            if line.startswith('#'):
                if current_section:
                    sections.append(current_section.strip())
                current_section = line
            else:
                current_section += f"\n{line}"

        # 添加最后一个部分
        if current_section:
            sections.append(current_section.strip())

        return sections

    def _create_word_document(self, task: Dict[str, Any]) -> str:
        """创建Word文档"""
        try:
            doc = Document()

            # 设置标题样式
            title = doc.add_heading(task["topic"], level=1)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加生成时间
            doc.add_paragraph(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            doc.add_paragraph()

            # 解析markdown并添加到文档
            self._add_markdown_to_doc(doc, task["full_text"])

            # 保存文档
            timestamp = int(time.time())
            filename = f"generated_document_{timestamp}.docx"
            file_path = f"storage/generated/{filename}"

            doc.save(file_path)
            return file_path

        except Exception as e:
            # 如果Word生成失败，至少保存文本版本
            timestamp = int(time.time())
            filename = f"generated_document_{timestamp}.txt"
            file_path = f"storage/generated/{filename}"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(task["full_text"])

            return file_path

    def _add_markdown_to_doc(self, doc: Document, markdown_text: str):
        """将markdown文本添加到Word文档"""
        lines = markdown_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('# '):
                doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:], level=3)
            elif line.startswith('#### '):
                doc.add_heading(line[5:], level=4)
            else:
                if line:
                    doc.add_paragraph(line)

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        if task_id not in self.active_generations:
            raise ValueError("任务不存在")

        task = self.active_generations[task_id]
        return {
            "task_id": task_id,
            "progress": task["progress"],
            "status": task["status"],
            "sections_completed": task["sections_completed"],
            "sections_total": task["sections_total"]
        }


class RealTemplateProcessor:
    """真实的模板处理器 - 基于DocuGen的模板系统"""

    def __init__(self):
        self.llm_client = RealLLMClient()
        # 创建模板目录
        Path("storage/templates").mkdir(parents=True, exist_ok=True)

    def list_templates(self) -> List[str]:
        """列出所有可用的模板"""
        templates_dir = Path("storage/templates")
        templates = [f.stem for f in templates_dir.glob("*.docx")]
        return templates

    def extract_variables_from_template(self, template_name: str) -> List[Dict[str, str]]:
        """从Word模板中提取所有变量 - 支持【变量】和{{变量}}格式"""
        template_path = Path(f"storage/templates/{template_name}.docx")

        if not template_path.exists():
            raise FileNotFoundError(f"模板 {template_name} 不存在")

        try:
            doc = Document(template_path)
            variables = set()

            # 正则模式，匹配【变量】和{{变量}}
            pattern = r'【([^】]+?)】|\{\{([^}]+?)\}\}'

            # 提取段落中的变量
            for paragraph in doc.paragraphs:
                matches = re.findall(pattern, paragraph.text)
                for match in matches:
                    var_name = match[0] or match[1]  # 取非空的匹配
                    if var_name.strip():
                        variables.add(var_name.strip())

            # 提取表格中的变量
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            matches = re.findall(pattern, paragraph.text)
                            for match in matches:
                                var_name = match[0] or match[1]
                                if var_name.strip():
                                    variables.add(var_name.strip())

            # 转换为字典格式
            result = []
            for var in sorted(variables):
                result.append({
                    "name": var,
                    "description": f"模板变量: {var}",
                    "default_value": ""
                })

            return result

        except Exception as e:
            raise Exception(f"提取模板变量失败: {str(e)}")

    def _replace_text_in_paragraph(self, paragraph, data: Dict[str, Any]) -> None:
        """在段落中替换占位符，支持占位符被拆分到多个run中的情况"""
        # 获取完整的段落文本
        full_text = paragraph.text

        # 定义替换模式
        patterns = [
            (r'【([^】]+?)】', lambda m: str(data.get(m.group(1), m.group(0)))),
            (r'\{\{([^}]+?)\}\}', lambda m: str(data.get(m.group(1), m.group(0))))
        ]

        # 应用所有替换
        new_text = full_text
        for pattern, replacement in patterns:
            new_text = re.sub(pattern, replacement, new_text)

        # 如果文本有变化，重新设置段落内容
        if new_text != full_text:
            # 清除所有runs
            paragraph.clear()
            # 添加新文本
            paragraph.add_run(new_text)

    def _fill_template(self, doc: Document, data: Dict[str, Any]) -> None:
        """填充文档模板"""
        # 处理所有段落
        for paragraph in doc.paragraphs:
            self._replace_text_in_paragraph(paragraph, data)

        # 处理所有表格
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_text_in_paragraph(paragraph, data)

    def generate_from_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """根据模板和数据生成文档"""
        template_path = Path(f"storage/templates/{template_name}.docx")

        if not template_path.exists():
            raise FileNotFoundError(f"模板 {template_name} 不存在")

        try:
            # 加载模板文档
            doc = Document(template_path)

            # 填充模板
            self._fill_template(doc, data)

            # 保存为新文档
            timestamp = int(time.time())
            filename = f"template_generated_{template_name}_{timestamp}.docx"
            file_path = f"storage/generated/{filename}"

            doc.save(file_path)
            return file_path

        except Exception as e:
            raise Exception(f"模板生成失败: {str(e)}")

    def upload_template(self, template_name: str, file_content: bytes) -> Dict[str, Any]:
        """上传新模板文件"""
        try:
            # 保存文件
            template_path = Path(f"storage/templates/{template_name}.docx")
            template_path.write_bytes(file_content)

            # 提取变量
            variables = self.extract_variables_from_template(template_name)

            return {
                "message": f"模板 {template_name} 上传成功",
                "variables_found": len(variables),
                "variables": variables
            }

        except Exception as e:
            raise Exception(f"上传模板失败: {str(e)}")

    def ai_fill_template_variables(self, template_name: str, context: str) -> Dict[str, Any]:
        """使用AI自动填充模板变量"""
        try:
            # 提取模板变量
            variables = self.extract_variables_from_template(template_name)

            if not variables:
                return {"message": "模板中未发现变量"}

            # 构建AI提示
            var_list = "\n".join([f"- {var['name']}: {var['description']}" for var in variables])

            prompt = f"""
请根据以下上下文信息，为模板变量提供合适的值：

上下文信息：
{context}

需要填充的模板变量：
{var_list}

请返回JSON格式的变量值，例如：
{{
    "变量1": "对应的值",
    "变量2": "对应的值"
}}

请确保值与上下文相关且合理。
            """

            messages = [
                {"role": "system", "content": "你是专业的文档处理助手，擅长根据上下文为模板变量提供合适的值。"},
                {"role": "user", "content": prompt}
            ]

            response = self.llm_client.chat(messages=messages)
            ai_content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            # 尝试解析JSON
            try:
                # 提取JSON部分
                json_start = ai_content.find("{")
                json_end = ai_content.rfind("}") + 1

                if json_start >= 0 and json_end > json_start:
                    json_str = ai_content[json_start:json_end]
                    ai_values = json.loads(json_str)

                    return {
                        "variables": variables,
                        "ai_values": ai_values,
                        "message": "AI成功生成变量值"
                    }
                else:
                    # 如果无法解析JSON，返回原始内容
                    return {
                        "variables": variables,
                        "ai_content": ai_content,
                        "message": "AI生成了内容但无法解析为变量值"
                    }

            except json.JSONDecodeError:
                return {
                    "variables": variables,
                    "ai_content": ai_content,
                    "message": "AI生成了内容但格式不是有效的JSON"
                }

        except Exception as e:
            return {"error": f"AI填充变量失败: {str(e)}"}


class RealBiddingDocumentService:
    """真正的投标文档生成服务"""

    def __init__(self):
        self.document_generator = RealDocumentGenerator()
        self.template_processor = RealTemplateProcessor()
        self.llm_client = RealLLMClient()

    async def generate_outline(self, tender_requirements: str, key_points: str = None, rag_content: str = None) -> Dict[str, Any]:
        """生成投标大纲"""
        topic = f"基于以下招标需求的投标方案：\n{tender_requirements}"
        return self.document_generator.generate_outline(topic, key_points, rag_content)

    async def generate_document_async(self, outline: str, tender_requirements: str, rag_content: str = None) -> str:
        """异步生成完整投标文档"""
        topic = f"投标方案文档"

        # 开始文档生成任务
        task_id = self.document_generator.start_document_generation(
            topic=topic,
            outline=outline,
            key_points=tender_requirements,
            rag_content=rag_content
        )

        # 处理所有章节
        while True:
            result = self.document_generator.process_next_section(task_id)
            if result["completed"]:
                return result["document_path"]

            # 添加小延迟，模拟真实处理时间
            time.sleep(0.5)

    async def generate_document(self, outline: str, tender_requirements: str, rag_content: str = None) -> str:
        """生成完整投标文档"""
        try:
            return await self.generate_document_async(outline, tender_requirements, rag_content)
        except Exception as e:
            print(f"文档生成失败: {str(e)}")
            # 返回一个错误文档路径
            timestamp = int(time.time())
            return f"/storage/generated/error_{timestamp}.txt"

    def list_templates(self) -> List[str]:
        """获取可用模板列表 - 真实模板文件 + 内置模板"""
        # 获取真实上传的模板
        real_templates = self.template_processor.list_templates()

        # 内置演示模板
        builtin_templates = [
            "软件开发投标模板",
            "系统集成投标模板",
            "IT咨询服务模板",
            "网站建设投标模板",
            "数据库项目模板",
            "移动应用开发模板"
        ]

        # 合并模板列表
        return real_templates + builtin_templates

    def get_template_variables(self, template_name: str) -> List[Dict[str, str]]:
        """获取模板变量"""
        return self.template_processor.extract_variables_from_template(template_name)

    def generate_from_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """从模板生成文档"""
        return self.template_processor.generate_from_template(template_name, data)

    def upload_template(self, template_name: str, file_content: bytes) -> Dict[str, Any]:
        """上传模板文件"""
        return self.template_processor.upload_template(template_name, file_content)

    def ai_fill_template_variables(self, template_name: str, context: str) -> Dict[str, Any]:
        """AI自动填充模板变量"""
        return self.template_processor.ai_fill_template_variables(template_name, context)