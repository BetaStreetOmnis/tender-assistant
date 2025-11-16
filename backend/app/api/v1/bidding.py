"""
投标管理API路由 - 集成DocuGen功能
"""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from pathlib import Path

from app.db.session import get_db
from app.schemas.bidding import BidResponseCreate, BidResponseResponse
from app.business.services.document_service import BiddingDocumentService, TenderAnalysisService
from app.models.bidding import BidResponse

router = APIRouter(prefix="/bidding", tags=["投标管理"])

# 服务实例
bidding_service = BiddingDocumentService()
tender_analysis_service = TenderAnalysisService()


@router.get("/demo", summary="投标管理演示")
async def demo():
    """演示投标管理功能"""
    return {
        "code": 200,
        "data": {
            "message": "🎉 投标管理模块已集成DocuGen功能！",
            "features": [
                "✅ 招标文档智能分析",
                "✅ 自动生成投标大纲",
                "✅ 基于大纲生成完整文档",
                "✅ 模板化文档生成",
                "✅ 自定义模板管理",
                "✅ 投标响应全流程管理"
            ],
            "available_apis": [
                "GET /bidding/templates - 获取模板列表",
                "POST /bidding/analyze-tender - 分析招标文档",
                "POST /bidding/generate-outline - 生成投标大纲",
                "POST /bidding/generate-document - 生成投标文档",
                "POST /bidding/upload-template - 上传自定义模板",
                "GET /bidding/templates/{name}/variables - 获取模板变量",
                "POST /bidding/templates/{name}/ai-fill - AI自动填充变量",
                "POST /bidding/templates/{name}/generate - 基于模板生成文档",
                "POST /bidding/generate-from-template - 通用模板生成"
            ]
        },
        "message": "系统功能完整，可以开始使用"
    }


@router.get("/templates", summary="获取投标模板列表")
async def get_templates():
    """获取可用的投标模板列表"""
    try:
        templates = bidding_service.list_templates()
        return {
            "code": 200,
            "data": {
                "templates": templates,
                "count": len(templates)
            },
            "message": "获取模板列表成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模板失败: {str(e)}")


@router.post("/analyze-tender", summary="分析招标文档")
async def analyze_tender(
    tender_content: str = Form(..., description="招标文档内容")
):
    """分析招标文档，提取关键信息和要点"""
    try:
        # 分析招标需求
        analysis_result = await tender_analysis_service.analyze_requirements(tender_content)

        # 提取关键要点
        key_points = await tender_analysis_service.extract_key_points(tender_content)

        return {
            "code": 200,
            "data": {
                "analysis": analysis_result["analysis"],
                "key_points": key_points
            },
            "message": "招标文档分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.post("/generate-outline", summary="生成投标大纲")
async def generate_outline(
    tender_requirements: str = Form(..., description="招标需求"),
    key_points: str = Form(None, description="关键要点"),
    rag_content: str = Form(None, description="参考内容")
):
    """根据招标需求生成投标大纲"""
    try:
        result = await bidding_service.generate_outline(
            tender_requirements=tender_requirements,
            key_points=key_points,
            rag_content=rag_content
        )

        return {
            "code": 200,
            "data": result,
            "message": "投标大纲生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成大纲失败: {str(e)}")


@router.post("/generate-document", summary="生成投标文档")
async def generate_document(
    outline: str = Form(..., description="文档大纲"),
    tender_requirements: str = Form(..., description="招标需求"),
    rag_content: str = Form(None, description="参考内容")
):
    """根据大纲生成完整的投标文档"""
    try:
        file_path = await bidding_service.generate_document(
            outline=outline,
            tender_requirements=tender_requirements,
            rag_content=rag_content
        )

        return {
            "code": 200,
            "data": {
                "file_path": file_path,
                "download_url": f"/download/{Path(file_path).name}" if file_path else None
            },
            "message": "投标文档生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成文档失败: {str(e)}")


@router.post("/generate-from-template", summary="基于模板生成文档")
async def generate_from_template(
    template_name: str = Form(..., description="模板名称"),
    data: str = Form(..., description="填充数据（JSON格式）")
):
    """使用指定模板生成投标文档"""
    try:
        import json
        fill_data = json.loads(data)

        file_path = await bidding_service.generate_from_template(
            template_name=template_name,
            data=fill_data
        )

        return {
            "code": 200,
            "data": {
                "file_path": file_path,
                "download_url": f"/download/{Path(file_path).name}"
            },
            "message": "模板文档生成成功"
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="数据格式错误，请提供有效的JSON格式")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成文档失败: {str(e)}")


@router.post("/upload-template", summary="上传自定义模板")
async def upload_template(
    file: UploadFile = File(...),
    name: str = Form(..., description="模板名称")
):
    """上传自定义投标模板"""
    try:
        if not file.filename.endswith('.docx'):
            raise HTTPException(status_code=400, detail="只支持.docx格式的模板文件")

        # 使用服务类的上传功能
        content = await file.read()
        result = bidding_service.upload_template(name, content)

        return {
            "code": 200,
            "data": result,
            "message": "模板上传成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传模板失败: {str(e)}")


@router.get("/templates/{template_name}/variables", summary="获取模板变量")
async def get_template_variables(template_name: str):
    """获取指定模板的变量列表"""
    try:
        variables = bidding_service.get_template_variables(template_name)
        return {
            "code": 200,
            "data": {
                "template_name": template_name,
                "variables": variables,
                "count": len(variables)
            },
            "message": "获取模板变量成功"
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"模板 {template_name} 不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模板变量失败: {str(e)}")


@router.post("/templates/{template_name}/ai-fill", summary="AI自动填充模板变量")
async def ai_fill_template_variables(
    template_name: str,
    context: str = Form(..., description="上下文信息")
):
    """使用AI根据上下文自动填充模板变量"""
    try:
        result = bidding_service.ai_fill_template_variables(template_name, context)
        return {
            "code": 200,
            "data": result,
            "message": "AI变量填充完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI填充失败: {str(e)}")


@router.post("/templates/{template_name}/generate", summary="使用模板生成文档")
async def generate_from_specific_template(
    template_name: str,
    variables: str = Form(..., description="变量值（JSON格式）")
):
    """使用指定模板和变量值生成文档"""
    try:
        import json
        variable_data = json.loads(variables)

        file_path = bidding_service.generate_from_template(template_name, variable_data)

        return {
            "code": 200,
            "data": {
                "file_path": file_path,
                "download_url": f"/download/{Path(file_path).name}",
                "template_used": template_name
            },
            "message": "基于模板的文档生成成功"
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="变量数据格式错误，请提供有效的JSON格式")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"模板 {template_name} 不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档生成失败: {str(e)}")


# 原有的投标响应管理API
@router.post("/responses", summary="创建投标响应")
async def create_bid_response(
    data: BidResponseCreate,
    db: Session = Depends(get_db)
):
    """创建投标响应文档"""
    try:
        bid_response = BidResponse(**data.model_dump())
        db.add(bid_response)
        db.commit()
        db.refresh(bid_response)

        return {
            "code": 200,
            "data": {
                "id": bid_response.id,
                "title": bid_response.title,
                "status": bid_response.status
            },
            "message": "投标响应创建成功"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/responses", summary="获取投标响应列表")
async def get_bid_responses(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取投标响应列表"""
    try:
        skip = (page - 1) * page_size
        query = db.query(BidResponse)

        if status:
            query = query.filter(BidResponse.status == status)

        responses = query.offset(skip).limit(page_size).all()
        total = query.count()

        return {
            "code": 200,
            "data": {
                "items": [
                    {
                        "id": resp.id,
                        "tender_id": resp.tender_id,
                        "title": resp.title,
                        "status": resp.status,
                        "created_at": resp.created_at,
                        "updated_at": resp.updated_at
                    }
                    for resp in responses
                ],
                "total": total,
                "page": page,
                "page_size": page_size
            },
            "message": "获取投标响应列表成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取列表失败: {str(e)}")


@router.get("/responses/{response_id}", summary="获取投标响应详情")
async def get_bid_response(
    response_id: UUID,
    db: Session = Depends(get_db)
):
    """获取投标响应详细信息"""
    try:
        response = db.query(BidResponse).filter(BidResponse.id == response_id).first()
        if not response:
            raise HTTPException(status_code=404, detail="投标响应不存在")

        return {
            "code": 200,
            "data": {
                "id": response.id,
                "tender_id": response.tender_id,
                "title": response.title,
                "status": response.status,
                "content": response.content,
                "created_at": response.created_at,
                "updated_at": response.updated_at
            },
            "message": "获取响应详情成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情失败: {str(e)}")