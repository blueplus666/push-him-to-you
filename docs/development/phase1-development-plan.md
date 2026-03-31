# 第一阶段开发计划

**项目名称**: "把他推向你" - AI驱动的命运模拟与小说生成系统  
**阶段**: 第一阶段 - 核心框架与UI/UX  
**时间周期**: 1-2个月  
**文档版本**: v1.0  
**创建日期**: 2026-04-01

---

## 一、阶段目标

### 1.1 核心目标

完成系统的核心框架搭建和完整UI/UX设计，为后续模块开发提供稳定的基础设施。

### 1.2 具体目标

1. **核心框架实现**
   - 状态管理模块（State Store）
   - 事件引擎模块（Event Engine）
   - Agent协调器（Master Orchestrator）
   - LLM Gateway（统一模型网关）

2. **UI/UX完整设计**
   - 参数设置界面
   - 世界构建界面
   - 人物创建界面
   - 人生模拟观察界面
   - 小说生成界面

3. **基础设施搭建**
   - 项目结构初始化
   - 数据库设计与实现
   - API接口设计与实现
   - 前端框架搭建

4. **文档完善**
   - API接口文档
   - 开发指南
   - 部署文档

---

## 二、技术架构

### 2.1 技术栈

**后端**:
- Python 3.10+
- FastAPI (Web框架)
- SQLite (数据库)
- Chroma (向量数据库)
- Redis (缓存，可选)
- Celery (任务队列，可选)

**前端**:
- React 18
- TypeScript
- shadcn/ui (UI组件库)
- Zustand (状态管理)
- React Router (路由)
- Axios (HTTP客户端)
- WebSocket (实时通信)

**开发工具**:
- Poetry (Python依赖管理)
- npm/pnpm (前端依赖管理)
- Docker (容器化)
- Git (版本控制)

### 2.2 项目结构

```
push-him-to-you/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI应用入口
│   │   ├── config.py                  # 配置管理
│   │   │
│   │   ├── api/                       # API路由
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py          # 模型管理API
│   │   │   │   ├── worlds.py          # 世界构建API
│   │   │   │   ├── characters.py      # 人物管理API
│   │   │   │   ├── simulations.py     # 模拟控制API
│   │   │   │   └── novels.py          # 小说生成API
│   │   │   └── websocket.py           # WebSocket处理
│   │   │
│   │   ├── core/                      # 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py        # Agent协调器
│   │   │   ├── event_bus.py           # 事件总线
│   │   │   ├── state_store.py         # 状态存储
│   │   │   └── exceptions.py          # 异常定义
│   │   │
│   │   ├── models/                    # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── world.py
│   │   │   ├── character.py
│   │   │   ├── event.py
│   │   │   └── simulation.py
│   │   │
│   │   ├── services/                  # 服务层
│   │   │   ├── __init__.py
│   │   │   ├── llm_gateway.py         # LLM网关
│   │   │   ├── llm_adapters/          # LLM适配器
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── qwen_adapter.py
│   │   │   │   ├── glm_adapter.py
│   │   │   │   ├── kimi_adapter.py
│   │   │   │   └── doubao_adapter.py
│   │   │   └── vector_store.py        # 向量存储服务
│   │   │
│   │   ├── agents/                    # Agent模块（第二阶段实现）
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Agent基类
│   │   │   └── registry.py            # Agent注册表
│   │   │
│   │   └── utils/                     # 工具函数
│   │       ├── __init__.py
│   │       ├── logger.py
│   │       └── helpers.py
│   │
│   ├── tests/                         # 测试
│   │   ├── __init__.py
│   │   ├── test_api/
│   │   ├── test_core/
│   │   └── test_services/
│   │
│   ├── data/                          # 数据目录
│   │   ├── db/                        # SQLite数据库
│   │   ├── vectors/                   # 向量数据
│   │   └── logs/                      # 日志文件
│   │
│   ├── config/                        # 配置文件
│   │   ├── llm_config.yaml            # LLM配置
│   │   └── app_config.yaml            # 应用配置
│   │
│   ├── pyproject.toml                 # Poetry配置
│   ├── requirements.txt               # 依赖列表
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                   # 应用入口
│   │   ├── App.tsx                    # 根组件
│   │   │
│   │   ├── components/                # 组件
│   │   │   ├── ui/                    # shadcn/ui组件
│   │   │   ├── layout/                # 布局组件
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   │
│   │   │   ├── settings/              # 设置模块
│   │   │   │   ├── ModelConfig.tsx
│   │   │   │   └── ApiKeyManagement.tsx
│   │   │   │
│   │   │   ├── world/                 # 世界构建模块
│   │   │   │   ├── WorldBuilder.tsx
│   │   │   │   └── WorldPreview.tsx
│   │   │   │
│   │   │   ├── character/             # 人物创建模块
│   │   │   │   ├── CharacterCreator.tsx
│   │   │   │   ├── CharacterList.tsx
│   │   │   │   └── PersonalityEditor.tsx
│   │   │   │
│   │   │   ├── simulation/            # 模拟观察模块
│   │   │   │   ├── SimulationControl.tsx
│   │   │   │   ├── EventStream.tsx
│   │   │   │   └── CharacterStatus.tsx
│   │   │   │
│   │   │   └── novel/                 # 小说生成模块
│   │   │       ├── PerspectiveSelector.tsx
│   │   │       ├── NovelPreview.tsx
│   │   │       └── NovelExporter.tsx
│   │   │
│   │   ├── pages/                     # 页面
│   │   │   ├── SettingsPage.tsx
│   │   │   ├── WorldBuilderPage.tsx
│   │   │   ├── CharacterCreatorPage.tsx
│   │   │   ├── SimulationPage.tsx
│   │   │   └── NovelGeneratorPage.tsx
│   │   │
│   │   ├── stores/                    # Zustand状态管理
│   │   │   ├── modelStore.ts
│   │   │   ├── worldStore.ts
│   │   │   ├── characterStore.ts
│   │   │   ├── simulationStore.ts
│   │   │   └── novelStore.ts
│   │   │
│   │   ├── services/                  # API服务
│   │   │   ├── api.ts                 # Axios实例
│   │   │   ├── websocket.ts           # WebSocket服务
│   │   │   ├── modelService.ts
│   │   │   ├── worldService.ts
│   │   │   ├── characterService.ts
│   │   │   ├── simulationService.ts
│   │   │   └── novelService.ts
│   │   │
│   │   ├── hooks/                     # 自定义Hooks
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useSimulation.ts
│   │   │   └── useCharacter.ts
│   │   │
│   │   ├── types/                     # TypeScript类型
│   │   │   ├── models.ts
│   │   │   ├── world.ts
│   │   │   ├── character.ts
│   │   │   ├── event.ts
│   │   │   └── simulation.ts
│   │   │
│   │   ├── lib/                       # 工具库
│   │   │   ├── utils.ts
│   │   │   └── constants.ts
│   │   │
│   │   └── styles/                    # 样式
│   │       ├── globals.css
│   │       └── themes/
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── docs/                              # 文档
│   ├── specs/                         # 设计文档
│   │   └── 2026-04-01-core-framework-design.md
│   ├── llm-providers/                 # LLM提供商文档
│   │   └── 国内大模型接入文档.md
│   ├── api/                           # API文档
│   │   └── api-reference.md
│   └── development/                   # 开发文档
│       ├── setup-guide.md
│       └── deployment-guide.md
│
├── docker-compose.yml                 # Docker编排
├── .env.example                       # 环境变量示例
├── .gitignore
└── README.md                          # 项目说明
```

---

## 三、开发任务分解

### 3.1 Week 1-2: 项目初始化与基础设施

#### 任务1.1: 项目初始化 (2天)

**后端初始化**:
```bash
# 创建项目目录
mkdir -p push-him-to-you/{backend,frontend,docs}

# 初始化Python项目
cd backend
poetry init
poetry add fastapi uvicorn sqlalchemy pydantic python-dotenv pyyaml openai zhipuai

# 创建基础目录结构
mkdir -p app/{api,core,models,services,agents,utils}
mkdir -p data/{db,vectors,logs}
mkdir -p config
mkdir -p tests
```

**前端初始化**:
```bash
# 创建React项目
cd ../frontend
npm create vite@latest . -- --template react-ts

# 安装依赖
npm install @radix-ui/react-icons class-variance-authority clsx tailwind-merge
npm install zustand react-router-dom axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 安装shadcn/ui
npx shadcn-ui@latest init
```

**交付物**:
- [x] 项目目录结构创建完成
- [x] Python环境配置完成
- [x] React环境配置完成
- [x] 基础依赖安装完成

#### 任务1.2: 数据库设计与实现 (2天)

**SQLite数据库Schema设计**:

```sql
-- 世界状态表
CREATE TABLE world_states (
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
);

-- 人物状态表
CREATE TABLE character_states (
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
);

-- 事件表
CREATE TABLE events (
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
);

-- 模拟上下文表
CREATE TABLE simulation_contexts (
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
);

-- LLM配置表
CREATE TABLE llm_configs (
    config_id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    api_key_encrypted TEXT NOT NULL,
    base_url TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 创建索引
CREATE INDEX idx_events_simulation ON events(simulation_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_characters_world ON character_states(world_id);
```

**交付物**:
- [x] 数据库Schema设计完成
- [x] SQLite数据库初始化脚本完成
- [x] 数据库迁移脚本完成
- [x] 数据库连接池配置完成

#### 任务1.3: 核心数据模型实现 (3天)

**Python数据模型**:

```python
# backend/app/models/world.py
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class WorldState(BaseModel):
    world_id: str
    era: str
    location: Dict[str, str]
    time_span: Dict[str, int]
    society_type: str
    special_settings: List[str]
    current_time: datetime
    environment_state: Dict[str, Any]
    social_events: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

# backend/app/models/character.py
class CharacterState(BaseModel):
    character_id: str
    world_id: str
    name: str
    gender: str
    birth_date: datetime
    age: float
    personality: Dict[str, int]
    current_state: Dict[str, Any]
    needs: Dict[str, int]
    skills: Dict[str, List[str]]
    values: Dict[str, Any]
    relationship_graph_id: Optional[str]
    event_timeline_id: Optional[str]
    created_at: datetime
    updated_at: datetime

# backend/app/models/event.py
class Event(BaseModel):
    event_id: str
    simulation_id: str
    event_type: str
    timestamp: datetime
    age_at_event: float
    title: str
    description: str
    intensity: int = Field(ge=1, le=10)
    participants: List[str]
    causes: List[str]
    effects: List[str]
    impact: Dict[str, Any]
    is_spark_moment: bool = False
    spark_score: Optional[float]
    metadata: Dict[str, Any]
    created_at: datetime

# backend/app/models/simulation.py
class SimulationContext(BaseModel):
    simulation_id: str
    world_id: str
    character_ids: List[str]
    status: str
    current_time: datetime
    current_age: float
    total_events: int = 0
    spark_moments_count: int = 0
    speed: float = 1.0
    created_at: datetime
    updated_at: datetime
```

**TypeScript类型定义**:

```typescript
// frontend/src/types/world.ts
export interface WorldState {
  world_id: string;
  era: string;
  location: Record<string, string>;
  time_span: {
    start: number;
    end: number;
  };
  society_type: string;
  special_settings: string[];
  current_time: string;
  environment_state: Record<string, any>;
  social_events: Array<Record<string, any>>;
  created_at: string;
  updated_at: string;
}

// frontend/src/types/character.ts
export interface CharacterState {
  character_id: string;
  world_id: string;
  name: string;
  gender: string;
  birth_date: string;
  age: number;
  personality: {
    openness: number;
    conscientiousness: number;
    extraversion: number;
    agreeableness: number;
    neuroticism: number;
  };
  current_state: Record<string, any>;
  needs: Record<string, number>;
  skills: Record<string, string[]>;
  values: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// frontend/src/types/event.ts
export interface Event {
  event_id: string;
  simulation_id: string;
  event_type: string;
  timestamp: string;
  age_at_event: number;
  title: string;
  description: string;
  intensity: number;
  participants: string[];
  causes: string[];
  effects: string[];
  impact: Record<string, any>;
  is_spark_moment: boolean;
  spark_score?: number;
  metadata: Record<string, any>;
  created_at: string;
}
```

**交付物**:
- [x] Python数据模型完成
- [x] TypeScript类型定义完成
- [x] 数据验证逻辑完成
- [x] 序列化/反序列化测试完成

---

### 3.2 Week 3-4: 核心框架实现

#### 任务2.1: 状态管理模块 (State Store) (3天)

**实现内容**:
- SQLiteStateStore类
- 异步CRUD操作
- 事务管理
- 缓存机制

**代码位置**: `backend/app/core/state_store.py`

**测试用例**:
```python
# backend/tests/test_core/test_state_store.py
import pytest
from app.core.state_store import SQLiteStateStore
from app.models.world import WorldState
from datetime import datetime

@pytest.mark.asyncio
async def test_create_world():
    store = SQLiteStateStore(":memory:")
    
    world = WorldState(
        world_id="test-world-001",
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
    
    world_id = await store.create_world(world)
    assert world_id == "test-world-001"
    
    retrieved = await store.get_world(world_id)
    assert retrieved is not None
    assert retrieved.era == "现代都市"
```

**交付物**:
- [x] StateStore接口定义完成
- [x] SQLiteStateStore实现完成
- [x] 单元测试完成
- [x] 性能测试完成

#### 任务2.2: 事件引擎模块 (Event Engine) (4天)

**实现内容**:
- EventBus类
- 事件发布/订阅机制
- 事件持久化
- 事件溯源

**代码位置**: `backend/app/core/event_bus.py`

**测试用例**:
```python
# backend/tests/test_core/test_event_bus.py
import pytest
from app.core.event_bus import EventBus, Event, EventType

@pytest.mark.asyncio
async def test_event_publish_subscribe():
    bus = EventBus(persist_events=False)
    await bus.start()
    
    received_events = []
    
    async def handler(event: Event):
        received_events.append(event)
    
    bus.subscribe(EventType.SIMULATION_STARTED, handler)
    
    event = Event(
        event_type=EventType.SIMULATION_STARTED,
        source="test",
        data={"simulation_id": "test-001"}
    )
    
    await bus.publish(event)
    await asyncio.sleep(0.1)  # 等待事件处理
    
    assert len(received_events) == 1
    assert received_events[0].data["simulation_id"] == "test-001"
    
    await bus.stop()
```

**交付物**:
- [x] EventBus实现完成
- [x] 事件类型定义完成
- [x] 单元测试完成
- [x] 集成测试完成

#### 任务2.3: Agent协调器 (Orchestrator) (3天)

**实现内容**:
- MasterOrchestrator类
- 模拟生命周期管理
- 任务调度
- 性能监控

**代码位置**: `backend/app/core/orchestrator.py`

**交付物**:
- [x] Orchestrator实现完成
- [x] 模拟控制逻辑完成
- [x] 单元测试完成
- [x] 集成测试完成

---

### 3.3 Week 5-6: LLM Gateway与API实现

#### 任务3.1: LLM Gateway实现 (4天)

**实现内容**:
- 统一LLM接口
- 各大模型适配器
- 模型路由
- 错误处理与重试

**代码位置**: `backend/app/services/llm_gateway.py`

**适配器实现**:
- QwenAdapter
- GLMAdapter
- KimiAdapter
- DoubaoAdapter

**交付物**:
- [x] LLM Gateway框架完成
- [x] 4个国内大模型适配器完成
- [x] 配置文件完成
- [x] 单元测试完成

#### 任务3.2: FastAPI路由实现 (3天)

**API端点**:

```python
# backend/app/api/v1/models.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/models", tags=["models"])

class ModelConfig(BaseModel):
    provider: str
    api_key: str
    model_name: str
    base_url: str = None

@router.post("/")
async def add_model(config: ModelConfig):
    """添加LLM模型配置"""
    pass

@router.get("/")
async def list_models():
    """列出所有已配置的模型"""
    pass

@router.delete("/{model_id}")
async def delete_model(model_id: str):
    """删除模型配置"""
    pass

# backend/app/api/v1/worlds.py
router = APIRouter(prefix="/api/v1/worlds", tags=["worlds"])

@router.post("/")
async def create_world(config: WorldConfig):
    """创建故事世界"""
    pass

@router.get("/{world_id}")
async def get_world(world_id: str):
    """获取世界详情"""
    pass

# backend/app/api/v1/characters.py
router = APIRouter(prefix="/api/v1/characters", tags=["characters"])

@router.post("/")
async def create_character(config: CharacterConfig):
    """创建人物"""
    pass

@router.get("/{character_id}")
async def get_character(character_id: str):
    """获取人物详情"""
    pass

# backend/app/api/v1/simulations.py
router = APIRouter(prefix="/api/v1/simulations", tags=["simulations"])

@router.post("/")
async def create_simulation(config: SimulationConfig):
    """创建模拟"""
    pass

@router.post("/{simulation_id}/start")
async def start_simulation(simulation_id: str):
    """启动模拟"""
    pass

@router.post("/{simulation_id}/pause")
async def pause_simulation(simulation_id: str):
    """暂停模拟"""
    pass

@router.get("/{simulation_id}/events")
async def get_simulation_events(simulation_id: str, limit: int = 50):
    """获取模拟事件流"""
    pass
```

**交付物**:
- [x] 所有API端点实现完成
- [x] 请求验证完成
- [x] 错误处理完成
- [x] API文档生成完成

#### 任务3.3: WebSocket实现 (2天)

**实现内容**:
- 实时事件推送
- 模拟状态更新
- 前后端通信

**代码位置**: `backend/app/api/websocket.py`

**交付物**:
- [x] WebSocket服务端实现完成
- [x] 客户端连接管理完成
- [x] 实时推送测试完成

---

### 3.4 Week 7-8: 前端UI实现

#### 任务4.1: 基础布局与导航 (2天)

**实现内容**:
- 主布局组件
- 侧边栏导航
- 响应式设计

**代码位置**: `frontend/src/components/layout/`

**交付物**:
- [x] MainLayout组件完成
- [x] Header组件完成
- [x] Sidebar组件完成
- [x] 路由配置完成

#### 任务4.2: 设置模块 (2天)

**实现内容**:
- 模型配置界面
- API Key管理
- 模型分配设置

**代码位置**: `frontend/src/components/settings/`

**交付物**:
- [x] ModelConfig组件完成
- [x] ApiKeyManagement组件完成
- [x] 表单验证完成

#### 任务4.3: 世界构建模块 (3天)

**实现内容**:
- 世界参数设置
- 世界预览
- 世界保存/加载

**代码位置**: `frontend/src/components/world/`

**交付物**:
- [x] WorldBuilder组件完成
- [x] WorldPreview组件完成
- [x] 与后端API集成完成

#### 任务4.4: 人物创建模块 (3天)

**实现内容**:
- 人物基本信息设置
- 大五人格编辑器
- 人物列表管理

**代码位置**: `frontend/src/components/character/`

**交付物**:
- [x] CharacterCreator组件完成
- [x] PersonalityEditor组件完成
- [x] CharacterList组件完成

#### 任务4.5: 模拟观察模块 (4天)

**实现内容**:
- 模拟控制面板
- 事件流显示
- 人物状态显示
- WebSocket实时更新

**代码位置**: `frontend/src/components/simulation/`

**交付物**:
- [x] SimulationControl组件完成
- [x] EventStream组件完成
- [x] CharacterStatus组件完成
- [x] WebSocket集成完成

#### 任务4.6: 小说生成模块 (3天)

**实现内容**:
- 视角选择
- 小说预览
- 小说导出

**代码位置**: `frontend/src/components/novel/`

**交付物**:
- [x] PerspectiveSelector组件完成
- [x] NovelPreview组件完成
- [x] NovelExporter组件完成

---

## 四、测试计划

### 4.1 单元测试

**后端单元测试**:
- 测试框架: pytest
- 覆盖率目标: >80%
- 测试内容:
  - 数据模型验证
  - StateStore CRUD操作
  - EventBus事件处理
  - LLM Gateway调用

**前端单元测试**:
- 测试框架: Vitest + React Testing Library
- 覆盖率目标: >70%
- 测试内容:
  - 组件渲染
  - 用户交互
  - 状态管理
  - API调用

### 4.2 集成测试

**后端集成测试**:
- API端点测试
- 数据库集成测试
- WebSocket连接测试

**前端集成测试**:
- 页面流程测试
- API集成测试
- WebSocket实时更新测试

### 4.3 端到端测试

**测试场景**:
1. 完整的用户流程：设置 → 世界构建 → 人物创建 → 模拟 → 小说生成
2. 多用户并发测试
3. 长时间运行稳定性测试

---

## 五、部署计划

### 5.1 开发环境

**本地开发**:
```bash
# 后端
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

### 5.2 Docker部署

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///data/db/push_him_to_you.db
    volumes:
      - ./data:/app/data
      - ./config:/app/config
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 5.3 生产环境

**部署清单**:
- [ ] 服务器配置（推荐：2核4G）
- [ ] 域名配置
- [ ] SSL证书配置
- [ ] Nginx反向代理配置
- [ ] 日志收集配置
- [ ] 监控告警配置

---

## 六、风险管理

### 6.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| LLM API不稳定 | 高 | 中 | 实现重试机制、多模型备份 |
| 数据库性能瓶颈 | 中 | 低 | 优化查询、添加索引、引入缓存 |
| WebSocket连接不稳定 | 中 | 中 | 实现心跳机制、自动重连 |
| 前端性能问题 | 低 | 低 | 代码分割、懒加载、虚拟滚动 |

### 6.2 进度风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 核心框架开发延期 | 高 | 中 | 提前开始、并行开发、简化功能 |
| UI设计变更 | 中 | 中 | 模块化设计、快速迭代 |
| 第三方依赖问题 | 低 | 低 | 锁定版本、准备替代方案 |

---

## 七、验收标准

### 7.1 功能验收

- [ ] 所有核心模块实现完成并通过测试
- [ ] 所有UI界面实现完成并可正常使用
- [ ] API接口完整且文档齐全
- [ ] 数据库设计合理且性能良好
- [ ] LLM Gateway支持至少4个国内大模型

### 7.2 性能验收

- [ ] API响应时间 < 200ms (P95)
- [ ] 页面加载时间 < 2s
- [ ] WebSocket延迟 < 100ms
- [ ] 支持10个并发用户

### 7.3 质量验收

- [ ] 后端单元测试覆盖率 > 80%
- [ ] 前端单元测试覆盖率 > 70%
- [ ] 无严重Bug
- [ ] 代码通过Lint检查

---

## 八、下一步计划

### 8.1 第二阶段：Agent模块开发

- WorldBuilder Agent
- CharacterGenerator Agent
- FateEngine Agent
- Narrator Agent
- 其他专业Agent

### 8.2 第三阶段：功能完善

- 多人物并行模拟
- 关系网络可视化
- 小说导出优化
- 用户反馈收集

---

**文档结束**

**注意事项**:
1. 本计划为初步规划，可根据实际情况调整
2. 每周进行进度回顾和计划调整
3. 遇到重大问题及时沟通和调整
4. 保持代码质量和文档同步更新
