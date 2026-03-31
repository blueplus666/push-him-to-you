import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_adapters.kimi_adapter import KimiAdapter
from app.services.llm_adapters.base import LLMConfig, LLMResponse, LLMRetryableError

@pytest.fixture
def kimi_config():
    return LLMConfig(
        provider="kimi",
        model="kimi-k2.5",
        api_key="test-api-key",
        base_url="https://api.moonshot.cn/v1"
    )

@pytest.fixture
def kimi_adapter(kimi_config):
    return KimiAdapter(kimi_config)

def test_kimi_adapter_creation(kimi_adapter):
    """测试Kimi适配器创建"""
    assert kimi_adapter.config.provider == "kimi"
    assert kimi_adapter.config.model == "kimi-k2.5"

@pytest.mark.asyncio
async def test_kimi_generate_success(kimi_adapter):
    """测试Kimi生成成功"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello from Kimi"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    mock_response.model = "kimi-k2.5"

    with patch.object(kimi_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await kimi_adapter.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello from Kimi"
        assert response.provider == "kimi"
        assert response.total_tokens == 30

@pytest.mark.asyncio
async def test_kimi_generate_with_system_prompt(kimi_adapter):
    """测试带系统提示词的生成"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 15
    mock_response.usage.completion_tokens = 10
    mock_response.usage.total_tokens = 25
    mock_response.model = "kimi-k2.5"

    with patch.object(kimi_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await kimi_adapter.generate("Hello", system_prompt="You are helpful")

        assert response.content == "Response"
        mock_call.assert_called_once()

@pytest.mark.asyncio
async def test_kimi_stream_generate(kimi_adapter):
    """测试流式生成"""
    async def mock_stream():
        chunks = ["Hello", " from", " Kimi"]
        for chunk in chunks:
            yield chunk

    with patch.object(kimi_adapter, '_stream_api', return_value=mock_stream()):
        result = []
        async for chunk in kimi_adapter.stream_generate("Hello"):
            result.append(chunk)

        assert result == ["Hello", " from", " Kimi"]
