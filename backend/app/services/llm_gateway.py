from typing import Optional, AsyncGenerator, Any, Dict, List
from app.config.llm_config import LLMConfigManager
from app.services.llm_adapters.base import LLMConfig, LLMResponse, BaseLLMAdapter
from app.services.llm_adapters.qwen_adapter import QwenAdapter
from app.services.llm_adapters.glm_adapter import GLMAdapter
from app.services.llm_adapters.kimi_adapter import KimiAdapter
from app.services.llm_adapters.doubao_adapter import DoubaoAdapter
import logging

logger = logging.getLogger(__name__)


class LLMGateway:
    """LLM网关

    统一的LLM调用入口，负责：
    - 适配器路由
    - 配置管理
    - 负载均衡（未来）
    """

    ADAPTER_MAP = {
        "qwen": QwenAdapter,
        "glm": GLMAdapter,
        "kimi": KimiAdapter,
        "doubao": DoubaoAdapter
    }

    def __init__(self, config_manager: LLMConfigManager):
        self.config_manager = config_manager
        self._adapters: Dict[str, BaseLLMAdapter] = {}

    def get_adapter(self, provider: str) -> Optional[BaseLLMAdapter]:
        """获取或创建适配器

        Args:
            provider: 提供商名称

        Returns:
            适配器实例，如果提供商不存在则返回None
        """
        if provider not in self.ADAPTER_MAP:
            return None

        if provider not in self._adapters:
            provider_config = self.config_manager.get_provider_config(provider)
            if provider_config:
                llm_config = LLMConfig(
                    provider=provider_config.provider,
                    model=provider_config.model,
                    api_key=provider_config.api_key,
                    base_url=provider_config.base_url,
                    temperature=provider_config.temperature,
                    max_tokens=provider_config.max_tokens
                )
                self._adapters[provider] = self.ADAPTER_MAP[provider](llm_config)

        return self._adapters.get(provider)

    async def generate(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """生成文本（非流式）

        Args:
            prompt: 用户提示词
            provider: 提供商名称（可选，默认使用配置中的默认提供商）
            model: 模型名称（可选）
            system_prompt: 系统提示词（可选）
            **kwargs: 额外参数

        Returns:
            LLMResponse: LLM响应对象

        Raises:
            ValueError: 提供商不存在
        """
        provider = provider or self.config_manager.config.get("default_provider", "qwen")
        adapter = self.get_adapter(provider)

        if not adapter:
            raise ValueError(f"Provider '{provider}' not found")

        return await self._call_adapter(
            adapter,
            prompt,
            model=model,
            system_prompt=system_prompt,
            **kwargs
        )

    async def stream_generate(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """生成文本（流式）

        Args:
            prompt: 用户提示词
            provider: 提供商名称（可选）
            model: 模型名称（可选）
            system_prompt: 系统提示词（可选）
            **kwargs: 额外参数

        Yields:
            str: 生成的文本片段
        """
        provider = provider or self.config_manager.config.get("default_provider", "qwen")
        adapter = self.get_adapter(provider)

        if not adapter:
            raise ValueError(f"Provider '{provider}' not found")

        async for chunk in self._stream_adapter(
            adapter,
            prompt,
            model=model,
            system_prompt=system_prompt,
            **kwargs
        ):
            yield chunk

    async def _call_adapter(
        self,
        adapter: BaseLLMAdapter,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """调用适配器生成"""
        if model:
            kwargs["model"] = model
        return await adapter.generate(prompt, system_prompt=system_prompt, **kwargs)

    async def _stream_adapter(
        self,
        adapter: BaseLLMAdapter,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """调用适配器流式生成"""
        if model:
            kwargs["model"] = model
        async for chunk in adapter.stream_generate(prompt, system_prompt=system_prompt, **kwargs):
            yield chunk

    def list_providers(self) -> List[str]:
        """列出所有可用的提供商"""
        return list(self.ADAPTER_MAP.keys())

    def get_default_model(self, task_type: str) -> Optional[str]:
        """获取指定任务类型的默认模型

        Args:
            task_type: 任务类型（如world_building, character_creation等）

        Returns:
            默认模型名称
        """
        default_models = self.config_manager.config.get("default_models", {})
        return default_models.get(task_type)

    def get_available_models(self, provider: str) -> List[str]:
        """获取提供商可用模型列表

        Args:
            provider: 提供商名称

        Returns:
            模型名称列表
        """
        return self.config_manager.get_available_models(provider)
