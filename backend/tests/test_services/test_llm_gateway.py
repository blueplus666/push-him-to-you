import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_gateway import LLMGateway
from app.services.llm_adapters.base import LLMConfig, LLMResponse
from app.config.llm_config import LLMConfigManager


@pytest.fixture
def config_manager():
    manager = LLMConfigManager()
    manager.load_config()
    return manager


@pytest.fixture
def llm_gateway(config_manager):
    return LLMGateway(config_manager)


def test_llm_gateway_creation(llm_gateway):
    """测试LLM Gateway创建"""
    assert llm_gateway is not None


def test_llm_gateway_get_adapter(llm_gateway):
    """测试获取适配器"""
    adapter = llm_gateway.get_adapter("qwen")
    assert adapter is not None
    assert adapter.provider_name == "qwen"


def test_llm_gateway_get_nonexistent_adapter(llm_gateway):
    """测试获取不存在的适配器"""
    adapter = llm_gateway.get_adapter("nonexistent")
    assert adapter is None


@pytest.mark.asyncio
async def test_llm_gateway_generate(llm_gateway):
    """测试通过Gateway生成文本"""
    mock_response = LLMResponse(
        content="Hello from Gateway",
        model="qwen-max",
        provider="qwen",
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
        finish_reason="stop",
        latency=0.5
    )

    with patch.object(llm_gateway, '_call_adapter', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await llm_gateway.generate("Hello", provider="qwen")

        assert response.content == "Hello from Gateway"
        assert response.provider == "qwen"


@pytest.mark.asyncio
async def test_llm_gateway_generate_default_provider(llm_gateway):
    """测试使用默认提供商生成"""
    mock_response = LLMResponse(
        content="Default response",
        model="qwen-max",
        provider="qwen",
        prompt_tokens=5,
        completion_tokens=10,
        total_tokens=15,
        finish_reason="stop",
        latency=0.3
    )

    with patch.object(llm_gateway, '_call_adapter', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await llm_gateway.generate("Hello")

        assert response.provider == "qwen"


@pytest.mark.asyncio
async def test_llm_gateway_stream_generate(llm_gateway):
    """测试流式生成"""
    async def mock_stream():
        chunks = ["Hello", " from", " Gateway"]
        for chunk in chunks:
            yield chunk

    with patch.object(llm_gateway, '_stream_adapter', return_value=mock_stream()):
        result = []
        async for chunk in llm_gateway.stream_generate("Hello", provider="qwen"):
            result.append(chunk)

        assert result == ["Hello", " from", " Gateway"]


def test_llm_gateway_list_providers(llm_gateway):
    """测试列出所有提供商"""
    providers = llm_gateway.list_providers()
    assert "qwen" in providers
    assert "glm" in providers
    assert "kimi" in providers
    assert "doubao" in providers


def test_llm_gateway_get_default_model(llm_gateway):
    """测试获取默认模型"""
    model = llm_gateway.get_default_model("world_building")
    assert model is not None
