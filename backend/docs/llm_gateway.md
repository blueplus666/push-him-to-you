# LLM Gateway API 文档

## 概述

LLM Gateway 是一个统一的 LLM 调用网关，提供对不同 LLM 提供商的统一访问接口。它封装了各提供商的 API 差异，让开发者可以通过一致的接口调用不同的 LLM 服务。

### 支持的 LLM 提供商

| 提供商 | 标识符 | 默认模型 | 特点 |
|--------|--------|----------|------|
| 通义千问 (Qwen) | `qwen` | qwen-max | 阿里云，支持长上下文，性价比高 |
| 智谱 GLM | `glm` | glm-5 | 智谱AI，超长上下文，中文能力强 |
| Moonshot Kimi | `kimi` | kimi-k2.5 | 月之暗面，256K上下文，擅长长文本 |
| 火山引擎豆包 | `doubao` | doubao-pro-32k | 字节跳动，高性价比 |

### 核心特性

- **统一接口**: 所有提供商使用相同的 API 调用方式
- **配置驱动**: 通过 YAML 配置文件管理所有提供商
- **自动重试**: 内置指数退避重试机制
- **流式支持**: 支持流式和非流式两种生成模式
- **懒加载**: 适配器按需创建，节省资源

---

## 快速开始

### 安装依赖

```bash
cd backend
pip install -e .
```

### 基本配置

1. 复制环境变量模板:

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的 API Key:

```env
# 至少配置一个提供商的 API Key
DASHSCOPE_API_KEY=your-dashscope-api-key-here
```

### 简单示例

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def main():
    # 1. 创建配置管理器
    config_manager = LLMConfigManager()
    config_manager.load_config()

    # 2. 创建 Gateway
    gateway = LLMGateway(config_manager)

    # 3. 生成文本
    response = await gateway.generate("你好，请介绍一下自己")
    print(response.content)

asyncio.run(main())
```

---

## 配置说明

### 配置文件结构

配置文件位于 `config/llm_config.yaml`，结构如下:

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
    temperature: 0.7
    max_tokens: 2048

default_provider: "qwen"

default_models:
  world_building: "qwen-max"
  character_creation: "glm-5"
  event_generation: "glm-4.7"
```

### 环境变量设置

API Key 通过环境变量配置，支持以下变量:

| 环境变量 | 提供商 | 获取地址 |
|----------|--------|----------|
| `DASHSCOPE_API_KEY` | 通义千问 | https://dashscope.console.aliyun.com/ |
| `ZHIPUAI_API_KEY` | 智谱GLM | https://open.bigmodel.cn/ |
| `MOONSHOT_API_KEY` | Kimi | https://platform.moonshot.cn/ |
| `ARK_API_KEY` | 豆包 | https://console.volcengine.com/ark |

### 默认模型配置

可以为不同任务类型配置默认模型:

```yaml
default_models:
  world_building: "qwen-max"      # 世界构建
  character_creation: "glm-5"      # 角色创建
  event_generation: "glm-4.7"      # 事件生成
  narrative_writing: "kimi-k2.5"   # 叙事写作
  emotional_analysis: "qwen-plus"  # 情感分析
```

---

## API 参考

### LLMGateway 类

主要的 LLM 调用入口类。

#### 构造函数

```python
LLMGateway(config_manager: LLMConfigManager)
```

**参数:**
- `config_manager`: LLM 配置管理器实例

#### 主要方法

##### generate()

生成文本（非流式）。

```python
async def generate(
    self,
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    **kwargs: Any
) -> LLMResponse
```

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | str | 是 | 用户提示词 |
| `provider` | str | 否 | 提供商名称，默认使用配置中的默认提供商 |
| `model` | str | 否 | 模型名称，默认使用提供商的默认模型 |
| `system_prompt` | str | 否 | 系统提示词 |
| `**kwargs` | Any | 否 | 额外参数（如 temperature, max_tokens） |

**返回值:**
- `LLMResponse`: 响应对象，包含以下字段:
  - `content`: str - 生成的内容
  - `model`: str - 使用的模型
  - `provider`: str - 提供商
  - `prompt_tokens`: int - 提示词 token 数
  - `completion_tokens`: int - 完成 token 数
  - `total_tokens`: int - 总 token 数
  - `finish_reason`: str - 完成原因
  - `latency`: float - 响应时间（秒）

**异常:**
- `ValueError`: 提供商不存在
- `LLMNonRetryableError`: 认证失败等不可重试错误
- `LLMAdapterError`: 重试次数耗尽后的错误

---

##### stream_generate()

生成文本（流式）。

```python
async def stream_generate(
    self,
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    **kwargs: Any
) -> AsyncGenerator[str, None]
```

**参数:** 同 `generate()`

**返回值:**
- `AsyncGenerator[str, None]`: 异步生成器，逐块返回文本

---

##### list_providers()

列出所有可用的提供商。

```python
def list_providers(self) -> List[str]
```

**返回值:**
- `List[str]`: 提供商名称列表

---

##### get_default_model()

获取指定任务类型的默认模型。

```python
def get_default_model(self, task_type: str) -> Optional[str]
```

**参数:**
- `task_type`: 任务类型（如 world_building, character_creation）

**返回值:**
- `Optional[str]`: 默认模型名称，不存在则返回 None

---

##### get_available_models()

获取提供商可用模型列表。

```python
def get_available_models(self, provider: str) -> List[str]
```

**参数:**
- `provider`: 提供商名称

**返回值:**
- `List[str]`: 模型名称列表

---

### LLMConfigManager 类

配置管理器，负责加载和管理 LLM 配置。

#### 构造函数

```python
LLMConfigManager(config_path: str = "config/llm_config.yaml")
```

#### 主要方法

##### load_config()

加载配置文件。

```python
def load_config(self) -> Dict[str, Any]
```

##### get_provider_config()

获取提供商配置。

```python
def get_provider_config(
    self,
    provider: str,
    model: Optional[str] = None
) -> Optional[LLMProviderConfig]
```

---

## 使用示例

### 基本文本生成

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def basic_generation():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 使用默认提供商生成
    response = await gateway.generate("什么是人工智能？")
    print(f"回答: {response.content}")
    print(f"Token 使用: {response.total_tokens}")
    print(f"响应时间: {response.latency:.2f}s")

asyncio.run(basic_generation())
```

### 流式生成

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def stream_generation():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    print("流式输出: ", end="", flush=True)

    async for chunk in gateway.stream_generate("讲一个简短的故事"):
        print(chunk, end="", flush=True)

    print()  # 换行

asyncio.run(stream_generation())
```

### 指定提供商

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def use_specific_provider():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 使用智谱 GLM
    response = await gateway.generate(
        "解释一下量子计算的基本原理",
        provider="glm"
    )
    print(f"GLM 回答: {response.content}")

    # 使用 Kimi
    response = await gateway.generate(
        "解释一下量子计算的基本原理",
        provider="kimi"
    )
    print(f"Kimi 回答: {response.content}")

asyncio.run(use_specific_provider())
```

### 指定模型

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def use_specific_model():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 使用 qwen-turbo（更快、更便宜）
    response = await gateway.generate(
        "翻译成英文: 你好世界",
        provider="qwen",
        model="qwen-turbo"
    )
    print(f"翻译结果: {response.content}")

asyncio.run(use_specific_model())
```

### 系统提示词

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def with_system_prompt():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    response = await gateway.generate(
        "介绍一下 Python",
        provider="qwen",
        system_prompt="你是一位资深的编程导师，回答要简洁明了，适合初学者理解。"
    )
    print(response.content)

asyncio.run(with_system_prompt())
```

### 调整生成参数

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def with_custom_params():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 低温度（更确定性）
    response = await gateway.generate(
        "1+1等于几？",
        provider="qwen",
        temperature=0.1
    )
    print(f"确定性回答: {response.content}")

    # 高温度（更有创意）
    response = await gateway.generate(
        "写一句有创意的广告语",
        provider="qwen",
        temperature=1.2,
        max_tokens=100
    )
    print(f"创意回答: {response.content}")

asyncio.run(with_custom_params())
```

### 获取任务默认模型

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def use_task_default_model():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 获取世界构建任务的默认模型
    model = gateway.get_default_model("world_building")
    print(f"世界构建默认模型: {model}")  # 输出: qwen-max

    # 使用默认模型
    if model:
        response = await gateway.generate(
            "创建一个奇幻世界的背景设定",
            model=model
        )
        print(response.content)

asyncio.run(use_task_default_model())
```

### 查看可用模型

```python
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

def list_available_models():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    # 列出所有提供商
    providers = gateway.list_providers()
    print(f"可用提供商: {providers}")

    # 列出每个提供商的模型
    for provider in providers:
        models = gateway.get_available_models(provider)
        print(f"{provider} 可用模型: {models}")

list_available_models()
```

---

## 错误处理

### 异常类型

| 异常类型 | 说明 | 是否可重试 |
|----------|------|------------|
| `LLMAdapterError` | 基础异常，重试耗尽后抛出 | 否 |
| `LLMRetryableError` | 可重试错误（速率限制、临时连接问题） | 是 |
| `LLMNonRetryableError` | 不可重试错误（认证失败、无效请求） | 否 |
| `ValueError` | 提供商不存在等参数错误 | 否 |

### 错误处理示例

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway
from app.services.llm_adapters.base import (
    LLMAdapterError,
    LLMRetryableError,
    LLMNonRetryableError
)

async def handle_errors():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    try:
        response = await gateway.generate("你好", provider="qwen")
        print(response.content)

    except LLMNonRetryableError as e:
        # 不可重试错误：检查 API Key、请求参数
        print(f"配置错误: {e}")
        print("请检查您的 API Key 是否正确")

    except LLMRetryableError as e:
        # 可重试错误：Gateway 已自动重试，仍然失败
        print(f"服务暂时不可用: {e}")
        print("请稍后重试")

    except LLMAdapterError as e:
        # 重试耗尽后的错误
        print(f"LLM 调用失败: {e}")

    except ValueError as e:
        # 参数错误
        print(f"参数错误: {e}")

asyncio.run(handle_errors())
```

### 处理不存在的提供商

```python
import asyncio
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway

async def handle_invalid_provider():
    config_manager = LLMConfigManager()
    config_manager.load_config()
    gateway = LLMGateway(config_manager)

    try:
        response = await gateway.generate("你好", provider="invalid_provider")
    except ValueError as e:
        print(f"错误: {e}")  # Provider 'invalid_provider' not found

        # 获取可用提供商
        available = gateway.list_providers()
        print(f"可用提供商: {available}")

asyncio.run(handle_invalid_provider())
```

---

## 最佳实践

### 配置管理

1. **使用环境变量存储 API Key**

   不要将 API Key 硬编码在代码或配置文件中:

   ```python
   # 正确做法
   # .env 文件
   DASHSCOPE_API_KEY=sk-xxxxx

   # 错误做法
   # 不要在代码中硬编码
   api_key = "sk-xxxxx"  # 危险！
   ```

2. **为不同任务选择合适的模型**

   ```python
   # 简单任务使用轻量模型
   response = await gateway.generate(
       "翻译: Hello",
       model="qwen-turbo"  # 快速、便宜
   )

   # 复杂任务使用高级模型
   response = await gateway.generate(
       "分析这篇论文的核心观点...",
       model="qwen-max"  # 更强、更准确
   )
   ```

3. **复用 Gateway 实例**

   ```python
   # 正确：复用实例
   gateway = LLMGateway(config_manager)

   response1 = await gateway.generate("问题1")
   response2 = await gateway.generate("问题2")

   # 错误：每次创建新实例
   for question in questions:
       gateway = LLMGateway(config_manager)  # 浪费资源
       response = await gateway.generate(question)
   ```

### 性能优化

1. **使用流式生成处理长文本**

   ```python
   # 流式生成可以更快看到响应
   async for chunk in gateway.stream_generate(long_prompt):
       process_chunk(chunk)  # 实时处理
   ```

2. **合理设置 max_tokens**

   ```python
   # 简短回答
   response = await gateway.generate(
       "用一句话总结",
       max_tokens=100
   )

   # 详细回答
   response = await gateway.generate(
       "详细解释",
       max_tokens=2000
   )
   ```

3. **控制并发请求**

   ```python
   import asyncio

   async def batch_generate(prompts: list, gateway: LLMGateway):
       # 控制并发数
       semaphore = asyncio.Semaphore(3)

       async def limited_generate(prompt):
           async with semaphore:
               return await gateway.generate(prompt)

       tasks = [limited_generate(p) for p in prompts]
       return await asyncio.gather(*tasks)
   ```

### 成本控制

1. **监控 Token 使用**

   ```python
   response = await gateway.generate("你好")
   print(f"本次消耗: {response.total_tokens} tokens")
   print(f"提示词: {response.prompt_tokens}, 完成: {response.completion_tokens}")
   ```

2. **选择性价比合适的模型**

   | 模型 | 价格 (每1K tokens) | 适用场景 |
   |------|-------------------|----------|
   | qwen-turbo | 0.003 元 | 简单任务、高并发 |
   | qwen-plus | 0.008 元 | 中等复杂任务 |
   | qwen-max | 0.12 元 | 复杂推理、高质量输出 |
   | glm-4-flash | 0.001 元 | 极低成本场景 |

### 调试技巧

1. **启用日志**

   ```python
   import logging

   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger("app.services.llm_gateway")
   logger.setLevel(logging.DEBUG)
   ```

2. **检查配置**

   ```python
   config_manager = LLMConfigManager()
   config = config_manager.load_config()

   # 检查提供商配置
   for provider in ["qwen", "glm", "kimi", "doubao"]:
       provider_config = config_manager.get_provider_config(provider)
       if provider_config:
           print(f"{provider}: {provider_config.model}")
           print(f"  base_url: {provider_config.base_url}")
           print(f"  api_key: {'*' * 8 if provider_config.api_key else 'NOT SET'}")
   ```

---

## 完整示例

以下是一个完整的示例，展示如何在实际项目中使用 LLM Gateway:

```python
import asyncio
import logging
from app.config.llm_config import LLMConfigManager
from app.services.llm_gateway import LLMGateway
from app.services.llm_adapters.base import LLMAdapterError

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryGenerator:
    """故事生成器示例"""

    def __init__(self):
        self.config_manager = LLMConfigManager()
        self.config_manager.load_config()
        self.gateway = LLMGateway(self.config_manager)

    async def generate_story(self, theme: str) -> str:
        """生成故事"""
        try:
            # 获取叙事写作的默认模型
            model = self.gateway.get_default_model("narrative_writing")

            response = await self.gateway.generate(
                prompt=f"请写一个关于{theme}的短篇故事，大约200字。",
                model=model,
                system_prompt="你是一位富有想象力的故事作家，擅长创作引人入胜的短篇故事。"
            )

            logger.info(f"生成完成，消耗 {response.total_tokens} tokens")
            return response.content

        except LLMAdapterError as e:
            logger.error(f"生成失败: {e}")
            raise

    async def generate_story_stream(self, theme: str):
        """流式生成故事"""
        model = self.gateway.get_default_model("narrative_writing")

        async for chunk in self.gateway.stream_generate(
            prompt=f"请写一个关于{theme}的短篇故事。",
            model=model,
            system_prompt="你是一位富有想象力的故事作家。"
        ):
            yield chunk

async def main():
    generator = StoryGenerator()

    # 非流式生成
    print("=== 非流式生成 ===")
    story = await generator.generate_story("勇气")
    print(story)

    # 流式生成
    print("\n=== 流式生成 ===")
    async for chunk in generator.generate_story_stream("友谊"):
        print(chunk, end="", flush=True)
    print()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 相关文档

- [配置文件示例](../config/llm_config.yaml)
- [环境变量模板](../.env.example)
- [测试用例](../tests/test_integration/test_llm_gateway_integration.py)
