"""
投标管理API单元测试
"""
import pytest
from fastapi.testclient import TestClient


class TestBiddingDemo:
    """演示接口测试"""
    
    def test_demo_endpoint(self, client: TestClient):
        """测试演示接口"""
        response = client.get("/api/v1/bidding/demo")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "features" in data["data"]
        assert len(data["data"]["features"]) > 0


class TestTemplateManagement:
    """模板管理测试"""
    
    def test_get_templates(self, client: TestClient):
        """测试获取模板列表"""
        response = client.get("/api/v1/bidding/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data["data"]
        assert "count" in data["data"]
    
    def test_upload_template_invalid_format(self, client: TestClient):
        """测试上传非docx格式文件"""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        data = {"name": "test_template"}
        
        response = client.post(
            "/api/v1/bidding/upload-template",
            files=files,
            data=data
        )
        
        assert response.status_code == 400
        assert "只支持 .docx" in response.json()["detail"]
    
    def test_upload_template_invalid_name(self, client: TestClient):
        """测试上传模板名称太短"""
        files = {"file": ("test.docx", b"test content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"name": "a"}  # 只有一个字符
        
        response = client.post(
            "/api/v1/bidding/upload-template",
            files=files,
            data=data
        )
        
        assert response.status_code == 400


class TestTenderAnalysis:
    """招标分析测试"""
    
    def test_analyze_tender_too_short(self, client: TestClient):
        """测试招标内容太短"""
        response = client.post(
            "/api/v1/bidding/analyze-tender",
            data={"tender_content": "太短"}
        )
        
        assert response.status_code == 400
        assert "太短" in response.json()["detail"]
    
    @pytest.mark.skip(reason="需要实际的AI服务")
    def test_analyze_tender_success(self, client: TestClient, sample_tender_content):
        """测试招标分析成功（需要AI服务）"""
        response = client.post(
            "/api/v1/bidding/analyze-tender",
            data={"tender_content": sample_tender_content}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data["data"]


class TestOutlineGeneration:
    """大纲生成测试"""
    
    @pytest.mark.skip(reason="需要实际的AI服务")
    def test_generate_outline(self, client: TestClient):
        """测试大纲生成（需要AI服务）"""
        response = client.post(
            "/api/v1/bidding/generate-outline",
            data={
                "tender_requirements": "开发一个电商系统",
                "key_points": "高性能，安全，易用"
            }
        )
        
        assert response.status_code == 200


class TestDocumentGeneration:
    """文档生成测试"""
    
    @pytest.mark.skip(reason="需要实际的AI服务")
    def test_generate_document(self, client: TestClient):
        """测试文档生成（需要AI服务）"""
        response = client.post(
            "/api/v1/bidding/generate-document",
            data={
                "outline": "1. 项目背景 2. 技术方案 3. 实施计划",
                "tender_requirements": "开发一个电商系统"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data["data"]


class TestBidResponses:
    """投标响应管理测试"""
    
    def test_create_bid_response(self, client: TestClient):
        """测试创建投标响应"""
        response = client.post(
            "/api/v1/bidding/responses",
            json={
                "title": "测试投标响应",
                "tender_id": "test-tender-001",
                "content": "测试内容"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data["data"]
        assert data["data"]["title"] == "测试投标响应"
    
    def test_get_bid_responses(self, client: TestClient):
        """测试获取投标响应列表"""
        response = client.get("/api/v1/bidding/responses")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]
    
    def test_get_bid_response_not_found(self, client: TestClient):
        """测试获取不存在的投标响应"""
        response = client.get("/api/v1/bidding/responses/00000000-0000-0000-0000-000000000000")
        
        assert response.status_code == 404
    
    def test_get_bid_responses_invalid_page(self, client: TestClient):
        """测试无效页码"""
        response = client.get("/api/v1/bidding/responses?page=0")
        
        assert response.status_code == 400


class TestFileDownload:
    """文件下载测试"""
    
    def test_download_invalid_filename(self, client: TestClient):
        """测试下载无效文件名（路径遍历攻击）"""
        response = client.get("/api/v1/bidding/download/../etc/passwd")
        
        assert response.status_code == 400
    
    def test_download_nonexistent_file(self, client: TestClient):
        """测试下载不存在的文件"""
        response = client.get("/api/v1/bidding/download/nonexistent.docx")
        
        assert response.status_code == 404
