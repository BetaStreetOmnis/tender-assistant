#!/usr/bin/env python3
"""
测试AI自动填充模板变量功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_auto_fill():
    """测试AI自动填充模板变量"""
    print("🤖 测试AI自动填充模板变量")
    print("=" * 60)

    # 1. 首先获取可用的模板
    print("\n1️⃣ 获取模板列表...")
    response = requests.get(f"{BASE_URL}/api/v1/template/list")

    if response.status_code == 200:
        templates = response.json().get('data', {}).get('templates', [])
        if templates:
            template_id = templates[0]['id']
            print(f"   ✅ 找到模板: ID={template_id}, 名称={templates[0]['name']}")
        else:
            print("   ❌ 没有找到模板，请先上传模板文件")
            return
    else:
        print(f"   ❌ 获取模板列表失败: {response.status_code}")
        return

    # 2. 测试无招标文档的自动填充
    print("\n2️⃣ 测试无招标文档的自动填充...")
    auto_fill_data = {
        "template_id": template_id,
        "tender_content": None,
        "use_knowledge": True
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/template/auto-fill",
        json=auto_fill_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ AI自动填充成功")
        print(f"   📊 使用了知识库: {result['data'].get('knowledge_used', False)}")
        print(f"   💰 Token使用: {result['data'].get('tokens_used', 0)}")
        print(f"   🎯 置信度: {result['data'].get('ai_confidence', 'unknown')}")

        filled_values = result['data'].get('filled_values', {})
        print(f"   📝 填充的变量 ({len(filled_values)} 个):")
        for var_name, value in filled_values.items():
            print(f"      • {var_name}: {value}")
    else:
        print(f"   ❌ AI自动填充失败: {response.status_code}")
        print(f"   错误信息: {response.text}")

    # 3. 测试带招标文档的自动填充
    print("\n3️⃣ 测试带招标文档的自动填充...")
    tender_content = """
项目名称：XX市政府智慧安防系统建设项目

建设内容：
1. 视频监控系统建设
2. 门禁系统升级改造
3. 周界报警系统
4. 智能分析平台

招标单位：XX市公安局
项目预算：500万元
工期要求：180日历天
质量标准：国家相关标准规范
    """

    auto_fill_data = {
        "template_id": template_id,
        "tender_content": tender_content,
        "use_knowledge": True
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/template/auto-fill",
        json=auto_fill_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ AI自动填充成功（基于招标文档）")
        print(f"   📊 使用了知识库: {result['data'].get('knowledge_used', False)}")
        print(f"   💰 Token使用: {result['data'].get('tokens_used', 0)}")
        print(f"   🎯 置信度: {result['data'].get('ai_confidence', 'unknown')}")

        filled_values = result['data'].get('filled_values', {})
        print(f"   📝 填充的变量 ({len(filled_values)} 个):")
        for var_name, value in filled_values.items():
            print(f"      • {var_name}: {value}")
    else:
        print(f"   ❌ AI自动填充失败: {response.status_code}")
        print(f"   错误信息: {response.text}")

    # 4. 测试不带知识库的填充
    print("\n4️⃣ 测试不带知识库的填充...")
    auto_fill_data = {
        "template_id": template_id,
        "tender_content": tender_content,
        "use_knowledge": False
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/template/auto-fill",
        json=auto_fill_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ AI自动填充成功（纯AI生成）")
        print(f"   📊 使用了知识库: {result['data'].get('knowledge_used', False)}")
        print(f"   💰 Token使用: {result['data'].get('tokens_used', 0)}")
        print(f"   🎯 置信度: {result['data'].get('ai_confidence', 'unknown')}")
    else:
        print(f"   ❌ AI自动填充失败: {response.status_code}")
        print(f"   错误信息: {response.text}")

def main():
    """主函数"""
    print("🧪 测试AI自动填充模板变量功能")
    print("确保后端服务正在运行: http://127.0.0.1:8000")

    try:
        test_auto_fill()
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    print("\n✅ 测试完成")

if __name__ == "__main__":
    main()