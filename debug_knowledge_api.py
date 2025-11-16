#!/usr/bin/env python3
"""
调试知识库API响应格式
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def debug_knowledge_upload():
    """调试知识库上传API"""
    print("🔍 调试知识库上传API")
    print("=" * 50)

    upload_data = {
        "title": "调试测试文档",
        "content": "这是一个调试测试文档内容",
        "category": "通用"
    }

    print("📤 请求数据:")
    print(json.dumps(upload_data, indent=2, ensure_ascii=False))

    print(f"\n🌐 请求URL: {BASE_URL}/api/v1/knowledge/upload")

    try:
        response = requests.post(f"{BASE_URL}/api/v1/knowledge/upload", json=upload_data)

        print(f"\n📊 响应状态码: {response.status_code}")
        print(f"📋 响应头:")
        for key, value in response.headers.items():
            print(f"   {key}: {value}")

        print(f"\n📄 响应内容:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))

            # 检查响应结构
            if 'code' in response_json:
                print(f"\n✅ 响应包含 'code' 字段: {response_json['code']}")
            else:
                print(f"\n❌ 响应缺少 'code' 字段")

            if 'data' in response_json:
                print(f"✅ 响应包含 'data' 字段")
                data = response_json['data']
                if isinstance(data, dict):
                    print(f"   data字段包含: {list(data.keys())}")
                else:
                    print(f"   data类型: {type(data)}")
            else:
                print(f"❌ 响应缺少 'data' 字段")

            if 'message' in response_json:
                print(f"✅ 响应包含 'message' 字段: {response_json['message']}")

        except json.JSONDecodeError:
            print("❌ 响应不是有效的JSON格式")
            print(f"原始内容: {response.text}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

def debug_knowledge_list():
    """调试知识库列表API"""
    print("\n🔍 调试知识库列表API")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/api/v1/knowledge/list")

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            response_json = response.json()
            print("✅ 列表API响应结构:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False)[:500] + "..." if len(str(response_json)) > 500 else json.dumps(response_json, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 列表API失败: {response.text}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    debug_knowledge_list()
    debug_knowledge_upload()