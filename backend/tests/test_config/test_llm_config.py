import pytest
import os
from pathlib import Path
from app.config.llm_config import (
    LLMConfigManager, 
    LLMProviderConfig,
    ModelConfig,
    ProviderConfig
)

def test_llm_config_loading():
    """测试LLM配置加载"""
    config_manager = LLMConfigManager()
    
    # 测试加载配置
    config = config_manager.load_config()
    assert config is not None
    assert "providers" in config

def test_llm_provider_config():
    """测试LLM提供商配置"""
    provider_config = LLMProviderConfig(
        provider="qwen",
        api_key="test-key",
        model="qwen-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    assert provider_config.provider == "qwen"
    assert provider_config.model == "qwen-plus"

def test_get_provider_config():
    """测试获取提供商配置"""
    config_manager = LLMConfigManager()
    
    # 获取不存在的提供商
    config = config_manager.get_provider_config("non-existent")
    assert config is None

def test_model_config():
    """测试模型配置"""
    model = ModelConfig(
        name="test-model",
        type="chat",
        context_length=8000,
        cost_per_1k_tokens=0.01
    )
    assert model.name == "test-model"
    assert model.type == "chat"
    assert model.context_length == 8000
    assert model.cost_per_1k_tokens == 0.01

def test_model_config_with_dimension():
    """测试带维度的模型配置（embedding模型）"""
    model = ModelConfig(
        name="text-embedding-v2",
        type="embedding",
        dimension=1536
    )
    assert model.name == "text-embedding-v2"
    assert model.type == "embedding"
    assert model.dimension == 1536

def test_provider_config():
    """测试提供商配置解析"""
    provider = ProviderConfig(
        name="测试提供商",
        base_url="https://api.test.com",
        models=[
            ModelConfig(name="model-1", type="chat"),
            ModelConfig(name="model-2", type="embedding")
        ]
    )
    assert provider.name == "测试提供商"
    assert provider.base_url == "https://api.test.com"
    assert len(provider.models) == 2
    assert provider.models[0].name == "model-1"
    assert provider.models[1].name == "model-2"

def test_get_provider_config_with_yaml():
    """测试从YAML文件获取提供商配置"""
    config_manager = LLMConfigManager()
    config_manager.load_config()
    
    qwen_config = config_manager.get_provider_config("qwen")
    assert qwen_config is not None
    assert qwen_config.provider == "qwen"
    assert qwen_config.base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    # 验证返回的是模型名称字符串，而不是字典
    assert isinstance(qwen_config.model, str)
    assert qwen_config.model == "qwen-max"

def test_get_provider_config_with_specific_model():
    """测试获取指定模型的提供商配置"""
    config_manager = LLMConfigManager()
    config_manager.load_config()
    
    qwen_config = config_manager.get_provider_config("qwen", "qwen-plus")
    assert qwen_config is not None
    assert qwen_config.model == "qwen-plus"

def test_get_available_models():
    """测试获取可用模型列表"""
    config_manager = LLMConfigManager()
    config_manager.load_config()
    
    models = config_manager.get_available_models("qwen")
    assert len(models) > 0
    assert "qwen-max" in models
    assert "qwen-plus" in models
    # 验证返回的是字符串列表
    assert all(isinstance(m, str) for m in models)

def test_get_available_models_non_existent():
    """测试获取不存在提供商的模型列表"""
    config_manager = LLMConfigManager()
    config_manager.load_config()
    
    models = config_manager.get_available_models("non-existent")
    assert models == []

def test_config_file_not_exists():
    """测试配置文件不存在时使用默认配置"""
    config_manager = LLMConfigManager("non_existent_config.yaml")
    config = config_manager.load_config()
    assert config is not None
    assert "providers" in config

def test_env_api_key_loading():
    """测试环境变量API Key加载"""
    # 设置环境变量
    os.environ["DASHSCOPE_API_KEY"] = "test-dashscope-key"
    
    try:
        config_manager = LLMConfigManager()
        config_manager.load_config()
        
        qwen_config = config_manager.get_provider_config("qwen")
        assert qwen_config is not None
        assert qwen_config.api_key == "test-dashscope-key"
    finally:
        # 清理环境变量
        if "DASHSCOPE_API_KEY" in os.environ:
            del os.environ["DASHSCOPE_API_KEY"]

def test_provider_config_defaults():
    """测试提供商配置默认值"""
    provider = ProviderConfig(
        name="测试",
        base_url="https://api.test.com"
    )
    assert provider.models == []
    assert provider.temperature == 0.7
    assert provider.max_tokens == 2048
