"""
投标管理API路由 - 优化版
"""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from pathlib import Path
import json
import logging

from app.core.deps import get_db, get_bidding_service, get_tender_analysis_service
from app.schemas.bidding import BidResponseCreate, BidResponseResponse
from app.schemas.response import (
    ApiResponse, TemplateInfo, TenderAnalysisResult, 
    OutlineResult, DocumentResult
)
from app.business.services.document_service import BiddingDocumentService, TenderAnalysisService
from app.models.bidding import BidResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bidding", tags=["投标管理"])


# ==================== 演示接口 ====================

@router.get("/demo", summary="投标管理演示")
async def demo():
    """演示投标管理功能"""
    return ApiResponse(
        data={
            "message": "🎉 投标管理模块已集成DocuGen功能！",
            "features": [
                "✅ 招标文档智能分析",
                "✅ 自动生成投标大纲",
                "✅ 基于大纲生成完整文档",
                "✅ 模板化文档生成",
                "✅ 自定义模板管理",
                "✅ 投标响应全流程管理"
            ],
            "endpoints": {
                "templates": "GET /api/v1/bidding/templates",
                "analyze": "POST /api/v1/bidding/analyze-tender",
                "outline": "POST /api/v1/bidding/generate-outline",
                "document": "POST /api/v1/bidding/generate-document"
            }
        },
        message="系统功能完整，可以开始使用"
    )


# ==================== 模板管理 ====================

@router.get("/templates", summary="获取投标模板列表")
async def get_templates(
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """获取可用的投标模板列表"""
    try:
        templates = service.list_templates()
        return ApiResponse(
            data={
                "templates": [TemplateInfo(name=t) for t in templates],
                "count": len(templates)
            },
            message="获取模板列表成功"
        )
    except Exception as e:
        logger.error(f"获取模板列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取模板失败: {str(e)}"
        )


@router.post("/upload-template", summary="上传自定义模板")
async def upload_template(
    file: UploadFile = File(...),
    name: str = Form(..., description="模板名称"),
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """上传自定义投标模板"""
    # 验证文件格式
    if not file.filename or not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 .docx 格式的模板文件"
        )
    
    # 验证模板名称
    if not name or len(name) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="模板名称至少需要2个字符"
        )
    
    try:
        content = await file.read()
        result = service.upload_template(name, content)
        
        logger.info(f"模板上传成功: {name}")
        return ApiResponse(
            data=result,
            message="模板上传成功"
        )
    except Exception as e:
        logger.error(f"上传模板失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传模板失败: {str(e)}"
        )


@router.get("/templates/{template_name}/variables", summary="获取模板变量")
async def get_template_variables(
    template_name: str,
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """获取指定模板的变量列表"""
    try:
        variables = service.get_template_variables(template_name)
        return ApiResponse(
            data=TemplateInfo(
                name=template_name,
                variables=variables
            ),
            message="获取模板变量成功"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"模板 '{template_name}' 不存在"
        )
    except Exception as e:
        logger.error(f"获取模板变量失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取模板变量失败: {str(e)}"
        )


# ==================== 招标分析 ====================

@router.post("/analyze-tender", summary="分析招标文档")
async def analyze_tender(
    tender_content: str = Form(..., description="招标文档内容"),
    analysis_service: TenderAnalysisService = Depends(get_tender_analysis_service)
):
    """分析招标文档，提取关键信息和要点"""
    if len(tender_content) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="招标文档内容太短，请提供更详细的信息"
        )
    
    try:
        # 分析招标需求
        analysis_result = await analysis_service.analyze_requirements(tender_content)
        
        # 提取关键要点
        key_points = await analysis_service.extract_key_points(tender_content)
        
        logger.info("招标文档分析完成")
        return ApiResponse(
            data=TenderAnalysisResult(
                analysis=analysis_result.get("analysis", ""),
                key_points=key_points
            ),
            message="招标文档分析完成"
        )
    except Exception as e:
        logger.error(f"分析失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分析失败: {str(e)}"
        )


# ==================== 大纲生成 ====================

@router.post("/generate-outline", summary="生成投标大纲")
async def generate_outline(
    tender_requirements: str = Form(..., description="招标需求"),
    key_points: Optional[str] = Form(None, description="关键要点"),
    rag_content: Optional[str] = Form(None, description="参考内容"),
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """根据招标需求生成投标大纲"""
    try:
        result = await service.generate_outline(
            tender_requirements=tender_requirements,
            key_points=key_points,
            rag_content=rag_content
        )
        
        logger.info("投标大纲生成成功")
        return ApiResponse(
            data=result,
            message="投标大纲生成成功"
        )
    except Exception as e:
        logger.error(f"生成大纲失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成大纲失败: {str(e)}"
        )


# ==================== 文档生成 ====================

@router.post("/generate-document", summary="生成投标文档")
async def generate_document(
    outline: str = Form(..., description="文档大纲"),
    tender_requirements: str = Form(..., description="招标需求"),
    rag_content: Optional[str] = Form(None, description="参考内容"),
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """根据大纲生成完整的投标文档"""
    try:
        file_path = await service.generate_document(
            outline=outline,
            tender_requirements=tender_requirements,
            rag_content=rag_content
        )
        
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="文档生成失败，请重试"
            )
        
        logger.info(f"投标文档生成成功: {file_path}")
        return ApiResponse(
            data=DocumentResult(
                file_path=file_path,
                download_url=f"/api/v1/bidding/download/{Path(file_path).name}"
            ),
            message="投标文档生成成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成文档失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成文档失败: {str(e)}"
        )


@router.post("/generate-from-template", summary="基于模板生成文档")
async def generate_from_template(
    template_name: str = Form(..., description="模板名称"),
    data: str = Form(..., description="填充数据（JSON格式）"),
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """使用指定模板生成投标文档"""
    # 解析JSON数据
    try:
        fill_data = json.loads(data)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"数据格式错误: {str(e)}"
        )
    
    try:
        file_path = await service.generate_from_template(
            template_name=template_name,
            data=fill_data
        )
        
        logger.info(f"模板文档生成成功: {template_name}")
        return ApiResponse(
            data=DocumentResult(
                file_path=file_path,
                download_url=f"/api/v1/bidding/download/{Path(file_path).name}"
            ),
            message="模板文档生成成功"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"模板 '{template_name}' 不存在"
        )
    except Exception as e:
        logger.error(f"生成文档失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成文档失败: {str(e)}"
        )


@router.post("/templates/{template_name}/ai-fill", summary="AI自动填充模板变量")
async def ai_fill_template_variables(
    template_name: str,
    context: str = Form(..., description="上下文信息"),
    service: BiddingDocumentService = Depends(get_bidding_service)
):
    """使用AI根据上下文自动填充模板变量"""
    try:
        result = service.ai_fill_template_variables(template_name, context)
        return ApiResponse(
            data=result,
            message="AI变量填充完成"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"模板 '{template_name}' 不存在"
        )
    except Exception as e:
        logger.error(f"AI填充失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI填充失败: {str(e)}"
        )


# ==================== 投标响应管理 ====================

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
        
        logger.info(f"投标响应创建成功: {bid_response.id}")
        return ApiResponse(
            data={
                "id": str(bid_response.id),
                "title": bid_response.title,
                "status": bid_response.status
            },
            message="投标响应创建成功"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建投标响应失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建失败: {str(e)}"
        )


@router.get("/responses", summary="获取投标响应列表")
async def get_bid_responses(
    page: int = 1,
    page_size: int = 20,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取投标响应列表"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="页码必须大于0"
        )
    
    try:
        skip = (page - 1) * page_size
        query = db.query(BidResponse)
        
        if status_filter:
            query = query.filter(BidResponse.status == status_filter)
        
        total = query.count()
        responses = query.offset(skip).limit(page_size).all()
        
        return ApiResponse(
            data={
                "items": [
                    {
                        "id": str(resp.id),
                        "tender_id": str(resp.tender_id) if resp.tender_id else None,
                        "title": resp.title,
                        "status": resp.status,
                        "created_at": resp.created_at.isoformat() if resp.created_at else None,
                        "updated_at": resp.updated_at.isoformat() if resp.updated_at else None
                    }
                    for resp in responses
                ],
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": (total + page_size - 1) // page_size
            },
            message="获取投标响应列表成功"
        )
    except Exception as e:
        logger.error(f"获取列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取列表失败: {str(e)}"
        )


@router.get("/responses/{response_id}", summary="获取投标响应详情")
async def get_bid_response(
    response_id: UUID,
    db: Session = Depends(get_db)
):
    """获取投标响应详细信息"""
    try:
        response = db.query(BidResponse).filter(BidResponse.id == response_id).first()
        
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"投标响应 '{response_id}' 不存在"
            )
        
        return ApiResponse(
            data={
                "id": str(response.id),
                "tender_id": str(response.tender_id) if response.tender_id else None,
                "title": response.title,
                "status": response.status,
                "content": response.content,
                "created_at": response.created_at.isoformat() if response.created_at else None,
                "updated_at": response.updated_at.isoformat() if response.updated_at else None
            },
            message="获取响应详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取详情失败: {str(e)}"
        )


# ==================== 文件下载 ====================

@router.get("/download/{filename}", summary="下载文档")
async def download_document(filename: str):
    """下载生成的投标文档"""
    # 安全检查：防止路径遍历攻击
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的文件名"
        )
    
    # 查找文件
    download_dir = Path("./downloads")
    file_path = download_dir / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文件 '{filename}' 不存在"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
