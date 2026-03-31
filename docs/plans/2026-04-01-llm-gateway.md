# LLM Gateway Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现统一的LLM调用网关，支持多个国内大模型，为系统提供AI能力。

**Architecture:** 采用适配器模式，每个LLM提供商实现统一的接口，LLM Gateway负责路由和负载均衡。

**Tech Stack:** Python 3.10+, OpenAI SDK, zhipuai SDK, aiohttp, Pydantic

---

## 文件结构

```
backend/
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_gateway.py          # LLM Gateway主类
│   │   └── llm_adapters/
│   │       ├── __init__.py
│   │       ├── base.py              # LLM适配器基类
│   │       ├── qwen_adapter.py      # 通义千问适配器
│   │       ├── glm_adapter.py       # 智谱GLM适配器
│   │       ├── kimi_adapter.py      # Kimi适配器
│   │       └── doubao_adapter.py    # 豆包适配器
│   └── config/
│       ├── __init__.py
│       └── llm_config.py            # LLM配置管理
├── tests/
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_llm_gateway.py
│   │   └── test_llm_adapters/
│   │       ├── __init__.py
│   │       ├── test_qwen_adapter.py
│   │       ├── test_glm_adapter.py
│   │       ├── test_kimi_adapter.py
│   │       └── test_doubao_adapter.py
│   └── conftest.py
└── config/
    └── llm_config.yaml              # LLM配置文件
```

---

## Task 1: LLM配置系统

**Files:**
- Create: `backend/app/config/__init__.py`
- Create: `backend/app/config/llm_config.py`
- Create: `backend/config/llm_config.yaml`
- Test: `backend/tests/test_config/` (创建测试目录)

- [ ] **Step 1: 编写LLM配置测试**

创建文件 `tests/test_config/test_llm_config.py`:

```python
import pytest
from app.config.llm_config import LLMConfigManager, LLMProviderConfig

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
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_config/test_llm_config.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现LLM配置管理**

创建文件 `app/config/llm_config.py`:

```python
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
```

- [ ] **Step 4: 创建配置文件**

创建文件 `config/llm_config.yaml`:

```yaml
providers:
  qwen:
    name: "通义千问"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    models:
      - name: "qwen-max"
        type: "chat"
        context_length: 32000
        cost_per_1k_tokens: 0.12
      - name: "qwen-plus"
        type: "chat"
        context_length: 32000
        cost_per_1k_tokens: 0.008
      - name: "qwen-turbo"
        type: "chat"
        context_length: 8000
        cost_per_1k_tokens: 0.003
      - name: "text-embedding-v2"
        type: "embedding"
        dimension: 1536
  
  glm:
    name: "智谱GLM"
    base_url: "https://open.bigmodel.cn/api/paas/v4"
    models:
      - name: "glm-5"
        type: "chat"
        context_length: 128000
        cost_per_1k_tokens: 0.1
      - name: "glm-4.7"
        type: "chat"
        context_length: 128000
        cost_per_1k_tokens: 0.05
      - name: "glm-4-flash"
        type: "chat"
        context_length: 128000
        cost_per_1k_tokens: 0.001
  
  kimi:
    name: "Moonshot Kimi"
    base_url: "https://api.moonshot.cn/v1"
    models:
      - name: "kimi-k2.5"
        type: "chat"
        context_length: 256000
        cost_per_1k_tokens: 0.12
      - name: "moonshot-v1-128k"
        type: "chat"
        context_length: 128000
        cost_per_1k_tokens: 0.012
  
  doubao:
    name: "火山引擎豆包"
    base_url: "https://ark.cn-beijing.volces.com/api/v3"
    models:
      - name: "doubao-pro-32k"
        type: "chat"
        context_length: 32000
        cost_per_1k_tokens: 0.008
      - name: "doubao-lite-32k"
        type: "chat"
        context_length: 32000
        cost_per_1k_tokens: 0.003

default_provider: "qwen"

default_models:
  world_building: "qwen-max"
  character_creation: "glm-5"
  event_generation: "glm-4.7"
  narrative_writing: "kimi-k2.5"
  emotional_analysis: "qwen-plus"
  spark_detection: "glm-5"
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_config/test_llm_config.py -v
```

Expected: PASS

- [ ] **Step 6: 提交LLM配置系统**

```bash
git add backend/app/config/
git add backend/config/
git add backend/tests/test_config/
git commit -m "feat: implement LLM configuration system"
```

---

## Task 2: LLM适配器基类

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/llm_adapters/__init__.py`
- Create: `backend/app/services/llm_adapters/base.py`
- Test: `backend/tests/test_services/test_llm_adapters/`

- [ ] **Step 1: 编写LLM适配器基类测试**

创建文件 `tests/test_services/test_llm_adapters/test_base.py`:

```python
import pytest
from app.services.llm_adapters.base import BaseLLMAdapter, LLMConfig, LLMResponse

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
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_services/test_llm_adapters/test_base.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现LLM适配器基类**

创建文件 `app/services/llm_adapters/base.py`:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

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
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    latency: float = Field(..., ge=0, description="响应时间（秒）")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="额外信息")
    
    model_config = ConfigDict(extra="allow")

class BaseLLMAdapter(ABC):
    """LLM适配器基类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """生成文本（非流式）"""
        pass
    
    @abstractmethod
    async def stream_generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """生成文本（流式）"""
        pass
    
    async def _retry_with_backoff(self, func, *args, **kwargs):
        """带退避的重试机制"""
        for attempt in range(self.config.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise
                
                delay = self.config.retry_delay * (2 ** attempt)
                logger.warning(f"Retry {attempt + 1}/{self.config.max_retries} after {delay}s: {e}")
                await asyncio.sleep(delay)
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_services/test_llm_adapters/test_base.py -v
```

Expected: PASS

- [ ] **Step 5: 提交LLM适配器基类**

```bash
git add backend/app/services/
git add backend/tests/test_services/
git commit -m "feat: implement base LLM adapter class"
```

---

**计划继续...由于篇幅限制，完整计划包含以下后续任务：**

- Task 3: 通义千问适配器
- Task 4: 智谱GLM适配器
- Task 5: Kimi适配器
- Task 6: 豆包适配器
- Task 7: LLM Gateway主类
- Task 8: 集成测试
- Task 9: 文档和示例

**每个任务都遵循相同的TDD模式：编写测试 → 验证失败 → 实现代码 → 验证通过 → 提交。**
