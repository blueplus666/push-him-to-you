from typing import Optional, AsyncGenerator, Any, List, Dict
from openai import AsyncOpenAI
from app.services.llm_adapters.base import (
    BaseLLMAdapter, 
    LLMConfig, 
    LLMResponse,
    LLMRetryableError,
    LLMNonRetryableError
)
import time


class OpenAICompatibleAdapter(BaseLLMAdapter):
    """OpenAI兼容API适配器基类
    
    为使用OpenAI兼容API的LLM提供商提供通用实现。
    子类只需提供default_base_url和provider_name类属性。
    """
    
    default_base_url: str = ""
    provider_name: str = ""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client: Optional[AsyncOpenAI] = None
    
    @property
    def client(self) -> AsyncOpenAI:
        """获取OpenAI客户端（懒加载）"""
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url or self.default_base_url,
                timeout=self.config.timeout
            )
        return self._client
    
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """生成文本（非流式）"""
        start_time = time.time()
        messages = self._build_messages(prompt, system_prompt)
        
        async def _call():
            return await self._call_api(messages, **kwargs)
        
        response = await self._retry_with_backoff(_call)
        latency = time.time() - start_time
        
        return LLMResponse(
            content=response.choices[0].message.content or "",
            model=response.model,
            provider=self.provider_name,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason or "stop",
            latency=latency
        )
    
    async def stream_generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """生成文本（流式）"""
        messages = self._build_messages(prompt, system_prompt)
        
        async for chunk in self._stream_api(messages, **kwargs):
            yield chunk
    
    def _build_messages(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages
    
    async def _call_api(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs: Any
    ):
        """调用API"""
        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get("model", self.config.model),
                messages=messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                top_p=kwargs.get("top_p", self.config.top_p)
            )
            return response
        except Exception as e:
            self._handle_api_error(e)
    
    async def _stream_api(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """流式调用API"""
        try:
            stream = await self.client.chat.completions.create(
                model=kwargs.get("model", self.config.model),
                messages=messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                top_p=kwargs.get("top_p", self.config.top_p),
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            self._handle_api_error(e, is_stream=True)
    
    def _handle_api_error(self, error: Exception, is_stream: bool = False) -> None:
        """处理API错误"""
        error_str = str(error).lower()
        
        if "rate limit" in error_str or "429" in error_str:
            raise LLMRetryableError(f"Rate limit exceeded: {error}")
        elif "auth" in error_str or "401" in error_str or "403" in error_str:
            raise LLMNonRetryableError(f"Authentication failed: {error}")
        elif "timeout" in error_str or "connection" in error_str:
            raise LLMRetryableError(f"Connection error: {error}")
        else:
            prefix = "Stream error" if is_stream else "API error"
            raise LLMRetryableError(f"{prefix}: {error}")
