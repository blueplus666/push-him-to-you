import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_adapters.openai_compatible_adapter import OpenAICompatibleAdapter
from app.services.llm_adapters.base import LLMConfig, LLMResponse, LLMRetryableError, LLMNonRetryableError


class TestAdapter(OpenAICompatibleAdapter):
    """测试用适配器"""
    default_base_url = "https://api.test.com/v1"
    provider_name = "test"


@pytest.fixture
def test_config():
    return LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-api-key"
    )


@pytest.fixture
def test_adapter(test_config):
    return TestAdapter(test_config)


def test_adapter_creation(test_adapter):
    """测试适配器创建"""
    assert test_adapter.provider_name == "test"
    assert test_adapter.default_base_url == "https://api.test.com/v1"


def test_build_messages(test_adapter):
    """测试消息构建"""
    messages = test_adapter._build_messages("Hello")
    assert len(messages) == 1
    assert messages[0] == {"role": "user", "content": "Hello"}


def test_build_messages_with_system(test_adapter):
    """测试带系统提示词的消息构建"""
    messages = test_adapter._build_messages("Hello", "You are helpful")
    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": "You are helpful"}
    assert messages[1] == {"role": "user", "content": "Hello"}


@pytest.mark.asyncio
async def test_generate_success(test_adapter):
    """测试生成成功"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello back"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage.prompt_tokens = 5
    mock_response.usage.completion_tokens = 10
    mock_response.usage.total_tokens = 15
    mock_response.model = "test-model"

    with patch.object(test_adapter, '_call_api', new_callable=AsyncMock) as mock_call:
        mock_call.return_value = mock_response
        response = await test_adapter.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello back"
        assert response.provider == "test"


@pytest.mark.asyncio
async def test_stream_generate(test_adapter):
    """测试流式生成"""
    async def mock_stream():
        yield "Hello"
        yield " from"
        yield " test"

    with patch.object(test_adapter, '_stream_api', return_value=mock_stream()):
        result = []
        async for chunk in test_adapter.stream_generate("Hello"):
            result.append(chunk)

        assert result == ["Hello", " from", " test"]


def test_handle_rate_limit_error(test_adapter):
    """测试速率限制错误处理"""
    error = Exception("Rate limit exceeded (429)")
    with pytest.raises(LLMRetryableError):
        test_adapter._handle_api_error(error)


def test_handle_auth_error(test_adapter):
    """测试认证错误处理"""
    error = Exception("Authentication failed (401)")
    with pytest.raises(LLMNonRetryableError):
        test_adapter._handle_api_error(error)


def test_handle_connection_error(test_adapter):
    """测试连接错误处理"""
    error = Exception("Connection timeout")
    with pytest.raises(LLMRetryableError) as exc_info:
        test_adapter._handle_api_error(error)
    assert "Connection error" in str(exc_info.value)
