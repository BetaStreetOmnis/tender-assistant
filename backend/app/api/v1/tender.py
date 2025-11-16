"""
招标管理API路由
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.schemas.tender import TenderProjectCreate, TenderProjectResponse
from app.services.tender_service import TenderService

router = APIRouter(prefix="/tender")


@router.post("/upload", summary="上传招标文件")
async def upload_tender_document(
    file: UploadFile = File(...),
    project_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    上传招标文件并自动解析

    - **file**: 招标文件（PDF/Word）
    - **project_name**: 项目名称（可选）
    """
    service = TenderService(db)
    result = await service.upload_and_parse_document(file, project_name)
    return result


@router.get("/projects", summary="获取招标项目列表")
async def get_tender_projects(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取招标项目列表，支持分页和状态筛选"""
    service = TenderService(db)
    projects = await service.get_projects(page, page_size, status)
    return projects


@router.get("/projects/{project_id}", summary="获取招标项目详情")
async def get_tender_project_detail(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """获取招标项目详细信息"""
    service = TenderService(db)
    project = await service.get_project_detail(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


@router.post("/projects/{project_id}/analyze", summary="分析招标需求")
async def analyze_tender_requirements(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    使用AI分析招标文件，提取需求信息

    - 提取技术要求
    - 提取商务要求
    - 识别废标条款
    - 生成需求清单
    """
    service = TenderService(db)
    result = await service.analyze_requirements(project_id)
    return result


@router.delete("/projects/{project_id}", summary="删除招标项目")
async def delete_tender_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """删除招标项目及相关数据"""
    service = TenderService(db)
    await service.delete_project(project_id)
    return {"message": "删除成功"}