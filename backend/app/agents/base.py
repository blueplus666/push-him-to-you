from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.services.llm_gateway import LLMGateway


class AgentConfig(BaseModel):
    """Agent配置"""
    name: str = Field(..., description="Agent名称")
    description: str = Field(default="", description="Agent描述")
    model: str = Field(..., description="使用的模型")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1)
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    
    model_config = ConfigDict(extra="allow")


class AgentResponse(BaseModel):
    """Agent响应"""
    success: bool = Field(..., description="是否成功")
    data: Dict[str, Any] = Field(default_factory=dict, description="返回数据")
    error: Optional[str] = Field(None, description="错误信息")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    model_config = ConfigDict(extra="allow")


class BaseAgent(ABC):
    """Agent基类
    
    所有Agent必须继承此类并实现execute方法。
    """
    
    def __init__(self, config: AgentConfig, llm_gateway: LLMGateway):
        self.config = config
        self.llm_gateway = llm_gateway
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行Agent任务
        
        Args:
            input_data: 输入数据
            
        Returns:
            AgentResponse: Agent响应
        """
        pass
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """调用LLM生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            
        Returns:
            str: 生成的文本
            
        Raises:
            RuntimeError: LLM调用失败时
        """
        try:
            response = await self.llm_gateway.generate(
                prompt=prompt,
                provider=self._get_provider(),
                model=self.config.model,
                system_prompt=system_prompt or self.config.system_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.content
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}") from e
    
    def _get_provider(self) -> str:
        """根据模型名称获取提供商"""
        model = self.config.model.lower()
        if "qwen" in model:
            return "qwen"
        elif "glm" in model:
            return "glm"
        elif "kimi" in model or "moonshot" in model:
            return "kimi"
        elif "doubao" in model:
            return "doubao"
        return "qwen"
