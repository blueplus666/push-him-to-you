import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_adapters.glm_adapter import GLMAdapter
from app.services.llm_adapters.base import LLMConfig, LLMResponse, LLMRetryableError

@pytest.fixture
def glm_config():
    return LLMConfig(
        provider="glm",
        model="glm-5",
        api_key="test-api-key",
        base_url="https://open.bigmodel.cn/api/paas/v4"
    )

@pytest.fixture
def glm_adapter(glm_config):
    return GLMAdapter(glm_config)

def test_glm_adapter_creation(glm_adapter):
    """测试GLM适配器创建"""
    assert glm_adapter.config.provider == "glm"
    assert glm_adapter.config.model == "glm-5"

@pytest.mark.asyncio
async def test_glm_generate_success(glm_adapter):
    """测试GLM生成成功"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello from GLM"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    mock_response.model = "glm-5"

    with patch.object(glm_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await glm_adapter.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello from GLM"
        assert response.provider == "glm"
        assert response.total_tokens == 30

@pytest.mark.asyncio
async def test_glm_generate_with_system_prompt(glm_adapter):
    """测试带系统提示词的生成"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 15
    mock_response.usage.completion_tokens = 10
    mock_response.usage.total_tokens = 25
    mock_response.model = "glm-5"

    with patch.object(glm_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await glm_adapter.generate("Hello", system_prompt="You are helpful")

        assert response.content == "Response"
        mock_call.assert_called_once()

@pytest.mark.asyncio
async def test_glm_stream_generate(glm_adapter):
    """测试流式生成"""
    async def mock_stream():
        chunks = ["Hello", " from", " GLM"]
        for chunk in chunks:
            yield chunk

    with patch.object(glm_adapter, '_stream_api', return_value=mock_stream()):
        result = []
        async for chunk in glm_adapter.stream_generate("Hello"):
            result.append(chunk)

        assert result == ["Hello", " from", " GLM"]
