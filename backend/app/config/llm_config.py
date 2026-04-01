from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
import yaml
import os
from pathlib import Path

class LLMProviderConfig(BaseModel):
    """LLM提供商配置"""
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
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            # 返回默认配置
            self.config = self._get_default_config()
        else:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        
        # 从环境变量读取API Keys
        self._load_api_keys_from_env()
        
        return self.config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "providers": {
                "qwen": {
                    "name": "通义千问",
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                    "models": ["qwen-max", "qwen-plus", "qwen-turbo"]
                },
                "glm": {
                    "name": "智谱GLM",
                    "base_url": "https://open.bigmodel.cn/api/paas/v4",
                    "models": ["glm-5", "glm-4.7", "glm-4-flash"]
                },
                "kimi": {
                    "name": "Moonshot Kimi",
                    "base_url": "https://api.moonshot.cn/v1",
                    "models": ["kimi-k2.5", "moonshot-v1-128k"]
                },
                "doubao": {
                    "name": "火山引擎豆包",
                    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
                    "models": ["doubao-pro-32k", "doubao-lite-32k"]
                }
            },
            "default_provider": "qwen",
            "default_models": {
                "world_building": "qwen-max",
                "character_creation": "glm-5",
                "event_generation": "glm-4.7",
                "narrative_writing": "kimi-k2.5"
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
        if provider not in self.config.get("providers", {}):
            return None
        
        provider_data = self.config["providers"][provider]
        
        return LLMProviderConfig(
            provider=provider,
            api_key=provider_data.get("api_key", ""),
            model=model or provider_data.get("models", [""])[0],
            base_url=provider_data.get("base_url"),
            temperature=provider_data.get("temperature", 0.7),
            max_tokens=provider_data.get("max_tokens", 2048)
        )
    
    def get_available_models(self, provider: str) -> List[str]:
        """获取提供商可用模型列表
        
        Args:
            provider: 提供商名称
            
        Returns:
            模型名称列表
        """
        if provider not in self.config.get("providers", {}):
            return []
        
        provider_data = self.config["providers"][provider]
        return provider_data.get("models", [])
