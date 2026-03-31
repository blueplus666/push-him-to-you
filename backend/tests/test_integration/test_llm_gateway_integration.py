import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock

from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway
from app.services.llm_adapters.base import LLMResponse, LLMRetryableError, LLMNonRetryableError


@pytest.fixture
def config_manager():
    """创建配置管理器"""
    manager = LLMConfigManager()
    manager.load_config()
    return manager


@pytest.fixture
def llm_gateway(config_manager):
    """创建LLM Gateway"""
    return LLMGateway(config_manager)


class TestLLMGatewayIntegration:
    """LLM Gateway集成测试"""

    def test_gateway_initialization(self, llm_gateway):
        """测试Gateway初始化"""
        assert llm_gateway is not None
        providers = llm_gateway.list_providers()
        assert len(providers) == 4
        assert "qwen" in providers

    def test_adapter_lazy_loading(self, llm_gateway):
        """测试适配器懒加载"""
        assert len(llm_gateway._adapters) == 0

        adapter = llm_gateway.get_adapter("qwen")
        assert adapter is not None
        assert len(llm_gateway._adapters) == 1

        adapter2 = llm_gateway.get_adapter("qwen")
        assert adapter is adapter2

    def test_config_to_adapter_integration(self, llm_gateway):
        """测试配置到适配器的集成"""
        adapter = llm_gateway.get_adapter("qwen")
        assert adapter is not None
        assert adapter.config.provider == "qwen"
        assert adapter.config.base_url is not None

    @pytest.mark.asyncio
    async def test_generate_with_mock(self, llm_gateway):
        """测试生成功能（使用mock）"""
        mock_response = LLMResponse(
            content="Integration test response",
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

            response = await llm_gateway.generate(
                "Test prompt",
                provider="qwen",
                system_prompt="You are helpful"
            )

            assert response.content == "Integration test response"
            assert response.provider == "qwen"

    @pytest.mark.asyncio
    async def test_stream_generate_with_mock(self, llm_gateway):
        """测试流式生成功能（使用mock）"""
        async def mock_stream():
            yield "Hello"
            yield " from"
            yield " integration"
            yield " test"

        with patch.object(llm_gateway, '_stream_adapter', return_value=mock_stream()):
            result = []
            async for chunk in llm_gateway.stream_generate("Test", provider="qwen"):
                result.append(chunk)

            assert result == ["Hello", " from", " integration", " test"]

    def test_default_model_mapping(self, llm_gateway):
        """测试默认模型映射"""
        model = llm_gateway.get_default_model("world_building")
        assert model == "qwen-max"

        model = llm_gateway.get_default_model("character_creation")
        assert model == "glm-5"

        model = llm_gateway.get_default_model("nonexistent_task")
        assert model is None

    def test_available_models(self, llm_gateway):
        """测试获取可用模型"""
        models = llm_gateway.get_available_models("qwen")
        assert len(models) > 0
        assert "qwen-max" in models

        models = llm_gateway.get_available_models("nonexistent")
        assert models == []

    @pytest.mark.asyncio
    async def test_error_handling_nonexistent_provider(self, llm_gateway):
        """测试不存在的提供商错误处理"""
        with pytest.raises(ValueError) as exc_info:
            await llm_gateway.generate("Test", provider="nonexistent")

        assert "not found" in str(exc_info.value)

    def test_all_adapters_creation(self, llm_gateway):
        """测试所有适配器创建"""
        providers = llm_gateway.list_providers()

        for provider in providers:
            adapter = llm_gateway.get_adapter(provider)
            assert adapter is not None, f"Failed to create adapter for {provider}"
            assert adapter.provider_name == provider


class TestConfigIntegration:
    """配置系统集成测试"""

    def test_config_loading(self, config_manager):
        """测试配置加载"""
        config = config_manager.load_config()
        assert config is not None
        assert "providers" in config

    def test_all_providers_config(self, config_manager):
        """测试所有提供商配置"""
        providers = ["qwen", "glm", "kimi", "doubao"]

        for provider in providers:
            provider_config = config_manager.get_provider_config(provider)
            assert provider_config is not None, f"Config missing for {provider}"
            assert provider_config.base_url is not None

    def test_env_key_loading(self, config_manager, monkeypatch):
        """测试环境变量API Key加载"""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key-123")

        manager = LLMConfigManager()
        manager.load_config()

        qwen_config = manager.get_provider_config("qwen")
        assert qwen_config.api_key == "test-key-123"


class TestAdapterIntegration:
    """适配器集成测试"""

    def test_adapter_config_propagation(self, llm_gateway):
        """测试配置正确传递到适配器"""
        adapter = llm_gateway.get_adapter("qwen")

        assert adapter.config.temperature == 0.7
        assert adapter.config.max_tokens == 2048

    @pytest.mark.asyncio
    async def test_adapter_retry_mechanism(self, llm_gateway):
        """测试适配器重试机制"""
        adapter = llm_gateway.get_adapter("qwen")

        call_count = 0

        async def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise LLMRetryableError("Temporary error")
            return LLMResponse(
                content="Success after retry",
                model="qwen-max",
                provider="qwen",
                prompt_tokens=5,
                completion_tokens=10,
                total_tokens=15,
                finish_reason="stop",
                latency=0.3
            )

        result = await adapter._retry_with_backoff(failing_func)

        assert call_count == 3
        assert result.content == "Success after retry"
