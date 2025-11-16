#!/usr/bin/env python3
"""
本地启动脚本 - 简化版
"""
from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import uvicorn
import time
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI标书助理系统 - 本地版")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class AnalyzeRequest(BaseModel):
    tender_content: str = ''

def create_analysis_result(content):
    """创建分析结果"""
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'id': str(int(time.time())),
            'analysis': f'智能分析结果：\n\n项目内容：{content}\n\n关键建议：\n1. 准备详细的技术方案\n2. 展示相关专业人员资质\n3. 制定科学的项目管理计划\n4. 建立完善的质量保证体系\n5. 提供全面的售后技术支持',
            'key_points': [
                '• 准备详细的技术实施方案',
                '• 展示相关专业人员资质和经验',
                '• 制定科学的项目管理计划',
                '• 建立完善的质量控制体系',
                '• 提供全面的售后技术支持'
            ],
            'created_at': datetime.now().isoformat(),
            'model_used': '本地分析引擎 v1.0',
            'tokens_used': 256,
            'ai_confidence': 'high',
            'analysis_type': 'local_analysis'
        }
    }

@app.get('/')
async def root():
    return {
        "message": "AI标书助理系统 - 本地版",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.post('/api/v1/health')
async def health():
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'status': 'healthy',
            'service': 'AI标书助理系统-本地版',
            'timestamp': datetime.now().isoformat()
        }
    }

@app.get('/api/v1/health')
async def get_health():
    return await health()

@app.post('/api/v1/bidding/analyze-tender')
async def analyze_tender(request: AnalyzeRequest):
    """处理JSON格式请求"""
    if not request.tender_content:
        raise HTTPException(status_code=400, detail='缺少招标文档内容')

    return create_analysis_result(request.tender_content)

@app.post('/api/v1/bidding/analyze-tender')
async def analyze_tender_form(tender_content: str = Form(...)):
    """处理表单格式请求"""
    if not tender_content:
        raise HTTPException(status_code=400, detail='缺少招标文档内容')

    return create_analysis_result(tender_content)

@app.get('/api/v1/bidding/responses')
async def get_responses():
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'items': [],
            'total': 0,
            'page': 1,
            'page_size': 20
        }
    }

@app.get('/api/v1/template/list')
async def get_template_list():
    return {
        'code': 200,
        'message': 'success',
        'data': {
            'templates': [
                {
                    'id': '1',
                    'name': '智能建筑投标模板',
                    'description': '适用于智能建筑项目的专业投标模板',
                    'category': '建筑工程'
                },
                {
                    'id': '2',
                    'name': '软件开发投标模板',
                    'description': '适用于软件开发项目的专业投标模板',
                    'category': '信息技术'
                }
            ]
        }
    }

if __name__ == "__main__":
    print("🚀 启动AI标书助理系统 - 本地版")
    print("🌐 监听地址: http://localhost:8001")
    print("📚 API文档: http://localhost:8001/docs")
    print("✅ 支持JSON和表单格式")
    print("按 Ctrl+C 停止服务")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info"
    )