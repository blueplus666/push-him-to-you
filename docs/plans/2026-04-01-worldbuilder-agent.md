# WorldBuilder Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现WorldBuilder Agent，负责创建和维护故事世界的基础设定。

**Architecture:** 采用Agent基类模式，WorldBuilder继承BaseAgent，通过LLM Gateway调用大模型生成世界设定。使用Pydantic模型定义世界状态结构，支持YAML模板配置。

**Tech Stack:** Python 3.10+, Pydantic, LLM Gateway, YAML

---

## 文件结构

```
backend/
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py                    # Agent基类
│   │   └── world_builder.py           # WorldBuilder Agent
│   ├── models/
│   │   ├── __init__.py
│   │   └── world.py                   # 世界模型（已存在，需更新）
│   └── prompts/
│       ├── __init__.py
│       └── world_builder_prompts.py   # WorldBuilder提示词模板
├── tests/
│   └── test_agents/
│       ├── __init__.py
│       ├── test_base_agent.py
│       └── test_world_builder.py
└── config/
    └── world_templates.yaml           # 世界设定模板
```

---

## Task 1: Agent基类

**Files:**
- Create: `backend/app/agents/__init__.py`
- Create: `backend/app/agents/base.py`
- Test: `backend/tests/test_agents/__init__.py`
- Test: `backend/tests/test_agents/test_base_agent.py`

- [ ] **Step 1: 编写Agent基类测试**

创建文件 `tests/test_agents/test_base_agent.py`:

```python
import pytest
from abc import ABC
from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.services.llm_gateway import LLMGateway


class TestAgent(BaseAgent):
    """测试用Agent"""
    
    async def execute(self, input_data: dict) -> AgentResponse:
        return AgentResponse(
            success=True,
            data={"result": "test"},
            metadata={"agent": "test"}
        )


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="test_agent",
        description="Test agent for unit tests",
        model="qwen-max",
        temperature=0.7
    )


@pytest.fixture
def mock_gateway():
    from unittest.mock import MagicMock
    gateway = MagicMock(spec=LLMGateway)
    return gateway


def test_agent_config_creation(agent_config):
    """测试Agent配置创建"""
    assert agent_config.name == "test_agent"
    assert agent_config.model == "qwen-max"
    assert agent_config.temperature == 0.7


def test_agent_response_creation():
    """测试Agent响应创建"""
    response = AgentResponse(
        success=True,
        data={"key": "value"},
        metadata={"time": 0.5}
    )
    assert response.success is True
    assert response.data == {"key": "value"}


def test_base_agent_is_abstract():
    """测试BaseAgent是抽象类"""
    with pytest.raises(TypeError):
        BaseAgent(AgentConfig(name="test", model="test"))


def test_test_agent_creation(agent_config, mock_gateway):
    """测试具体Agent创建"""
    agent = TestAgent(agent_config, mock_gateway)
    assert agent.config.name == "test_agent"


@pytest.mark.asyncio
async def test_test_agent_execute(agent_config, mock_gateway):
    """测试Agent执行"""
    agent = TestAgent(agent_config, mock_gateway)
    response = await agent.execute({"input": "test"})
    assert response.success is True
    assert response.data == {"result": "test"}
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_agents/test_base_agent.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现Agent基类**

创建文件 `app/agents/__init__.py`:

```python
from app.agents.base import BaseAgent, AgentConfig, AgentResponse

__all__ = ["BaseAgent", "AgentConfig", "AgentResponse"]
```

创建文件 `app/agents/base.py`:

```python
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
        """
        response = await self.llm_gateway.generate(
            prompt=prompt,
            provider=self._get_provider(),
            model=self.config.model,
            system_prompt=system_prompt or self.config.system_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.content
    
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
```

- [ ] **Step 4: 创建测试目录初始化文件**

创建文件 `tests/test_agents/__init__.py`:

```python
# Agent tests
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_agents/test_base_agent.py -v
```

Expected: PASS

- [ ] **Step 6: 提交Agent基类**

```bash
git add backend/app/agents/
git add backend/tests/test_agents/
git commit -m "feat: implement BaseAgent class"
```

---

## Task 2: 世界模型更新

**Files:**
- Modify: `backend/app/models/world.py`
- Test: `backend/tests/test_models/test_world.py`

- [ ] **Step 1: 编写世界模型测试**

创建文件 `tests/test_models/test_world.py`:

```python
import pytest
from datetime import datetime
from app.models.world import (
    WorldState, 
    WorldSetting, 
    SocialStructure, 
    CulturalFeature,
    EnvironmentDescription,
    ConflictSource
)


def test_world_setting_creation():
    """测试世界设定创建"""
    setting = WorldSetting(
        era="现代都市",
        location={"province": "浙江", "city": "杭州"},
        society_type="平稳发展型",
        special_settings=["包含重大社会事件"]
    )
    assert setting.era == "现代都市"
    assert setting.location["city"] == "杭州"


def test_social_structure_creation():
    """测试社会结构创建"""
    structure = SocialStructure(
        classes=["上层", "中层", "底层"],
        power_distribution={"政府": 40, "企业": 35, "民间": 25},
        social_mobility="中等流动性"
    )
    assert len(structure.classes) == 3


def test_cultural_feature_creation():
    """测试文化特征创建"""
    culture = CulturalFeature(
        core_values=["勤劳", "诚信", "创新"],
        customs=["春节团圆", "中秋赏月"],
        taboos=["不孝", "欺诈"]
    )
    assert "勤劳" in culture.core_values


def test_environment_description_creation():
    """测试环境描述创建"""
    env = EnvironmentDescription(
        natural_environment="江南水乡，四季分明",
        urban_environment="现代化都市，高楼林立",
        key_locations=["西湖", "钱塘江", "高新区"]
    )
    assert "西湖" in env.key_locations


def test_conflict_source_creation():
    """测试冲突源创建"""
    conflict = ConflictSource(
        social_contradictions=["贫富差距", "代际冲突"],
        resource_competition=["房价", "教育资源"],
        potential_events=["经济危机", "技术革命"]
    )
    assert len(conflict.social_contradictions) == 2


def test_world_state_creation():
    """测试世界状态创建"""
    world = WorldState(
        world_id="world-001",
        setting=WorldSetting(
            era="现代都市",
            location={"province": "浙江", "city": "杭州"},
            society_type="平稳发展型"
        ),
        social_structure=SocialStructure(
            classes=["上层", "中层", "底层"],
            power_distribution={"政府": 40, "企业": 35, "民间": 25}
        ),
        cultural_features=CulturalFeature(
            core_values=["勤劳", "诚信"]
        ),
        environment=EnvironmentDescription(
            natural_environment="江南水乡"
        ),
        conflict_sources=[
            ConflictSource(
                social_contradictions=["贫富差距"]
            )
        ]
    )
    assert world.world_id == "world-001"
    assert world.setting.era == "现代都市"
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_models/test_world.py -v
```

Expected: FAIL - ImportError

- [ ] **Step 3: 实现世界模型**

创建文件 `app/models/world.py`:

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from datetime import datetime


class WorldSetting(BaseModel):
    """世界基础设定"""
    era: str = Field(..., description="时代背景")
    location: Dict[str, str] = Field(..., description="地理位置")
    society_type: str = Field(..., description="社会类型")
    special_settings: List[str] = Field(default_factory=list, description="特殊设定")
    time_span: Dict[str, int] = Field(
        default_factory=lambda: {"start": 1990, "end": 2025},
        description="时间跨度"
    )
    
    model_config = ConfigDict(extra="allow")


class SocialStructure(BaseModel):
    """社会结构"""
    classes: List[str] = Field(default_factory=list, description="社会阶层")
    power_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="权力分布（百分比）"
    )
    social_mobility: str = Field(default="中等流动性", description="社会流动性")
    
    model_config = ConfigDict(extra="allow")


class CulturalFeature(BaseModel):
    """文化特征"""
    core_values: List[str] = Field(default_factory=list, description="核心价值观")
    customs: List[str] = Field(default_factory=list, description="习俗")
    taboos: List[str] = Field(default_factory=list, description="禁忌")
    religion: Optional[str] = Field(None, description="主要宗教")
    
    model_config = ConfigDict(extra="allow")


class EnvironmentDescription(BaseModel):
    """环境描述"""
    natural_environment: str = Field(default="", description="自然环境")
    urban_environment: str = Field(default="", description="城市环境")
    key_locations: List[str] = Field(default_factory=list, description="关键地点")
    climate: Optional[str] = Field(None, description="气候特征")
    
    model_config = ConfigDict(extra="allow")


class ConflictSource(BaseModel):
    """冲突源"""
    social_contradictions: List[str] = Field(default_factory=list, description="社会矛盾")
    resource_competition: List[str] = Field(default_factory=list, description="资源争夺")
    potential_events: List[str] = Field(default_factory=list, description="潜在事件")
    
    model_config = ConfigDict(extra="allow")


class WorldState(BaseModel):
    """世界状态模型"""
    world_id: str = Field(..., description="世界唯一标识")
    setting: WorldSetting = Field(..., description="世界设定")
    social_structure: Optional[SocialStructure] = Field(None, description="社会结构")
    cultural_features: Optional[CulturalFeature] = Field(None, description="文化特征")
    environment: Optional[EnvironmentDescription] = Field(None, description="环境描述")
    conflict_sources: List[ConflictSource] = Field(
        default_factory=list,
        description="冲突源列表"
    )
    
    current_time: datetime = Field(
        default_factory=datetime.now,
        description="当前时间"
    )
    environment_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="环境状态"
    )
    social_events: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="社会事件列表"
    )
    
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "world_id": "world-001",
                "setting": {
                    "era": "现代都市",
                    "location": {"province": "浙江", "city": "杭州"},
                    "society_type": "平稳发展型"
                },
                "social_structure": {
                    "classes": ["上层", "中层", "底层"],
                    "power_distribution": {"政府": 40, "企业": 35, "民间": 25}
                }
            }
        }
    )
    
    def update_time(self, new_time: datetime) -> None:
        """更新当前时间"""
        self.current_time = new_time
        self.updated_at = datetime.now()
    
    def add_social_event(self, event: Dict[str, Any]) -> None:
        """添加社会事件"""
        self.social_events.append(event)
        self.updated_at = datetime.now()
```

- [ ] **Step 4: 更新models/__init__.py**

更新文件 `app/models/__init__.py`:

```python
from app.models.world import (
    WorldState,
    WorldSetting,
    SocialStructure,
    CulturalFeature,
    EnvironmentDescription,
    ConflictSource
)

__all__ = [
    "WorldState",
    "WorldSetting",
    "SocialStructure",
    "CulturalFeature",
    "EnvironmentDescription",
    "ConflictSource"
]
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_models/test_world.py -v
```

Expected: PASS

- [ ] **Step 6: 提交世界模型**

```bash
git add backend/app/models/
git add backend/tests/test_models/
git commit -m "feat: implement WorldState model with detailed structure"
```

---

## Task 3: WorldBuilder提示词模板

**Files:**
- Create: `backend/app/prompts/__init__.py`
- Create: `backend/app/prompts/world_builder_prompts.py`
- Test: `backend/tests/test_prompts/test_world_builder_prompts.py`

- [ ] **Step 1: 编写提示词模板测试**

创建文件 `tests/test_prompts/test_world_builder_prompts.py`:

```python
import pytest
from app.prompts.world_builder_prompts import (
    WorldBuilderPrompts,
    WORLD_BUILDER_SYSTEM_PROMPT,
    WORLD_BUILDER_USER_PROMPT
)


def test_system_prompt_exists():
    """测试系统提示词存在"""
    assert WORLD_BUILDER_SYSTEM_PROMPT is not None
    assert len(WORLD_BUILDER_SYSTEM_PROMPT) > 100


def test_user_prompt_template():
    """测试用户提示词模板"""
    prompt = WORLD_BUILDER_USER_PROMPT.format(
        era="现代都市",
        location="杭州",
        society_type="平稳发展型",
        special_settings="无"
    )
    assert "现代都市" in prompt
    assert "杭州" in prompt


def test_world_builder_prompts_class():
    """测试WorldBuilderPrompts类"""
    prompts = WorldBuilderPrompts()
    
    system_prompt = prompts.get_system_prompt()
    assert system_prompt is not None
    
    user_prompt = prompts.get_user_prompt(
        era="古代",
        location="长安",
        society_type="封建社会",
        special_settings="武侠世界"
    )
    assert "古代" in user_prompt
    assert "长安" in user_prompt


def test_parse_world_response():
    """测试解析世界响应"""
    prompts = WorldBuilderPrompts()
    
    response_text = """
## 世界概述
这是一个现代都市世界。

## 社会结构
- 上层：企业家、高管
- 中层：白领、技术人员
- 底层：工人、服务业从业者

## 文化特征
- 核心价值观：勤劳、诚信、创新
- 主要习俗：春节团圆、中秋赏月

## 环境特点
- 自然环境：江南水乡，四季分明
- 城市环境：现代化都市

## 潜在冲突源
- 社会矛盾：贫富差距、代际冲突
- 资源争夺：房价、教育资源
"""
    
    parsed = prompts.parse_response(response_text)
    assert "世界概述" in parsed
    assert "社会结构" in parsed
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_prompts/test_world_builder_prompts.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现提示词模板**

创建文件 `app/prompts/__init__.py`:

```python
from app.prompts.world_builder_prompts import WorldBuilderPrompts

__all__ = ["WorldBuilderPrompts"]
```

创建文件 `app/prompts/world_builder_prompts.py`:

```python
from typing import Dict, Any
import re


WORLD_BUILDER_SYSTEM_PROMPT = """你是一位专业的世界构建师，擅长创建丰富、真实、有深度的故事世界。

你的职责是：
1. 构建完整的世界设定（时代、地点、社会背景）
2. 设计合理的社会结构和权力分布
3. 创造独特的文化特征和价值观
4. 描述生动的环境特点
5. 识别潜在的冲突源和戏剧张力

你的输出应该：
- 具有内在一致性
- 富有细节和深度
- 为人物命运提供合理的舞台
- 包含足够的戏剧张力潜力

请用中文回答，结构清晰，内容丰富。"""


WORLD_BUILDER_USER_PROMPT = """请基于以下参数构建一个完整的故事世界：

**时代背景**: {era}
**地理范围**: {location}
**社会类型**: {society_type}
**特殊设定**: {special_settings}

请按以下结构输出世界设定：

## 世界概述
（200字左右的世界整体描述）

## 社会结构
（阶层划分、权力分布、社会流动性）

## 文化特征
（核心价值观、主要习俗、禁忌）

## 环境特点
（自然环境、城市环境、关键地点）

## 潜在冲突源
（社会矛盾、资源争夺、可能发生的重大事件）

请确保设定具有内在一致性，并为后续的人物命运发展提供丰富的可能性。"""


class WorldBuilderPrompts:
    """WorldBuilder提示词管理类"""
    
    def __init__(self):
        self.system_prompt = WORLD_BUILDER_SYSTEM_PROMPT
        self.user_prompt_template = WORLD_BUILDER_USER_PROMPT
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.system_prompt
    
    def get_user_prompt(
        self,
        era: str,
        location: str,
        society_type: str,
        special_settings: str = "无"
    ) -> str:
        """获取用户提示词
        
        Args:
            era: 时代背景
            location: 地理范围
            society_type: 社会类型
            special_settings: 特殊设定
            
        Returns:
            str: 格式化后的用户提示词
        """
        return self.user_prompt_template.format(
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )
    
    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析LLM响应
        
        Args:
            response_text: LLM返回的文本
            
        Returns:
            Dict: 解析后的结构化数据
        """
        sections = {
            "世界概述": self._extract_section(response_text, "世界概述", "社会结构"),
            "社会结构": self._extract_section(response_text, "社会结构", "文化特征"),
            "文化特征": self._extract_section(response_text, "文化特征", "环境特点"),
            "环境特点": self._extract_section(response_text, "环境特点", "潜在冲突源"),
            "潜在冲突源": self._extract_section(response_text, "潜在冲突源", None)
        }
        return sections
    
    def _extract_section(
        self, 
        text: str, 
        section_name: str, 
        next_section: str = None
    ) -> str:
        """提取指定章节内容"""
        pattern = rf"##\s*{section_name}\s*\n(.*?)(?=\n##\s|$)"
        if next_section:
            pattern = rf"##\s*{section_name}\s*\n(.*?)(?=\n##\s*{next_section}|$)"
        
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
```

- [ ] **Step 4: 创建测试目录**

创建文件 `tests/test_prompts/__init__.py`:

```python
# Prompts tests
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_prompts/test_world_builder_prompts.py -v
```

Expected: PASS

- [ ] **Step 6: 提交提示词模板**

```bash
git add backend/app/prompts/
git add backend/tests/test_prompts/
git commit -m "feat: implement WorldBuilder prompts"
```

---

## Task 4: WorldBuilder Agent实现

**Files:**
- Create: `backend/app/agents/world_builder.py`
- Test: `backend/tests/test_agents/test_world_builder.py`

- [ ] **Step 1: 编写WorldBuilder Agent测试**

创建文件 `tests/test_agents/test_world_builder.py`:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.world_builder import WorldBuilderAgent
from app.agents.base import AgentConfig, AgentResponse
from app.services.llm_gateway import LLMGateway
from app.config.llm_config import LLMConfigManager


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="world_builder",
        description="World building agent",
        model="qwen-max",
        temperature=0.8
    )


@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=LLMGateway)
    return gateway


@pytest.fixture
def world_builder(agent_config, mock_gateway):
    return WorldBuilderAgent(agent_config, mock_gateway)


def test_world_builder_creation(world_builder):
    """测试WorldBuilder创建"""
    assert world_builder.config.name == "world_builder"
    assert world_builder.config.model == "qwen-max"


@pytest.mark.asyncio
async def test_world_builder_execute(world_builder, mock_gateway):
    """测试WorldBuilder执行"""
    mock_response = MagicMock()
    mock_response.content = """
## 世界概述
这是一个现代都市世界，位于江南水乡杭州。

## 社会结构
- 上层：企业家、高管
- 中层：白领、技术人员
- 底层：工人、服务业从业者

## 文化特征
- 核心价值观：勤劳、诚信、创新

## 环境特点
- 自然环境：江南水乡，四季分明

## 潜在冲突源
- 社会矛盾：贫富差距
"""
    mock_gateway.generate = AsyncMock(return_value=mock_response)
    
    input_data = {
        "era": "现代都市",
        "location": "杭州",
        "society_type": "平稳发展型",
        "special_settings": "无"
    }
    
    response = await world_builder.execute(input_data)
    
    assert response.success is True
    assert "world_state" in response.data


@pytest.mark.asyncio
async def test_world_builder_with_invalid_input(world_builder):
    """测试无效输入处理"""
    input_data = {}
    
    response = await world_builder.execute(input_data)
    
    assert response.success is False
    assert response.error is not None


@pytest.mark.asyncio
async def test_world_builder_update_world(world_builder, mock_gateway):
    """测试更新世界设定"""
    mock_response = MagicMock()
    mock_response.content = "更新后的世界描述..."
    mock_gateway.generate = AsyncMock(return_value=mock_response)
    
    from app.models.world import WorldState, WorldSetting
    
    existing_world = WorldState(
        world_id="world-001",
        setting=WorldSetting(
            era="现代都市",
            location={"province": "浙江", "city": "杭州"},
            society_type="平稳发展型"
        )
    )
    
    input_data = {
        "action": "update",
        "world": existing_world,
        "update_request": "添加新的社会事件"
    }
    
    response = await world_builder.execute(input_data)
    
    assert response.success is True
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_agents/test_world_builder.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现WorldBuilder Agent**

创建文件 `app/agents/world_builder.py`:

```python
from typing import Dict, Any, Optional
from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.models.world import (
    WorldState,
    WorldSetting,
    SocialStructure,
    CulturalFeature,
    EnvironmentDescription,
    ConflictSource
)
from app.prompts.world_builder_prompts import WorldBuilderPrompts
import uuid
from datetime import datetime


class WorldBuilderAgent(BaseAgent):
    """世界构建Agent
    
    负责创建和维护故事世界的基础设定。
    """
    
    def __init__(self, config: AgentConfig, llm_gateway):
        super().__init__(config, llm_gateway)
        self.prompts = WorldBuilderPrompts()
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行世界构建任务
        
        Args:
            input_data: 输入数据，包含：
                - action: "create" 或 "update"
                - era: 时代背景
                - location: 地理范围
                - society_type: 社会类型
                - special_settings: 特殊设定（可选）
                - world: 现有世界（更新时需要）
                
        Returns:
            AgentResponse: 包含world_state的响应
        """
        try:
            action = input_data.get("action", "create")
            
            if action == "create":
                return await self._create_world(input_data)
            elif action == "update":
                return await self._update_world(input_data)
            else:
                return AgentResponse(
                    success=False,
                    error=f"Unknown action: {action}"
                )
                
        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )
    
    async def _create_world(self, input_data: Dict[str, Any]) -> AgentResponse:
        """创建新世界"""
        era = input_data.get("era")
        location = input_data.get("location")
        society_type = input_data.get("society_type")
        special_settings = input_data.get("special_settings", "无")
        
        if not all([era, location, society_type]):
            return AgentResponse(
                success=False,
                error="Missing required fields: era, location, society_type"
            )
        
        user_prompt = self.prompts.get_user_prompt(
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )
        
        response_text = await self.generate(
            prompt=user_prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        world_state = self._parse_to_world_state(
            response_text,
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )
        
        return AgentResponse(
            success=True,
            data={
                "world_state": world_state.model_dump(),
                "raw_response": response_text
            },
            metadata={
                "agent": "world_builder",
                "action": "create"
            }
        )
    
    async def _update_world(self, input_data: Dict[str, Any]) -> AgentResponse:
        """更新现有世界"""
        world_data = input_data.get("world")
        update_request = input_data.get("update_request", "")
        
        if not world_data:
            return AgentResponse(
                success=False,
                error="Missing world data for update"
            )
        
        update_prompt = f"""
当前世界设定：
{world_data}

更新请求：{update_request}

请根据更新请求，提供更新后的相关部分内容。
"""
        
        response_text = await self.generate(
            prompt=update_prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        return AgentResponse(
            success=True,
            data={
                "update_response": response_text
            },
            metadata={
                "agent": "world_builder",
                "action": "update"
            }
        )
    
    def _parse_to_world_state(
        self,
        response_text: str,
        era: str,
        location: str,
        society_type: str,
        special_settings: str = "无"
    ) -> WorldState:
        """将LLM响应解析为WorldState对象"""
        parsed = self.prompts.parse_response(response_text)
        
        world_id = f"world-{uuid.uuid4().hex[:8]}"
        
        setting = WorldSetting(
            era=era,
            location={"description": location},
            society_type=society_type,
            special_settings=[special_settings] if special_settings != "无" else []
        )
        
        social_structure = self._parse_social_structure(parsed.get("社会结构", ""))
        cultural_features = self._parse_cultural_features(parsed.get("文化特征", ""))
        environment = self._parse_environment(parsed.get("环境特点", ""))
        conflict_sources = self._parse_conflicts(parsed.get("潜在冲突源", ""))
        
        return WorldState(
            world_id=world_id,
            setting=setting,
            social_structure=social_structure,
            cultural_features=cultural_features,
            environment=environment,
            conflict_sources=conflict_sources
        )
    
    def _parse_social_structure(self, text: str) -> Optional[SocialStructure]:
        """解析社会结构"""
        if not text:
            return None
        
        classes = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                class_name = line.lstrip("-• ").split("：")[0].split(":")[0].strip()
                if class_name:
                    classes.append(class_name)
        
        return SocialStructure(classes=classes) if classes else None
    
    def _parse_cultural_features(self, text: str) -> Optional[CulturalFeature]:
        """解析文化特征"""
        if not text:
            return None
        
        core_values = []
        customs = []
        
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if "核心价值观" in line or "价值观" in line:
                values_str = line.split("：")[-1].split(":")[-1].strip()
                core_values = [v.strip() for v in values_str.split("、") if v.strip()]
            elif "习俗" in line:
                customs_str = line.split("：")[-1].split(":")[-1].strip()
                customs = [c.strip() for c in customs_str.split("、") if c.strip()]
        
        return CulturalFeature(
            core_values=core_values,
            customs=customs
        ) if core_values or customs else None
    
    def _parse_environment(self, text: str) -> Optional[EnvironmentDescription]:
        """解析环境描述"""
        if not text:
            return None
        
        natural_env = ""
        urban_env = ""
        key_locations = []
        
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if "自然" in line:
                natural_env = line.split("：")[-1].split(":")[-1].strip()
            elif "城市" in line:
                urban_env = line.split("：")[-1].split(":")[-1].strip()
        
        return EnvironmentDescription(
            natural_environment=natural_env,
            urban_environment=urban_env,
            key_locations=key_locations
        )
    
    def _parse_conflicts(self, text: str) -> list:
        """解析冲突源"""
        if not text:
            return []
        
        social_contradictions = []
        resource_competition = []
        
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                conflict = line.lstrip("-• ").strip()
                if "矛盾" in line or "冲突" in line:
                    social_contradictions.append(conflict)
                else:
                    resource_competition.append(conflict)
        
        if social_contradictions or resource_competition:
            return [ConflictSource(
                social_contradictions=social_contradictions,
                resource_competition=resource_competition
            )]
        return []
```

- [ ] **Step 4: 更新agents/__init__.py**

更新文件 `app/agents/__init__.py`:

```python
from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.agents.world_builder import WorldBuilderAgent

__all__ = ["BaseAgent", "AgentConfig", "AgentResponse", "WorldBuilderAgent"]
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_agents/test_world_builder.py -v
```

Expected: PASS

- [ ] **Step 6: 提交WorldBuilder Agent**

```bash
git add backend/app/agents/
git add backend/tests/test_agents/
git commit -m "feat: implement WorldBuilderAgent"
```

---

## Task 5: 世界设定模板配置

**Files:**
- Create: `backend/config/world_templates.yaml`
- Create: `backend/app/services/world_template_manager.py`
- Test: `backend/tests/test_services/test_world_template_manager.py`

- [ ] **Step 1: 编写模板管理器测试**

创建文件 `tests/test_services/test_world_template_manager.py`:

```python
import pytest
from app.services.world_template_manager import WorldTemplateManager


@pytest.fixture
def template_manager():
    return WorldTemplateManager()


def test_template_manager_creation(template_manager):
    """测试模板管理器创建"""
    assert template_manager is not None


def test_list_templates(template_manager):
    """测试列出模板"""
    templates = template_manager.list_templates()
    assert isinstance(templates, list)


def test_get_template(template_manager):
    """测试获取模板"""
    template = template_manager.get_template("modern_urban")
    assert template is not None
    assert template.get("era") is not None


def test_get_nonexistent_template(template_manager):
    """测试获取不存在的模板"""
    template = template_manager.get_template("nonexistent")
    assert template is None
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_services/test_world_template_manager.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 创建世界模板配置**

创建文件 `config/world_templates.yaml`:

```yaml
templates:
  modern_urban:
    name: "现代都市"
    description: "现代城市背景，适合都市情感、职场故事"
    era: "现代都市"
    location: "杭州"
    society_type: "平稳发展型"
    special_settings: []
    default_conflicts:
      - "贫富差距"
      - "代际冲突"
      - "职场竞争"
    default_culture:
      core_values:
        - "勤劳"
        - "诚信"
        - "创新"
      customs:
        - "春节团圆"
        - "中秋赏月"

  ancient_wuxia:
    name: "古代武侠"
    description: "古代武侠世界，适合江湖恩怨、侠义故事"
    era: "古代"
    location: "中原"
    society_type: "武侠世界"
    special_settings:
      - "武林门派"
      - "江湖恩怨"
    default_conflicts:
      - "门派争斗"
      - "正邪对立"
      - "江湖仇杀"
    default_culture:
      core_values:
        - "侠义"
        - "忠诚"
        - "信义"
      customs:
        - "拜师学艺"
        - "武林大会"

  republican:
    name: "民国时期"
    description: "民国背景，适合家族恩怨、时代变迁故事"
    era: "民国"
    location: "上海"
    society_type: "动荡变革型"
    special_settings:
      - "新旧交替"
      - "家族企业"
    default_conflicts:
      - "新旧思想冲突"
      - "家族恩怨"
      - "民族危机"
    default_culture:
      core_values:
        - "家族荣誉"
        - "传统美德"
        - "革新精神"
      customs:
        - "祭祖"
        - "包办婚姻"

  future_sf:
    name: "未来科幻"
    description: "未来科幻世界，适合科技伦理、人类命运故事"
    era: "未来"
    location: "新世界城"
    society_type: "科技主导型"
    special_settings:
      - "人工智能"
      - "虚拟现实"
      - "太空探索"
    default_conflicts:
      - "人机矛盾"
      - "资源争夺"
      - "伦理困境"
    default_culture:
      core_values:
        - "创新"
        - "效率"
        - "平等"
      customs:
        - "虚拟聚会"
        - "数据祭祀"
```

- [ ] **Step 4: 实现模板管理器**

创建文件 `app/services/world_template_manager.py`:

```python
from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path


class WorldTemplateManager:
    """世界模板管理器"""
    
    def __init__(self, config_path: str = "config/world_templates.yaml"):
        self.config_path = Path(config_path)
        self._templates: Dict[str, Any] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """加载模板配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self._templates = config.get("templates", {})
        else:
            self._templates = self._get_default_templates()
    
    def _get_default_templates(self) -> Dict[str, Any]:
        """获取默认模板"""
        return {
            "modern_urban": {
                "name": "现代都市",
                "era": "现代都市",
                "location": "杭州",
                "society_type": "平稳发展型"
            }
        }
    
    def list_templates(self) -> List[str]:
        """列出所有模板名称"""
        return list(self._templates.keys())
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取指定模板"""
        return self._templates.get(template_id)
    
    def get_template_for_builder(self, template_id: str) -> Dict[str, Any]:
        """获取用于WorldBuilder的模板数据"""
        template = self.get_template(template_id)
        if not template:
            return {}
        
        return {
            "era": template.get("era", ""),
            "location": template.get("location", ""),
            "society_type": template.get("society_type", ""),
            "special_settings": ", ".join(template.get("special_settings", []))
        }
```

- [ ] **Step 5: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_services/test_world_template_manager.py -v
```

Expected: PASS

- [ ] **Step 6: 提交模板配置**

```bash
git add backend/config/world_templates.yaml
git add backend/app/services/world_template_manager.py
git add backend/tests/test_services/test_world_template_manager.py
git commit -m "feat: implement world templates configuration"
```

---

## Task 6: 集成测试

**Files:**
- Create: `backend/tests/test_integration/test_world_builder_integration.py`

- [ ] **Step 1: 编写集成测试**

创建文件 `tests/test_integration/test_world_builder_integration.py`:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.agents.world_builder import WorldBuilderAgent
from app.agents.base import AgentConfig
from app.services.llm_gateway import LLMGateway
from app.config.llm_config import LLMConfigManager
from app.services.world_template_manager import WorldTemplateManager


@pytest.fixture
def config_manager():
    manager = LLMConfigManager()
    manager.load_config()
    return manager


@pytest.fixture
def llm_gateway(config_manager):
    return LLMGateway(config_manager)


@pytest.fixture
def template_manager():
    return WorldTemplateManager()


@pytest.fixture
def world_builder(llm_gateway):
    config = AgentConfig(
        name="world_builder",
        model="qwen-max",
        temperature=0.8
    )
    return WorldBuilderAgent(config, llm_gateway)


class TestWorldBuilderIntegration:
    """WorldBuilder集成测试"""
    
    def test_template_manager_integration(self, template_manager):
        """测试模板管理器集成"""
        templates = template_manager.list_templates()
        assert len(templates) > 0
        
        template = template_manager.get_template("modern_urban")
        assert template is not None
    
    @pytest.mark.asyncio
    async def test_world_builder_with_template(self, world_builder, template_manager):
        """测试使用模板创建世界"""
        template_data = template_manager.get_template_for_builder("modern_urban")
        
        mock_response = MagicMock()
        mock_response.content = """
## 世界概述
现代都市杭州，江南水乡。

## 社会结构
- 上层：企业家
- 中层：白领
- 底层：工人

## 文化特征
- 核心价值观：勤劳、诚信

## 环境特点
- 自然环境：江南水乡

## 潜在冲突源
- 社会矛盾：贫富差距
"""
        
        with patch.object(world_builder.llm_gateway, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = mock_response
            
            response = await world_builder.execute(template_data)
            
            assert response.success is True
            assert "world_state" in response.data
    
    def test_full_workflow(self, template_manager):
        """测试完整工作流"""
        template = template_manager.get_template("modern_urban")
        assert template is not None
        
        builder_input = template_manager.get_template_for_builder("modern_urban")
        assert builder_input["era"] == "现代都市"
```

- [ ] **Step 2: 运行集成测试**

```bash
cd backend
poetry run pytest tests/test_integration/test_world_builder_integration.py -v
```

Expected: PASS

- [ ] **Step 3: 运行所有测试**

```bash
cd backend
poetry run pytest tests/ -v
```

Expected: All tests PASS

- [ ] **Step 4: 提交集成测试**

```bash
git add backend/tests/test_integration/test_world_builder_integration.py
git commit -m "test: add WorldBuilder integration tests"
```

---

## 验证清单

- [ ] 所有测试通过
- [ ] Agent基类可正常继承
- [ ] WorldBuilder Agent可创建世界
- [ ] 模板系统正常工作
- [ ] 与LLM Gateway集成正常
- [ ] 代码符合项目规范

---

**计划完成，保存到 `docs/plans/2026-04-01-worldbuilder-agent.md`。**
