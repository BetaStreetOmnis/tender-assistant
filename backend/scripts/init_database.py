#!/usr/bin/env python3
"""
数据库初始化脚本
"""
import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'tender_assistant')

def create_database():
    """创建数据库"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )

        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 '{DB_NAME}' 创建成功或已存在")

            # 使用数据库
            cursor.execute(f"USE {DB_NAME}")

            # 创建投标响应表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bid_responses (
                    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
                    tender_id VARCHAR(100),
                    title VARCHAR(255) NOT NULL,
                    status ENUM('draft', 'in_progress', 'completed', 'submitted') DEFAULT 'draft',
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_status (status),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ 投标响应表创建成功")

            # 插入示例数据
            cursor.execute("""
                INSERT IGNORE INTO bid_responses (id, title, status, content) VALUES
                ('550e8400-e29b-41d4-a716-446655440001', '软件开发项目投标', 'draft', '这是一个软件开发项目的投标响应草稿'),
                ('550e8400-e29b-41d4-a716-446655440002', '系统集成项目投标', 'completed', '这是一个系统集成项目的完整投标响应'),
                ('550e8400-e29b-41d4-a716-446655440003', '咨询���务项目投标', 'in_progress', '这是一个咨询服务项目的投标响应，正在进行中')
            """)
            print("✅ 示例数据插入成功")

        connection.commit()
        print(f"🎉 数据库初始化完成！")

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    print(f"正在连接到数据库: {DB_HOST}:{DB_PORT}")
    print(f"用户名: {DB_USER}")
    print(f"数据库名: {DB_NAME}")
    print("-" * 50)
    create_database()