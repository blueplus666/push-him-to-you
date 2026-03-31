import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_adapters.doubao_adapter import DoubaoAdapter
from app.services.llm_adapters.base import LLMConfig, LLMResponse, LLMRetryableError

@pytest.fixture
def doubao_config():
    return LLMConfig(
        provider="doubao",
        model="doubao-pro-32k",
        api_key="test-api-key",
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )

@pytest.fixture
def doubao_adapter(doubao_config):
    return DoubaoAdapter(doubao_config)

def test_doubao_adapter_creation(doubao_adapter):
    """测试豆包适配器创建"""
    assert doubao_adapter.config.provider == "doubao"
    assert doubao_adapter.config.model == "doubao-pro-32k"

@pytest.mark.asyncio
async def test_doubao_generate_success(doubao_adapter):
    """测试豆包生成成功"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello from Doubao"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    mock_response.model = "doubao-pro-32k"

    with patch.object(doubao_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await doubao_adapter.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello from Doubao"
        assert response.provider == "doubao"
        assert response.total_tokens == 30

@pytest.mark.asyncio
async def test_doubao_generate_with_system_prompt(doubao_adapter):
    """测试带系统提示词的生成"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 15
    mock_response.usage.completion_tokens = 10
    mock_response.usage.total_tokens = 25
    mock_response.model = "doubao-pro-32k"

    with patch.object(doubao_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await doubao_adapter.generate("Hello", system_prompt="You are helpful")

        assert response.content == "Response"
        mock_call.assert_called_once()

@pytest.mark.asyncio
async def test_doubao_stream_generate(doubao_adapter):
    """测试流式生成"""
    async def mock_stream():
        chunks = ["Hello", " from", " Doubao"]
        for chunk in chunks:
            yield chunk

    with patch.object(doubao_adapter, '_stream_api', return_value=mock_stream()):
        result = []
        async for chunk in doubao_adapter.stream_generate("Hello"):
            result.append(chunk)

        assert result == ["Hello", " from", " Doubao"]
