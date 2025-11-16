"""
简化版FastAPI启动 - 用于测试
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AI标书助理系统",
    description="智能招投标文档管理系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI标书助理系统",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "tender-assistant"
    }


@app.get("/api/v1/test")
async def test_api():
    """测试API"""
    return {
        "success": True,
        "message": "API运行正常",
        "data": {
            "modules": [
                "招标管理",
                "投标管理",
                "模板管理",
                "智能检查"
            ]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
