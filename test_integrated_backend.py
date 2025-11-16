#!/usr/bin/env python3
"""
测试完整集成后端的所有功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 测试AI标书助理系统 - 完整集成版")
print("=" * 60)

# 1. 测试知识库上传
print("\n1️⃣ 测试知识库上传...")
response = requests.post(
    f"{BASE_URL}/api/v1/knowledge/upload",
    json={
        "title": "投标文档撰写规范",
        "content": "投标文档应包含：1.公司资质证明 2.技术方案 3.项目团队介绍 4.报价明细 5.售后服务承诺。文档格式要求：使用A4纸张，正文使用宋体小四号字，行距1.5倍。",
        "category": "规范标准"
    }
)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

# 2. 测试知识库列表
print("\n2️⃣ 测试知识库列表...")
response = requests.get(f"{BASE_URL}/api/v1/knowledge/list")
print(f"状态码: {response.status_code}")
data = response.json()
print(f"知识库文档数: {data['data']['total']}")

# 3. 测试知识库搜索
print("\n3️⃣ 测试知识库搜索...")
response = requests.get(f"{BASE_URL}/api/v1/knowledge/search?query=投标&top_k=2")
print(f"状态码: {response.status_code}")
data = response.json()
print(f"搜索结果数: {data['data']['count']}")
if data['data']['results']:
    print(f"第一个结果: {data['data']['results'][0]['title']}")

# 4. 测试AI大纲生成（不使用RAG）
print("\n4️⃣ 测试AI大纲生成（不使用RAG）...")
response = requests.post(
    f"{BASE_URL}/api/v1/bidding/generate-outline",
    json={
        "topic": "智慧停车场项目投标方案",
        "key_points": "需要包含技术方案、项目管理、质量保证等内容",
        "use_knowledge": False
    }
)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    outline = data['data']['outline']
    print(f"大纲长度: {len(outline)} 字符")
    print(f"大纲前200字: {outline[:200]}...")
    print(f"Token使用: {data['data']['tokens_used']}")

# 5. 测试AI大纲生成（使用RAG）
print("\n5️⃣ 测试AI大纲生成（使用RAG）...")
response = requests.post(
    f"{BASE_URL}/api/v1/bidding/generate-outline",
    json={
        "topic": "投标文档编制方案",
        "use_knowledge": True
    }
)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"大纲长度: {len(data['data']['outline'])} 字符")
    print(f"是否使用知识库增强: {data['data']['knowledge_enhanced']}")

# 6. 测试AI章节生成
print("\n6️⃣ 测试AI章节生成...")
response = requests.post(
    f"{BASE_URL}/api/v1/bidding/generate-section",
    json={
        "outline_section": "## 项目技术方案\n### 系统架构设计",
        "context": "这是一个智慧停车场项目",
        "use_knowledge": False
    }
)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    content = data['data']['section_content']
    print(f"生成内容长度: {len(content)} 字符")
    print(f"内容前150字: {content[:150]}...")

# 7. 测试招标文档分析
print("\n7️⃣ 测试招标文档分析...")
response = requests.post(
    f"{BASE_URL}/api/v1/bidding/analyze",
    json={
        "tender_content": "某市智慧停车场项目招标。项目投资5000万元，建设停车位2000个，建设期12个月。要求具有建筑智能化工程专业承包一级资质。"
    }
)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"分析文本长度: {len(data['data']['analysis'])} 字符")
    print(f"关键要点数: {len(data['data']['key_points'])}")
    print(f"第一个要点: {data['data']['key_points'][0] if data['data']['key_points'] else '无'}")
    print(f"Token使用: {data['data']['tokens_used']}")

print("\n" + "=" * 60)
print("✅ 所有测试完成！")