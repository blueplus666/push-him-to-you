import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_adapters.qwen_adapter import QwenAdapter
from app.services.llm_adapters.base import LLMConfig, LLMResponse, LLMRetryableError

@pytest.fixture
def qwen_config():
    return LLMConfig(
        provider="qwen",
        model="qwen-max",
        api_key="test-api-key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

@pytest.fixture
def qwen_adapter(qwen_config):
    return QwenAdapter(qwen_config)

def test_qwen_adapter_creation(qwen_adapter):
    """测试Qwen适配器创建"""
    assert qwen_adapter.config.provider == "qwen"
    assert qwen_adapter.config.model == "qwen-max"

@pytest.mark.asyncio
async def test_qwen_generate_success(qwen_adapter):
    """测试Qwen生成成功"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello from Qwen"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    mock_response.model = "qwen-max"

    with patch.object(qwen_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await qwen_adapter.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello from Qwen"
        assert response.provider == "qwen"
        assert response.total_tokens == 30

@pytest.mark.asyncio
async def test_qwen_generate_with_system_prompt(qwen_adapter):
    """测试带系统提示词的生成"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 15
    mock_response.usage.completion_tokens = 10
    mock_response.usage.total_tokens = 25
    mock_response.model = "qwen-max"

    with patch.object(qwen_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await qwen_adapter.generate("Hello", system_prompt="You are helpful")

        assert response.content == "Response"
        mock_call.assert_called_once()

@pytest.mark.asyncio
async def test_qwen_stream_generate(qwen_adapter):
    """测试流式生成"""
    async def mock_stream():
        chunks = ["Hello", " from", " Qwen"]
        for chunk in chunks:
            yield chunk

    with patch.object(qwen_adapter, '_stream_api', return_value=mock_stream()):
        result = []
        async for chunk in qwen_adapter.stream_generate("Hello"):
            result.append(chunk)

        assert result == ["Hello", " from", " Qwen"]
