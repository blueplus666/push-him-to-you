from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator, Callable, TypeVar, Awaitable
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
import asyncio
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class LLMAdapterError(Exception):
    """LLM适配器基础异常"""
    pass


class LLMRetryableError(LLMAdapterError):
    """可重试的LLM错误（如速率限制、临时连接问题）"""
    pass


class LLMNonRetryableError(LLMAdapterError):
    """不可重试的LLM错误（如认证失败、无效请求）"""
    pass

class LLMConfig(BaseModel):
    """LLM配置基类"""
    provider: str = Field(..., description="提供商名称")
    model: str = Field(..., description="模型名称")
    api_key: str = Field(..., description="API密钥")
    base_url: Optional[str] = Field(None, description="API地址")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_retries: int = Field(default=3, ge=0)
    retry_delay: float = Field(default=1.0, ge=0.0)
    timeout: float = Field(default=30.0, ge=1.0)
    
    model_config = ConfigDict(extra="allow")

class LLMResponse(BaseModel):
    """LLM响应基类"""
    content: str = Field(..., description="生成的内容")
    model: str = Field(..., description="使用的模型")
    provider: str = Field(..., description="提供商")
    prompt_tokens: int = Field(..., ge=0, description="提示词token数")
    completion_tokens: int = Field(..., ge=0, description="完成token数")
    total_tokens: int = Field(..., ge=0, description="总token数")
    finish_reason: str = Field(..., description="完成原因")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        description="创建时间"
    )
    latency: float = Field(..., ge=0, description="响应时间（秒）")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="额外信息")
    
    model_config = ConfigDict(extra="allow")

class BaseLLMAdapter(ABC):
    """LLM适配器基类
    
    所有LLM提供商适配器必须继承此类并实现以下方法：
    - generate(): 非流式生成
    - stream_generate(): 流式生成
    
    配置通过LLMConfig传入，支持重试机制和超时控制。
    """
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        """生成文本（非流式）
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            **kwargs: 额外参数
            
        Returns:
            LLMResponse: LLM响应对象
            
        Raises:
            LLMNonRetryableError: 认证失败、无效请求等不可重试错误
            LLMRetryableError: 速率限制、临时连接问题等可重试错误
            LLMAdapterError: 重试次数耗尽后的错误
        """
        pass
    
    @abstractmethod
    async def stream_generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """生成文本（流式）
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            **kwargs: 额外参数
            
        Yields:
            str: 生成的文本片段
            
        Raises:
            LLMNonRetryableError: 认证失败、无效请求等不可重试错误
            LLMRetryableError: 速率限制、临时连接问题等可重试错误
        """
        pass
    
    async def _retry_with_backoff(
        self, 
        func: Callable[..., Awaitable[T]], 
        *args: Any, 
        **kwargs: Any
    ) -> T:
        """带退避的重试机制
        
        Args:
            func: 异步函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            函数返回值
            
        Raises:
            LLMNonRetryableError: 不可重试的错误直接抛出
            LLMAdapterError: 重试次数耗尽后的错误
        """
        last_exception: Optional[Exception] = None
        
        for attempt in range(self.config.max_retries):
            try:
                return await func(*args, **kwargs)
            except LLMNonRetryableError:
                raise
            except LLMRetryableError as e:
                last_exception = e
                if attempt < self.config.max_retries - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Retry {attempt + 1}/{self.config.max_retries} after {delay}s: {e}"
                    )
                    await asyncio.sleep(delay)
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error during LLM call: {e}")
                raise LLMNonRetryableError(str(e)) from e
        
        logger.error(f"All {self.config.max_retries} retries exhausted")
        raise LLMAdapterError(
            f"Failed after {self.config.max_retries} retries"
        ) from last_exception
