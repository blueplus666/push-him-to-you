from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
import yaml
import os
from pathlib import Path

class ModelConfig(BaseModel):
    """模型配置"""
    name: str = Field(..., description="模型名称")
    type: str = Field(default="chat", description="模型类型")
    context_length: int = Field(default=4096, description="上下文长度")
    cost_per_1k_tokens: float = Field(default=0.0, description="每1k token成本")
    dimension: Optional[int] = Field(None, description="向量维度（embedding模型）")
    
    model_config = ConfigDict(extra="allow")

class ProviderConfig(BaseModel):
    """提供商配置"""
    name: str = Field(..., description="提供商显示名称")
    base_url: str = Field(..., description="API地址")
    models: List[ModelConfig] = Field(default_factory=list, description="模型列表")
    api_key: Optional[str] = Field(None, description="API密钥")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=2048)
    
    model_config = ConfigDict(extra="allow")

class LLMProviderConfig(BaseModel):
    """LLM提供商配置（用于适配器）"""
    provider: str = Field(..., description="提供商名称")
    api_key: str = Field(..., description="API密钥")
    model: str = Field(..., description="模型名称")
    base_url: Optional[str] = Field(None, description="API地址")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(default=2048, ge=1, description="最大token数")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p采样")
    
    model_config = ConfigDict(extra="allow")

class LLMConfigManager:
    """LLM配置管理器"""
    
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._providers: Dict[str, ProviderConfig] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if not self.config_path.exists():
                self.config = self._get_default_config()
            else:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
            
            self._load_api_keys_from_env()
            self._validate_and_parse_config()
            
            return self.config
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {self.config_path}: {e}")
    
    def _validate_and_parse_config(self):
        """验证并解析配置"""
        providers = self.config.get("providers", {})
        for provider_name, provider_data in providers.items():
            try:
                self._providers[provider_name] = ProviderConfig(**provider_data)
            except Exception as e:
                raise ValueError(f"提供商 {provider_name} 配置无效: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "providers": {
                "qwen": {
                    "name": "通义千问",
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                    "models": [{"name": "qwen-max", "type": "chat"}]
                },
                "glm": {
                    "name": "智谱GLM",
                    "base_url": "https://open.bigmodel.cn/api/paas/v4",
                    "models": [{"name": "glm-5", "type": "chat"}]
                },
                "kimi": {
                    "name": "Moonshot Kimi",
                    "base_url": "https://api.moonshot.cn/v1",
                    "models": [{"name": "kimi-k2.5", "type": "chat"}]
                },
                "doubao": {
                    "name": "火山引擎豆包",
                    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
                    "models": [{"name": "doubao-pro-32k", "type": "chat"}]
                }
            },
            "default_provider": "qwen",
            "default_models": {
                "world_building": "qwen-max",
                "character_creation": "glm-5"
            }
        }
    
    def _load_api_keys_from_env(self):
        """从环境变量加载API Keys"""
        env_mapping = {
            "qwen": "DASHSCOPE_API_KEY",
            "glm": "ZHIPUAI_API_KEY",
            "kimi": "MOONSHOT_API_KEY",
            "doubao": "ARK_API_KEY"
        }
        
        for provider, env_key in env_mapping.items():
            api_key = os.getenv(env_key)
            if api_key and provider in self.config.get("providers", {}):
                self.config["providers"][provider]["api_key"] = api_key
    
    def get_provider_config(self, provider: str, model: Optional[str] = None) -> Optional[LLMProviderConfig]:
        """获取提供商配置"""
        if provider not in self._providers:
            return None
        
        provider_config = self._providers[provider]
        
        model_name = model
        if not model_name and provider_config.models:
            model_name = provider_config.models[0].name
        
        return LLMProviderConfig(
            provider=provider,
            api_key=provider_config.api_key or "",
            model=model_name or "",
            base_url=provider_config.base_url,
            temperature=provider_config.temperature,
            max_tokens=provider_config.max_tokens
        )
    
    def get_available_models(self, provider: str) -> List[str]:
        """获取提供商可用模型列表"""
        if provider not in self._providers:
            return []
        return [m.name for m in self._providers[provider].models]
