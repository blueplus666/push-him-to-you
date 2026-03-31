import pytest
from pydantic import ValidationError
from app.services.llm_adapters.base import (
    BaseLLMAdapter, 
    LLMConfig, 
    LLMResponse,
    LLMAdapterError,
    LLMRetryableError,
    LLMNonRetryableError
)

def test_llm_config_creation():
    """测试LLM配置创建"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        base_url="https://api.test.com"
    )
    
    assert config.provider == "test"
    assert config.model == "test-model"
    assert config.api_key == "test-key"

def test_llm_response_creation():
    """测试LLM响应创建"""
    response = LLMResponse(
        content="Hello, world!",
        model="test-model",
        provider="test",
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
        finish_reason="stop",
        latency=0.5
    )
    
    assert response.content == "Hello, world!"
    assert response.total_tokens == 30

def test_base_llm_adapter_is_abstract():
    """测试BaseLLMAdapter是抽象类"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key"
    )
    
    with pytest.raises(TypeError):
        BaseLLMAdapter(config)

def test_llm_config_defaults():
    """测试LLM配置默认值"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key"
    )
    
    assert config.temperature == 0.7
    assert config.max_tokens == 2048
    assert config.top_p == 0.9
    assert config.max_retries == 3
    assert config.timeout == 30.0

def test_llm_response_with_metadata():
    """测试LLM响应带元数据"""
    response = LLMResponse(
        content="Test",
        model="model",
        provider="provider",
        prompt_tokens=5,
        completion_tokens=10,
        total_tokens=15,
        finish_reason="stop",
        latency=0.3,
        metadata={"custom": "value"}
    )
    
    assert response.metadata == {"custom": "value"}

def test_llm_config_validation_invalid_temperature():
    """测试无效的temperature值"""
    with pytest.raises(ValidationError):
        LLMConfig(
            provider="test",
            model="test-model",
            api_key="test-key",
            temperature=3.0
        )

def test_llm_config_validation_negative_max_tokens():
    """测试无效的max_tokens值"""
    with pytest.raises(ValidationError):
        LLMConfig(
            provider="test",
            model="test-model",
            api_key="test-key",
            max_tokens=0
        )

def test_llm_config_validation_invalid_top_p():
    """测试无效的top_p值"""
    with pytest.raises(ValidationError):
        LLMConfig(
            provider="test",
            model="test-model",
            api_key="test-key",
            top_p=1.5
        )

def test_llm_config_extra_fields():
    """测试额外字段是否被允许"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        custom_field="custom_value"
    )
    assert config.model_extra is not None
    assert config.model_extra.get("custom_field") == "custom_value"

def test_llm_adapter_error():
    """测试LLM适配器异常"""
    with pytest.raises(LLMAdapterError):
        raise LLMAdapterError("Test error")

def test_llm_retryable_error():
    """测试可重试异常"""
    with pytest.raises(LLMRetryableError):
        raise LLMRetryableError("Rate limit exceeded")

def test_llm_non_retryable_error():
    """测试不可重试异常"""
    with pytest.raises(LLMNonRetryableError):
        raise LLMNonRetryableError("Authentication failed")

def test_llm_response_created_at_timezone():
    """测试响应时间使用UTC时区"""
    response = LLMResponse(
        content="Test",
        model="model",
        provider="provider",
        prompt_tokens=5,
        completion_tokens=10,
        total_tokens=15,
        finish_reason="stop",
        latency=0.3
    )
    assert response.created_at.tzinfo is not None

@pytest.mark.asyncio
async def test_retry_with_backoff_success():
    """测试重试机制成功"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        max_retries=3,
        retry_delay=0.1
    )
    
    call_count = 0
    
    async def success_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    class TestAdapter(BaseLLMAdapter):
        async def generate(self, prompt, system_prompt=None, **kwargs):
            pass
        
        async def stream_generate(self, prompt, system_prompt=None, **kwargs):
            pass
    
    adapter = TestAdapter(config)
    result = await adapter._retry_with_backoff(success_func)
    
    assert result == "success"
    assert call_count == 1

@pytest.mark.asyncio
async def test_retry_with_backoff_retryable_error():
    """测试可重试错误的重试机制"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        max_retries=3,
        retry_delay=0.1
    )
    
    call_count = 0
    
    async def failing_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise LLMRetryableError("Rate limit")
        return "success"
    
    class TestAdapter(BaseLLMAdapter):
        async def generate(self, prompt, system_prompt=None, **kwargs):
            pass
        
        async def stream_generate(self, prompt, system_prompt=None, **kwargs):
            pass
    
    adapter = TestAdapter(config)
    result = await adapter._retry_with_backoff(failing_func)
    
    assert result == "success"
    assert call_count == 3

@pytest.mark.asyncio
async def test_retry_with_backoff_non_retryable_error():
    """测试不可重试错误立即抛出"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        max_retries=3,
        retry_delay=0.1
    )
    
    call_count = 0
    
    async def failing_func():
        nonlocal call_count
        call_count += 1
        raise LLMNonRetryableError("Auth failed")
    
    class TestAdapter(BaseLLMAdapter):
        async def generate(self, prompt, system_prompt=None, **kwargs):
            pass
        
        async def stream_generate(self, prompt, system_prompt=None, **kwargs):
            pass
    
    adapter = TestAdapter(config)
    
    with pytest.raises(LLMNonRetryableError):
        await adapter._retry_with_backoff(failing_func)
    
    assert call_count == 1

@pytest.mark.asyncio
async def test_retry_with_backoff_exhausted():
    """测试重试次数耗尽"""
    config = LLMConfig(
        provider="test",
        model="test-model",
        api_key="test-key",
        max_retries=2,
        retry_delay=0.1
    )
    
    call_count = 0
    
    async def always_failing():
        nonlocal call_count
        call_count += 1
        raise LLMRetryableError("Always fails")
    
    class TestAdapter(BaseLLMAdapter):
        async def generate(self, prompt, system_prompt=None, **kwargs):
            pass
        
        async def stream_generate(self, prompt, system_prompt=None, **kwargs):
            pass
    
    adapter = TestAdapter(config)
    
    with pytest.raises(LLMAdapterError):
        await adapter._retry_with_backoff(always_failing)
    
    assert call_count == 2
