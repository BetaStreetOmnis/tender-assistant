#!/usr/bin/env python3
import requests
import json

def test_api():
    # 测试获取模板列表
    response = requests.get("http://127.0.0.1:8000/api/v1/template/list")
    print("模板列表:", response.status_code)
    if response.status_code == 200:
        data = response.json()
        templates = data.get('data', {}).get('templates', [])
        print("模板数量:", len(templates))
        for t in templates:
            print(f"  - {t}")

    # 测试自动填充
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/template/auto-fill",
        json={
            "template_id": "1",  # 使用字符串
            "tender_content": "测试招标文档内容",
            "use_knowledge": False
        }
    )
    print("自动填充:", response.status_code)
    print("响应:", response.text)

if __name__ == "__main__":
    test_api()