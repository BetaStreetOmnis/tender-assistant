"""
FastAPI 主应用入口 - 简化版
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import bidding
from app.api.v1 import template
# from app.api.v1 import knowledge  # 暂时注释掉，因为该模块不存在


# 创建FastAPI应用
app = FastAPI(
    title="AI标书助理系统",
    description="基于DocuGen的智能投标文档生成平台",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(bidding.router, prefix="/api/v1", tags=["投标管理"])
app.include_router(template.router, prefix="/api/v1", tags=["模板管理"])
# app.include_router(knowledge.router, prefix="/api/v1", tags=["知识库管理"])  # 暂时注释掉

@app.get("/", summary="根路径")
async def root():
    """系统信息"""
    return {
        "message": "🎯 AI标书助理系统",
        "description": "基于DocuGen的智能投标文档生成平台",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "✅ 招标文档智能分析",
            "✅ 投标大纲自动生成",
            "✅ 完整文档AI生成",
            "✅ 模板化文档管理",
            "✅ 实时API演示"
        ],
        "endpoints": {
            "demo": "/api/v1/bidding/demo",
            "templates": "/api/v1/bidding/templates",
            "analyze": "/api/v1/bidding/analyze-tender",
            "docs": "/docs"
        }
    }


@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "AI标书助理系统"
    }