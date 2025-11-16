"""
应用配置管理
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    APP_NAME: str = "tender-assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    # 数据库配置
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Redis配置
    REDIS_URL: str
    REDIS_PASSWORD: str = ""

    # Milvus配置
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    MILVUS_USER: str = ""
    MILVUS_PASSWORD: str = ""

    # Neo4j配置
    NEO4J_URI: str = ""
    NEO4J_USER: str = ""
    NEO4J_PASSWORD: str = ""

    # LLM配置
    DASHSCOPE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    # 文件存储
    UPLOAD_DIR: str = "storage/uploads"
    TEMPLATE_DIR: str = "storage/templates"
    GENERATED_DIR: str = "storage/generated"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB

    # Celery配置
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # JWT配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # 业务配置
    DEFAULT_TEMPLATE_TYPE: str = "software"
    MAX_RAG_RESULTS: int = 10
    ENABLE_KNOWLEDGE_GRAPH: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'  # 忽略未定义的环境变量（允许 DocuGen 等模块使用自己的配置）
    )


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()