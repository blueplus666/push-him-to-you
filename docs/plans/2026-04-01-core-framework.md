# Core Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现核心框架的状态管理、事件引擎和Agent协调器，为整个系统提供稳定的基础设施。

**Architecture:** 采用事件驱动架构，State Store作为单一真相源，Event Bus负责模块间通信，Orchestrator管理整个模拟生命周期。

**Tech Stack:** Python 3.10+, FastAPI, SQLite, Pydantic, asyncio

---

## 文件结构

```
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── state_store.py         # 状态存储接口和SQLite实现
│   │   ├── event_bus.py           # 事件总线实现
│   │   ├── orchestrator.py        # Agent协调器
│   │   └── exceptions.py          # 自定义异常
│   ├── models/
│   │   ├── __init__.py
│   │   ├── world.py               # 世界状态模型
│   │   ├── character.py           # 人物状态模型
│   │   ├── event.py               # 事件模型
│   │   └── simulation.py          # 模拟上下文模型
│   └── config.py                  # 配置管理
├── tests/
│   ├── test_core/
│   │   ├── __init__.py
│   │   ├── test_state_store.py
│   │   ├── test_event_bus.py
│   │   └── test_orchestrator.py
│   └── conftest.py                # pytest配置和fixtures
├── data/
│   └── db/                        # SQLite数据库目录
└── pyproject.toml                 # Poetry配置
```

---

## Task 1: 项目初始化和依赖配置

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: 创建Poetry配置文件**

```toml
[tool.poetry]
name = "push-him-to-you"
version = "0.1.0"
description = "AI驱动的命运模拟与小说生成系统"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
pydantic = "^2.5.0"
python-dotenv = "^1.0.0"
pyyaml = "^6.0"
openai = "^1.12.0"
zhipuai = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
black = "^24.1.0"
ruff = "^0.2.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
line-length = 100
target-version = "py310"
```

- [ ] **Step 2: 创建基础包结构**

```bash
mkdir -p backend/app/{core,models}
mkdir -p backend/tests/test_core
mkdir -p backend/data/db
touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py
touch backend/tests/__init__.py
touch backend/tests/test_core/__init__.py
```

- [ ] **Step 3: 创建pytest配置文件**

```python
import pytest
import asyncio
from pathlib import Path
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_db_path(tmp_path):
    """提供临时数据库路径"""
    return str(tmp_path / "test.db")
```

- [ ] **Step 4: 安装依赖**

```bash
cd backend
poetry install
```

Expected: 所有依赖成功安装

- [ ] **Step 5: 提交初始化**

```bash
git add backend/
git commit -m "chore: initialize project structure and dependencies"
```

---

## Task 2: 数据模型实现

**Files:**
- Create: `backend/app/models/world.py`
- Create: `backend/app/models/character.py`
- Create: `backend/app/models/event.py`
- Create: `backend/app/models/simulation.py`
- Test: `backend/tests/test_models/` (创建测试目录)

- [ ] **Step 1: 编写世界状态模型测试**

```python
import pytest
from datetime import datetime
from pydantic import ValidationError

def test_world_state_creation():
    from app.models.world import WorldState
    
    world = WorldState(
        world_id="test-001",
        era="现代都市",
        location={"province": "浙江", "city": "杭州"},
        time_span={"start": 1990, "end": 2025},
        society_type="平稳发展型",
        special_settings=["包含重大社会事件"],
        current_time=datetime.now(),
        environment_state={},
        social_events=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert world.world_id == "test-001"
    assert world.era == "现代都市"
    assert world.location["city"] == "杭州"

def test_world_state_validation_error():
    from app.models.world import WorldState
    
    with pytest.raises(ValidationError):
        WorldState(
            world_id="test-001",
            era="现代都市",
            # 缺少必需字段
        )
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_models/test_world.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现世界状态模型**

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class WorldState(BaseModel):
    """世界状态模型"""
    world_id: str = Field(..., description="世界唯一标识")
    era: str = Field(..., description="时代背景")
    location: Dict[str, str] = Field(..., description="地理位置")
    time_span: Dict[str, int] = Field(..., description="时间跨度")
    society_type: str = Field(..., description="社会类型")
    special_settings: List[str] = Field(default_factory=list, description="特殊设定")
    
    current_time: datetime = Field(..., description="当前时间")
    environment_state: Dict[str, Any] = Field(default_factory=dict, description="环境状态")
    social_events: List[Dict[str, Any]] = Field(default_factory=list, description="社会事件列表")
    
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "world_id": "world-001",
                "era": "现代都市",
                "location": {"province": "浙江", "city": "杭州"},
                "time_span": {"start": 1990, "end": 2025},
                "society_type": "平稳发展型",
                "special_settings": ["包含重大社会事件"],
                "current_time": "2024-01-01T00:00:00",
                "environment_state": {},
                "social_events": []
            }
        }
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_models/test_world.py -v
```

Expected: PASS

- [ ] **Step 5: 编写人物状态模型测试**

```python
import pytest
from datetime import datetime
from pydantic import ValidationError

def test_character_state_creation():
    from app.models.character import CharacterState
    
    character = CharacterState(
        character_id="char-001",
        world_id="world-001",
        name="李明",
        gender="male",
        birth_date=datetime(1990, 3, 15),
        age=25.0,
        personality={
            "openness": 75,
            "conscientiousness": 68,
            "extraversion": 45,
            "agreeableness": 82,
            "neuroticism": 35
        },
        current_state={
            "occupation": "软件工程师",
            "income_level": 4,
            "relationship_status": "single"
        },
        needs={
            "physiological": 85,
            "safety": 78,
            "belonging": 65
        },
        skills={
            "technical": ["编程", "数据分析"],
            "social": ["沟通", "团队协作"]
        },
        values={
            "core_values": ["家庭", "自由", "成长"],
            "life_goal": "成为一名技术专家"
        },
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert character.character_id == "char-001"
    assert character.name == "李明"
    assert character.personality["openness"] == 75

def test_character_personality_validation():
    from app.models.character import CharacterState
    
    # 测试人格值范围验证
    with pytest.raises(ValidationError):
        CharacterState(
            character_id="char-001",
            world_id="world-001",
            name="李明",
            gender="male",
            birth_date=datetime(1990, 3, 15),
            age=25.0,
            personality={
                "openness": 150,  # 超出范围
                "conscientiousness": 68,
                "extraversion": 45,
                "agreeableness": 82,
                "neuroticism": 35
            },
            current_state={},
            needs={},
            skills={},
            values={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
```

- [ ] **Step 6: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_models/test_character.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 7: 实现人物状态模型**

```python
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any, Optional
from datetime import datetime

class CharacterState(BaseModel):
    """人物状态模型"""
    character_id: str = Field(..., description="人物唯一标识")
    world_id: str = Field(..., description="所属世界ID")
    name: str = Field(..., description="姓名")
    gender: str = Field(..., description="性别")
    birth_date: datetime = Field(..., description="出生日期")
    age: float = Field(..., ge=0, le=120, description="年龄")
    
    personality: Dict[str, int] = Field(
        ...,
        description="大五人格维度：openness, conscientiousness, extraversion, agreeableness, neuroticism"
    )
    
    current_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="当前状态：occupation, income_level, relationship_status, health_status, mental_state, life_satisfaction"
    )
    
    needs: Dict[str, int] = Field(
        default_factory=dict,
        description="马斯洛需求层次：physiological, safety, belonging, esteem, self_actualization"
    )
    
    skills: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="技能分类：technical, social, creative, physical"
    )
    
    values: Dict[str, Any] = Field(
        default_factory=dict,
        description="价值观：core_values, life_goal, fear"
    )
    
    relationship_graph_id: Optional[str] = Field(None, description="关系网络ID")
    event_timeline_id: Optional[str] = Field(None, description="事件时间线ID")
    
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    @field_validator('personality')
    @classmethod
    def validate_personality(cls, v):
        """验证人格值范围"""
        for key, value in v.items():
            if not (0 <= value <= 100):
                raise ValueError(f"Personality value for {key} must be between 0 and 100")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "character_id": "char-001",
                "world_id": "world-001",
                "name": "李明",
                "gender": "male",
                "birth_date": "1990-03-15T00:00:00",
                "age": 25.0,
                "personality": {
                    "openness": 75,
                    "conscientiousness": 68,
                    "extraversion": 45,
                    "agreeableness": 82,
                    "neuroticism": 35
                },
                "current_state": {
                    "occupation": "软件工程师",
                    "income_level": 4
                }
            }
        }
```

- [ ] **Step 8: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_models/test_character.py -v
```

Expected: PASS

- [ ] **Step 9: 实现事件模型**

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    """事件类型枚举"""
    LIFE_STAGE = "life_stage"
    CAUSAL = "causal"
    RANDOM = "random"
    CHARACTER_DRIVEN = "character_driven"
    RELATIONSHIP = "relationship"
    ENVIRONMENT = "environment"

class Event(BaseModel):
    """事件模型"""
    event_id: str = Field(..., description="事件唯一标识")
    simulation_id: str = Field(..., description="所属模拟ID")
    event_type: EventType = Field(..., description="事件类型")
    timestamp: datetime = Field(..., description="事件发生时间")
    age_at_event: float = Field(..., ge=0, le=120, description="事件发生时年龄")
    
    title: str = Field(..., description="事件标题")
    description: str = Field(..., description="事件描述")
    intensity: int = Field(..., ge=1, le=10, description="事件强度1-10")
    
    participants: List[str] = Field(default_factory=list, description="参与者ID列表")
    
    causes: List[str] = Field(default_factory=list, description="导致此事件的事件ID列表")
    effects: List[str] = Field(default_factory=list, description="此事件导致的事件ID列表")
    
    impact: Dict[str, Any] = Field(
        default_factory=dict,
        description="事件影响：personality_changes, relationship_changes, state_changes"
    )
    
    is_spark_moment: bool = Field(default=False, description="是否为闪光时刻")
    spark_score: Optional[float] = Field(None, ge=0, le=10, description="闪光时刻评分")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    
    class Config:
        use_enum_values = True
```

- [ ] **Step 10: 实现模拟上下文模型**

```python
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum

class SimulationStatus(str, Enum):
    """模拟状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ERROR = "error"

class SimulationContext(BaseModel):
    """模拟上下文模型"""
    simulation_id: str = Field(..., description="模拟唯一标识")
    world_id: str = Field(..., description="所属世界ID")
    character_ids: List[str] = Field(default_factory=list, description="参与人物ID列表")
    
    status: SimulationStatus = Field(default=SimulationStatus.IDLE, description="模拟状态")
    current_time: datetime = Field(..., description="当前时间")
    current_age: float = Field(default=0.0, ge=0, le=120, description="当前年龄")
    
    total_events: int = Field(default=0, ge=0, description="总事件数")
    spark_moments_count: int = Field(default=0, ge=0, description="闪光时刻数")
    
    speed: float = Field(default=1.0, ge=0.1, le=10.0, description="模拟速度")
    
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    class Config:
        use_enum_values = True
```

- [ ] **Step 11: 提交数据模型**

```bash
git add backend/app/models/
git add backend/tests/test_models/
git commit -m "feat: implement data models for world, character, event, and simulation"
```

---

## Task 3: 状态存储实现

**Files:**
- Create: `backend/app/core/state_store.py`
- Create: `backend/app/core/exceptions.py`
- Test: `backend/tests/test_core/test_state_store.py`

- [ ] **Step 1: 编写StateStore接口测试**

```python
import pytest
from datetime import datetime
from app.core.state_store import StateStore, SQLiteStateStore
from app.models.world import WorldState

@pytest.mark.asyncio
async def test_state_store_interface():
    """测试StateStore接口定义"""
    store = SQLiteStateStore(":memory:")
    
    # 测试创建世界
    world = WorldState(
        world_id="test-001",
        era="现代都市",
        location={"province": "浙江", "city": "杭州"},
        time_span={"start": 1990, "end": 2025},
        society_type="平稳发展型",
        special_settings=[],
        current_time=datetime.now(),
        environment_state={},
        social_events=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    world_id = await store.create_world(world)
    assert world_id == "test-001"
    
    # 测试获取世界
    retrieved = await store.get_world("test-001")
    assert retrieved is not None
    assert retrieved.world_id == "test-001"
    assert retrieved.era == "现代都市"
    
    # 测试获取不存在的世界
    not_found = await store.get_world("non-existent")
    assert not_found is None

@pytest.mark.asyncio
async def test_state_store_update_world():
    """测试更新世界状态"""
    store = SQLiteStateStore(":memory:")
    
    # 创建世界
    world = WorldState(
        world_id="test-001",
        era="现代都市",
        location={"province": "浙江", "city": "杭州"},
        time_span={"start": 1990, "end": 2025},
        society_type="平稳发展型",
        special_settings=[],
        current_time=datetime.now(),
        environment_state={},
        social_events=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    await store.create_world(world)
    
    # 更新世界
    success = await store.update_world("test-001", {
        "era": "古代",
        "society_type": "封建社会"
    })
    assert success is True
    
    # 验证更新
    updated = await store.get_world("test-001")
    assert updated.era == "古代"
    assert updated.society_type == "封建社会"
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd backend
poetry run pytest tests/test_core/test_state_store.py -v
```

Expected: FAIL - ModuleNotFoundError

- [ ] **Step 3: 实现自定义异常**

```python
class PushHimToYouError(Exception):
    """基础异常类"""
    pass

class StateStoreError(PushHimToYouError):
    """状态存储异常"""
    pass

class WorldNotFoundError(StateStoreError):
    """世界未找到"""
    pass

class CharacterNotFoundError(StateStoreError):
    """人物未找到"""
    pass

class EventNotFoundError(StateStoreError):
    """事件未找到"""
    pass

class SimulationNotFoundError(StateStoreError):
    """模拟未找到"""
    pass
```

- [ ] **Step 4: 实现StateStore抽象接口**

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime

class StateStore(ABC):
    """状态存储抽象接口"""
    
    # ========== World State ==========
    @abstractmethod
    async def create_world(self, world_state: 'WorldState') -> str:
        """创建世界状态"""
        pass
    
    @abstractmethod
    async def get_world(self, world_id: str) -> Optional['WorldState']:
        """获取世界状态"""
        pass
    
    @abstractmethod
    async def update_world(self, world_id: str, updates: Dict[str, Any]) -> bool:
        """更新世界状态"""
        pass
    
    @abstractmethod
    async def delete_world(self, world_id: str) -> bool:
        """删除世界状态"""
        pass
    
    # ========== Character State ==========
    @abstractmethod
    async def create_character(self, character_state: 'CharacterState') -> str:
        """创建人物状态"""
        pass
    
    @abstractmethod
    async def get_character(self, character_id: str) -> Optional['CharacterState']:
        """获取人物状态"""
        pass
    
    @abstractmethod
    async def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """更新人物状态"""
        pass
    
    @abstractmethod
    async def delete_character(self, character_id: str) -> bool:
        """删除人物状态"""
        pass
    
    @abstractmethod
    async def list_characters(self, world_id: str) -> List['CharacterState']:
        """列出世界中的所有人物"""
        pass
    
    # ========== Event ==========
    @abstractmethod
    async def create_event(self, event: 'Event') -> str:
        """创建事件"""
        pass
    
    @abstractmethod
    async def get_event(self, event_id: str) -> Optional['Event']:
        """获取事件"""
        pass
    
    @abstractmethod
    async def list_events(
        self,
        simulation_id: str,
        character_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List['Event']:
        """列出事件（支持多种过滤条件）"""
        pass
    
    # ========== Simulation Context ==========
    @abstractmethod
    async def create_simulation(self, simulation_context: 'SimulationContext') -> str:
        """创建模拟上下文"""
        pass
    
    @abstractmethod
    async def get_simulation(self, simulation_id: str) -> Optional['SimulationContext']:
        """获取模拟上下文"""
        pass
    
    @abstractmethod
    async def update_simulation(self, simulation_id: str, updates: Dict[str, Any]) -> bool:
        """更新模拟上下文"""
        pass
    
    @abstractmethod
    async def delete_simulation(self, simulation_id: str) -> bool:
        """删除模拟上下文"""
        pass
```

- [ ] **Step 5: 实现SQLiteStateStore（第一部分：初始化和世界管理）**

```python
import sqlite3
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from .state_store import StateStore
from .exceptions import WorldNotFoundError, CharacterNotFoundError
from app.models.world import WorldState
from app.models.character import CharacterState
from app.models.event import Event
from app.models.simulation import SimulationContext

logger = logging.getLogger(__name__)

class SQLiteStateStore(StateStore):
    """基于SQLite的状态存储实现"""
    
    def __init__(self, db_path: str = "data/db/push_him_to_you.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建世界状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS world_states (
                    world_id TEXT PRIMARY KEY,
                    era TEXT NOT NULL,
                    location TEXT NOT NULL,
                    time_span TEXT NOT NULL,
                    society_type TEXT NOT NULL,
                    special_settings TEXT NOT NULL,
                    current_time TEXT NOT NULL,
                    environment_state TEXT NOT NULL,
                    social_events TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # 创建人物状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS character_states (
                    character_id TEXT PRIMARY KEY,
                    world_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    age REAL NOT NULL,
                    personality TEXT NOT NULL,
                    current_state TEXT NOT NULL,
                    needs TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    values TEXT NOT NULL,
                    relationship_graph_id TEXT,
                    event_timeline_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (world_id) REFERENCES world_states(world_id)
                )
            ''')
            
            # 创建事件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    simulation_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    age_at_event REAL NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    intensity INTEGER NOT NULL,
                    participants TEXT NOT NULL,
                    causes TEXT NOT NULL,
                    effects TEXT NOT NULL,
                    impact TEXT NOT NULL,
                    is_spark_moment INTEGER NOT NULL DEFAULT 0,
                    spark_score REAL,
                    metadata TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 创建模拟上下文表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS simulation_contexts (
                    simulation_id TEXT PRIMARY KEY,
                    world_id TEXT NOT NULL,
                    character_ids TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_time TEXT NOT NULL,
                    current_age REAL NOT NULL,
                    total_events INTEGER NOT NULL DEFAULT 0,
                    spark_moments_count INTEGER NOT NULL DEFAULT 0,
                    speed REAL NOT NULL DEFAULT 1.0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (world_id) REFERENCES world_states(world_id)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_simulation ON events(simulation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_characters_world ON character_states(world_id)')
            
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
    
    # ========== World State Implementation ==========
    async def create_world(self, world_state: WorldState) -> str:
        """创建世界状态"""
        def _create():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO world_states VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    world_state.world_id,
                    world_state.era,
                    json.dumps(world_state.location, ensure_ascii=False),
                    json.dumps(world_state.time_span),
                    world_state.society_type,
                    json.dumps(world_state.special_settings, ensure_ascii=False),
                    world_state.current_time.isoformat(),
                    json.dumps(world_state.environment_state, ensure_ascii=False),
                    json.dumps(world_state.social_events, ensure_ascii=False),
                    world_state.created_at.isoformat(),
                    world_state.updated_at.isoformat()
                ))
                conn.commit()
                return world_state.world_id
        
        return await asyncio.get_event_loop().run_in_executor(None, _create)
    
    async def get_world(self, world_id: str) -> Optional[WorldState]:
        """获取世界状态"""
        def _get():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM world_states WHERE world_id = ?', (world_id,))
                row = cursor.fetchone()
                if row:
                    return WorldState(
                        world_id=row[0],
                        era=row[1],
                        location=json.loads(row[2]),
                        time_span=json.loads(row[3]),
                        society_type=row[4],
                        special_settings=json.loads(row[5]),
                        current_time=datetime.fromisoformat(row[6]),
                        environment_state=json.loads(row[7]),
                        social_events=json.loads(row[8]),
                        created_at=datetime.fromisoformat(row[9]),
                        updated_at=datetime.fromisoformat(row[10])
                    )
                return None
        
        return await asyncio.get_event_loop().run_in_executor(None, _get)
    
    async def update_world(self, world_id: str, updates: Dict[str, Any]) -> bool:
        """更新世界状态"""
        def _update():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 构建UPDATE语句
                set_clauses = []
                values = []
                for key, value in updates.items():
                    if key in ['location', 'time_span', 'special_settings', 'environment_state', 'social_events']:
                        set_clauses.append(f"{key} = ?")
                        values.append(json.dumps(value, ensure_ascii=False))
                    elif key == 'current_time':
                        set_clauses.append(f"{key} = ?")
                        values.append(value.isoformat())
                    else:
                        set_clauses.append(f"{key} = ?")
                        values.append(value)
                
                # 添加updated_at
                set_clauses.append("updated_at = ?")
                values.append(datetime.now().isoformat())
                values.append(world_id)
                
                query = f"UPDATE world_states SET {', '.join(set_clauses)} WHERE world_id = ?"
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
        
        return await asyncio.get_event_loop().run_in_executor(None, _update)
    
    async def delete_world(self, world_id: str) -> bool:
        """删除世界状态"""
        def _delete():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM world_states WHERE world_id = ?', (world_id,))
                conn.commit()
                return cursor.rowcount > 0
        
        return await asyncio.get_event_loop().run_in_executor(None, _delete)
```

- [ ] **Step 6: 运行测试验证通过**

```bash
cd backend
poetry run pytest tests/test_core/test_state_store.py::test_state_store_interface -v
poetry run pytest tests/test_core/test_state_store.py::test_state_store_update_world -v
```

Expected: PASS

- [ ] **Step 7: 提交StateStore实现**

```bash
git add backend/app/core/
git add backend/tests/test_core/
git commit -m "feat: implement StateStore with SQLite backend"
```

---

**计划继续...由于篇幅限制，完整计划包含以下后续任务：**

- Task 4: 事件总线实现
- Task 5: Agent协调器实现
- Task 6: 集成测试
- Task 7: 性能优化和文档

**每个任务都遵循相同的TDD模式：编写测试 → 验证失败 → 实现代码 → 验证通过 → 提交。**
