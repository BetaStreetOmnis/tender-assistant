"""
模板管理API路由
"""
import os
import json
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse

# 导入 DocuGen 模块
from app.docgen.base_templates_generator import BaseTemplatesGenerator
from app.docgen.generator_doc import DocumentGenerator

router = APIRouter(prefix="/template", tags=["模板管理"])

# 创建必要的目录
TEMPLATES_DIR = Path("storage/templates")
DOWNLOADS_DIR = Path("storage/downloads")
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# 延迟初始化服务（避免在导入时初始化）
def get_template_processor():
    """获取模板处理器实例"""
    return BaseTemplatesGenerator(model_type="third_party")

def get_document_generator():
    """获取文档生成器实例"""
    return DocumentGenerator(model_type="third_party")


@router.get("/list")
async def list_templates():
    """
    获取所有可用的模板列表
    """
    try:
        processor = get_template_processor()
        templates_list = processor.list_templates()
        return JSONResponse(content={"success": True, "templates": templates_list})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/upload")
async def upload_template(
    template_name: str = Form(...),
    template_file: UploadFile = File(...),
    description: str = Form("")
):
    """
    上传Word文档模板文件
    """
    try:
        # 确保文件名安全
        safe_template_name = "".join(c for c in template_name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
        if not safe_template_name:
            safe_template_name = "uploaded_template"

        file_path = TEMPLATES_DIR / f"{safe_template_name}.docx"

        # 保存上传的文件
        content = await template_file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # 注册模板并提取变量
        processor = get_template_processor()
        template_metadata = processor.register_uploaded_template(
            str(file_path),
            template_name,
            description
        )

        return JSONResponse(content={
            "success": True,
            "filename": file_path.name,
            "template_name": template_name,
            "variables": template_metadata.get("variables", [])
        })

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.get("/variables")
async def get_template_variables(template_name: str):
    """
    获取指定模板中的变量列表
    """
    try:
        template_filename = f"{template_name}.docx"
        template_path = TEMPLATES_DIR / template_filename

        if not template_path.exists():
            return JSONResponse(
                content={"success": False, "error": f"模板文件 '{template_filename}' 不存在"},
                status_code=404
            )

        processor = get_template_processor()
        variables = processor.extract_variables_from_template(str(template_path))

        return JSONResponse(content={
            "success": True,
            "template_name": template_name,
            "variables": variables
        })

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/generate-from-template")
async def generate_from_template(
    template_name: str = Form(...),
    data: str = Form(...),  # JSON格式的数据字符串
    use_rag: bool = Form(False)
):
    """
    根据指定的模板和提供的JSON数据生成文档
    """
    try:
        data_dict = json.loads(data)

        # 如果启用RAG，获取相关知识库内容
        rag_content = None
        if use_rag:
            # TODO: 集成 RAG 知识库
            pass

        processor = get_template_processor()
        file_path = processor.generate_from_template(
            template_name,
            data_dict,
            rag_content
        )

        filename = os.path.basename(file_path)
        return JSONResponse(content={
            "success": True,
            "filename": filename,
            "download_url": f"/api/v1/template/download/{filename}"
        })

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/generate-outline")
async def generate_outline(
    topic: str = Form(...),
    key_points: Optional[str] = Form(None),
    use_rag: bool = Form(False)
):
    """
    根据主题和关键词生成文档大纲
    """
    try:
        rag_content = None
        if use_rag:
            # TODO: 集成 RAG 知识库
            pass

        generator = get_document_generator()
        result = generator.generate_outline(topic, key_points, rag_content)
        return JSONResponse(content={"success": True, **result})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/generate-fulltext")
async def generate_fulltext(
    outline: str = Form(...),
    key_points: Optional[str] = Form(None),
    use_rag: bool = Form(False)
):
    """
    根据大纲生成完整文档
    """
    try:
        rag_content = None
        if use_rag:
            # TODO: 集成 RAG 知识库
            pass

        generator = get_document_generator()
        result = generator.start_fulltext_generation(outline, key_points, rag_content)
        return JSONResponse(content={"success": True, **result})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.get("/generation-status/{task_id}")
async def get_generation_status(task_id: str):
    """
    获取文档生成状态
    """
    try:
        generator = get_document_generator()
        result = generator.get_generation_status(task_id)
        return JSONResponse(content={"success": True, **result})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/process-next-section/{task_id}")
async def process_next_section(task_id: str):
    """
    处理下一个章节
    """
    try:
        generator = get_document_generator()
        result = generator.process_next_section(task_id)
        return JSONResponse(content={"success": True, **result})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.post("/export-word")
async def export_word(
    content: str = Form(...),
    content_type: str = Form("outline")  # outline 或 fulltext
):
    """
    将内容导出为Word文档
    """
    try:
        generator = get_document_generator()
        file_path = generator.export_to_doc(content, content_type)
        filename = os.path.basename(file_path)
        return JSONResponse(content={
            "success": True,
            "filename": filename,
            "download_url": f"/api/v1/template/download/{filename}"
        })

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    下载生成的文档
    """
    # 首先尝试从 downloads 目录查找
    file_path = DOWNLOADS_DIR / filename

    # 如果不存在，尝试从 storage/downloads 查找
    if not file_path.exists():
        file_path = Path("storage") / "downloads" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    # 根据文件扩展名确定媒体类型
    if filename.lower().endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.lower().endswith(".pdf"):
        media_type = "application/pdf"
    else:
        media_type = "application/octet-stream"

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type
    )


@router.delete("/delete/{template_name}")
async def delete_template(template_name: str):
    """
    删除模板
    """
    try:
        template_path = TEMPLATES_DIR / f"{template_name}.docx"

        if not template_path.exists():
            return JSONResponse(
                content={"success": False, "error": "模板不存在"},
                status_code=404
            )

        template_path.unlink()

        return JSONResponse(content={"success": True, "message": "模板已删除"})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
