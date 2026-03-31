# "把他推向你" - 核心框架深化设计文档

**文档版本**: v1.0  
**创建日期**: 2026-04-01  
**作者**: AI设计团队  
**状态**: 设计评审中

---

## 目录

1. [项目概述](#一项目概述)
2. [核心架构设计](#二核心架构设计)
3. [核心模块设计](#三核心模块设计)
4. [数据模型设计](#四数据模型设计)
5. [LLM集成设计](#五llm集成设计)
6. [API接口设计](#六api接口设计)
7. [第一阶段开发计划](#七第一阶段开发计划)
8. [附录：国内大模型接入文档](#八附录国内大模型接入文档)

---

## 一、项目概述

### 1.1 项目背景

"把他推向你"是一个创新性的AI驱动命运模拟与小说生成系统。基于第一性原理分析，本项目的核心价值链为：

```
设定 → 模拟 → 记录 → 叙事
```

### 1.2 开发策略

采用**增量开发**策略：
- **第一阶段**：设计并实现核心框架（状态管理、事件引擎、Agent协调器）和完整UI/UX
- **第二阶段**：开发各个专业Agent模块（世界构建、人物塑造、命运引擎等）
- **第三阶段**：集成所有模块，完成端到端功能

### 1.3 技术选型

基于需求分析和可行性评估，技术栈选择如下：

| 层级 | 技术选型 | 选择理由 |
|------|---------|---------|
| **前端框架** | React 18 + TypeScript | 现代化、类型安全、生态丰富 |
| **UI组件库** | shadcn/ui | 设计精美、高度可定制、开发效率高 |
| **状态管理** | Zustand | 轻量级、TypeScript友好、易于调试 |
| **后端框架** | FastAPI (Python) | 高性能、异步支持、自动API文档 |
| **任务队列** | Celery + Redis | 成熟稳定、支持异步任务 |
| **数据存储** | SQLite + Chroma | 轻量级、无需额外服务、适合MVP |
| **向量数据库** | Chroma | 开源、易用、支持本地部署 |
| **LLM Gateway** | 自研统一网关 | 支持多模型、灵活配置 |

### 1.4 核心设计原则

1. **插件化架构**：每个模块都是独立的插件，通过事件总线通信
2. **事件驱动**：模块间通过事件异步通信，降低耦合度
3. **共享状态层**：所有模块共享统一的状态存储，避免状态传递开销
4. **配置化**：LLM模型分配、Agent行为均可通过配置文件调整
5. **渐进式开发**：核心框架先行，后续模块逐步集成

---

## 二、核心架构设计

### 2.1 整体架构图

基于批判性分析和第一性原理，采用**事件驱动 + 共享状态层**的混合架构：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           应用层 (Application Layer)                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        API Gateway (FastAPI)                       │  │
│  │  - RESTful API 暴露                                                │  │
│  │  - WebSocket 实时通信                                              │  │
│  │  - 认证授权                                                        │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      前端应用 (React + shadcn/ui)                  │  │
│  │  - 参数设置界面                                                    │  │
│  │  - 世界构建界面                                                    │  │
│  │  - 人生模拟观察界面                                                │  │
│  │  - 小说生成界面                                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          协调层 (Orchestration Layer)                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      Master Orchestrator                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │ 任务调度器  │  │ 状态管理器  │  │ 冲突解决器  │               │  │
│  │  │TaskScheduler│  │StateManager │  │ConflictRes. │               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        Event Bus (事件总线)                         │  │
│  │  - 事件发布/订阅                                                   │  │
│  │  - 事件路由                                                        │  │
│  │  - 事件持久化                                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Agent层 (Agent Layer)                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     Agent Plugin System                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
│  │  │ World    │  │Character │  │  Fate    │  │Narrator  │         │  │
│  │  │ Builder  │  │ Generator│  │ Engine   │  │          │         │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
│  │  │Emotional │  │  Event   │  │Relation  │  │  Spark   │         │  │
│  │  │ Renderer │  │ Generator│  │ Network  │  │ Capture  │         │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │  │
│  │                                                                    │  │
│  │  所有Agent通过事件总线通信，订阅相关事件并发布处理结果             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          核心层 (Core Layer)                             │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        State Store (状态存储)                       │  │
│  │  - World State (世界状态)                                          │  │
│  │  - Character States (人物状态)                                     │  │
│  │  - Event History (事件历史)                                        │  │
│  │  - Simulation Context (模拟上下文)                                 │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        LLM Gateway (模型网关)                       │  │
│  │  - 统一的LLM调用接口                                               │  │
│  │  - 模型路由与负载均衡                                              │  │
│  │  - 成本优化与限流                                                  │  │
│  │  - 支持多模型提供商                                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          数据层 (Data Layer)                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │   SQLite   │  │   Chroma   │  │    Redis   │  │ 文件存储    │       │
│  │ (关系数据) │  │ (向量数据) │  │  (缓存)    │  │ (小说导出) │       │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 架构设计说明

#### 2.2.1 为什么选择事件驱动 + 共享状态层？

**传统API方式的问题**：
```
FateEngine → HTTP调用 → CharacterGenerator → HTTP调用 → Narrator
问题：多次网络调用、状态传递开销大、难以并行处理
```

**事件驱动 + 共享状态的优势**：
```
1. FateEngine从StateStore读取character_state（内存访问，极快）
2. FateEngine生成事件，发布EventGenerated事件
3. 多个Agent并行订阅处理：
   - CharacterGenerator计算人物反应
   - RelationNetwork更新关系
   - SparkCapture评估闪光时刻
4. 所有Agent将结果写入StateStore

优势：
- 状态访问是内存操作，性能高
- 多个Agent可以并行处理
- 事件总线保证消息可靠传递
- 易于监控和调试
```

#### 2.2.2 分层职责

| 层级 | 职责 | 关键组件 |
|------|------|---------|
| **应用层** | 对外接口、用户交互 | API Gateway、前端UI |
| **协调层** | 任务调度、状态管理、事件路由 | Orchestrator、Event Bus |
| **Agent层** | 专业领域处理 | 各专业Agent插件 |
| **核心层** | 共享基础设施 | State Store、LLM Gateway |
| **数据层** | 数据持久化 | SQLite、Chroma、Redis |

### 2.3 数据流设计

#### 2.3.1 核心数据流

```
用户操作 → API Gateway → Orchestrator → Event Bus → Agent处理 → State Store更新 → 事件通知 → UI更新
```

#### 2.3.2 典型场景数据流

**场景：生成一个人生事件**

```python
# 1. 用户启动模拟
用户点击"开始模拟" → API Gateway接收请求

# 2. Orchestrator调度
Orchestrator创建SimulationTask → 发布SimulationStarted事件

# 3. FateEngine处理
FateEngine订阅SimulationStarted事件
  → 从StateStore读取world_state和character_state
  → 生成候选事件列表
  → 发布EventsGenerated事件

# 4. 多个Agent并行处理
CharacterGenerator订阅EventsGenerated事件
  → 计算人物反应
  → 发布CharacterReactionComputed事件

RelationNetwork订阅EventsGenerated事件
  → 更新关系网络
  → 发布RelationshipUpdated事件

SparkCapture订阅EventsGenerated事件
  → 评估闪光时刻
  → 发布SparkDetected事件（如果是闪光时刻）

# 5. Narrator生成叙事
Narrator订阅所有相关事件
  → 从StateStore读取完整上下文
  → 生成叙事文本
  → 发布NarrativeGenerated事件

# 6. StateStore更新
所有Agent将结果写入StateStore
StateStore发布StateChanged事件

# 7. UI实时更新
前端通过WebSocket订阅StateChanged事件
  → 实时更新界面显示
```

### 2.4 插件化架构设计

#### 2.4.1 Agent插件规范

每个Agent必须实现以下接口：

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Agent配置基类"""
    agent_id: str
    agent_name: str
    enabled: bool = True
    llm_model: str  # 分配的LLM模型
    llm_config: Dict[str, Any] = {}  # LLM配置参数

class AgentOutput(BaseModel):
    """Agent输出基类"""
    agent_id: str
    timestamp: datetime
    event_type: str  # 发布的事件类型
    data: Dict[str, Any]  # 核心数据
    metadata: Dict[str, Any] = {}  # Agent特定扩展

class BaseAgent(ABC):
    """Agent基类"""
    
    def __init__(self, config: AgentConfig, event_bus, state_store, llm_gateway):
        self.config = config
        self.event_bus = event_bus
        self.state_store = state_store
        self.llm_gateway = llm_gateway
    
    @abstractmethod
    def get_subscribed_events(self) -> List[str]:
        """返回该Agent订阅的事件类型列表"""
        pass
    
    @abstractmethod
    async def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> AgentOutput:
        """处理事件并返回结果"""
        pass
    
    async def start(self):
        """启动Agent，订阅事件"""
        for event_type in self.get_subscribed_events():
            self.event_bus.subscribe(event_type, self.handle_event)
    
    async def stop(self):
        """停止Agent，取消订阅"""
        for event_type in self.get_subscribed_events():
            self.event_bus.unsubscribe(event_type, self.handle_event)
```

#### 2.4.2 Agent注册机制

```python
# Agent注册表
class AgentRegistry:
    """Agent注册表，管理所有Agent插件"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
    
    def register(self, agent_class: type, config: AgentConfig):
        """注册Agent"""
        agent = agent_class(
            config=config,
            event_bus=self.event_bus,
            state_store=self.state_store,
            llm_gateway=self.llm_gateway
        )
        self.agents[config.agent_id] = agent
        return agent
    
    def get_agent(self, agent_id: str) -> BaseAgent:
        """获取Agent实例"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[str]:
        """列出所有已注册的Agent"""
        return list(self.agents.keys())
    
    async def start_all(self):
        """启动所有Agent"""
        for agent in self.agents.values():
            await agent.start()
    
    async def stop_all(self):
        """停止所有Agent"""
        for agent in self.agents.values():
            await agent.stop()
```

---

## 三、核心模块设计

### 3.1 状态管理模块 (State Store)

状态管理模块是整个系统的核心，负责维护所有状态数据的单一真相源。

#### 3.1.1 状态数据模型

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class WorldState(BaseModel):
    """世界状态"""
    world_id: str
    era: str  # 时代背景
    location: Dict[str, str]  # 地理位置
    time_span: Dict[str, int]  # 时间跨度
    society_type: str  # 社会类型
    special_settings: List[str]  # 特殊设定
    
    # 动态状态
    current_time: datetime  # 当前时间
    environment_state: Dict[str, Any]  # 环境状态
    social_events: List[Dict[str, Any]]  # 社会事件列表
    
    # 元数据
    created_at: datetime
    updated_at: datetime

class CharacterState(BaseModel):
    """人物状态"""
    character_id: str
    name: str
    gender: str
    birth_date: datetime
    age: float
    
    # 人格特质（大五人格）
    personality: Dict[str, int] = Field(
        description="大五人格维度：openness, conscientiousness, extraversion, agreeableness, neuroticism"
    )
    
    # 当前状态
    current_state: Dict[str, Any] = Field(
        description="当前状态：occupation, income_level, relationship_status, health_status, mental_state, life_satisfaction"
    )
    
    # 需求层次
    needs: Dict[str, int] = Field(
        description="马斯洛需求层次：physiological, safety, belonging, esteem, self_actualization"
    )
    
    # 技能
    skills: Dict[str, List[str]] = Field(
        description="技能分类：technical, social, creative, physical"
    )
    
    # 价值观
    values: Dict[str, Any] = Field(
        description="价值观：core_values, life_goal, fear"
    )
    
    # 关系网络ID
    relationship_graph_id: str
    
    # 事件时间线ID
    event_timeline_id: str
    
    # 元数据
    created_at: datetime
    updated_at: datetime

class Event(BaseModel):
    """事件模型"""
    event_id: str
    event_type: str  # 事件类型
    timestamp: datetime
    age_at_event: float
    
    # 事件内容
    title: str
    description: str
    intensity: int = Field(ge=1, le=10, description="事件强度1-10")
    
    # 参与者
    participants: List[str]  # 参与的人物ID列表
    
    # 因果关系
    causes: List[str] = Field(default_factory=list, description="导致此事件的事件ID列表")
    effects: List[str] = Field(default_factory=list, description="此事件导致的事件ID列表")
    
    # 影响评估
    impact: Dict[str, Any] = Field(
        description="事件影响：personality_changes, relationship_changes, state_changes"
    )
    
    # 闪光时刻标记
    is_spark_moment: bool = False
    spark_score: Optional[float] = None
    
    # 元数据
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SimulationContext(BaseModel):
    """模拟上下文"""
    simulation_id: str
    world_id: str
    character_ids: List[str]
    
    # 模拟状态
    status: str  # running, paused, stopped, completed
    current_time: datetime
    current_age: float
    
    # 统计信息
    total_events: int = 0
    spark_moments_count: int = 0
    
    # 配置
    speed: float = 1.0
    
    # 元数据
    created_at: datetime
    updated_at: datetime
```

#### 3.1.2 状态存储接口

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class StateStore(ABC):
    """状态存储抽象接口"""
    
    # ========== World State ==========
    @abstractmethod
    async def create_world(self, world_state: WorldState) -> str:
        """创建世界状态"""
        pass
    
    @abstractmethod
    async def get_world(self, world_id: str) -> Optional[WorldState]:
        """获取世界状态"""
        pass
    
    @abstractmethod
    async def update_world(self, world_id: str, updates: Dict[str, Any]) -> bool:
        """更新世界状态"""
        pass
    
    # ========== Character State ==========
    @abstractmethod
    async def create_character(self, character_state: CharacterState) -> str:
        """创建人物状态"""
        pass
    
    @abstractmethod
    async def get_character(self, character_id: str) -> Optional[CharacterState]:
        """获取人物状态"""
        pass
    
    @abstractmethod
    async def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """更新人物状态"""
        pass
    
    @abstractmethod
    async def list_characters(self, world_id: str) -> List[CharacterState]:
        """列出世界中的所有人物"""
        pass
    
    # ========== Event ==========
    @abstractmethod
    async def create_event(self, event: Event) -> str:
        """创建事件"""
        pass
    
    @abstractmethod
    async def get_event(self, event_id: str) -> Optional[Event]:
        """获取事件"""
        pass
    
    @abstractmethod
    async def list_events(
        self, 
        character_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """列出事件（支持多种过滤条件）"""
        pass
    
    # ========== Simulation Context ==========
    @abstractmethod
    async def create_simulation(self, simulation_context: SimulationContext) -> str:
        """创建模拟上下文"""
        pass
    
    @abstractmethod
    async def get_simulation(self, simulation_id: str) -> Optional[SimulationContext]:
        """获取模拟上下文"""
        pass
    
    @abstractmethod
    async def update_simulation(self, simulation_id: str, updates: Dict[str, Any]) -> bool:
        """更新模拟上下文"""
        pass
```

#### 3.1.3 SQLite实现

```python
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio
from pathlib import Path

class SQLiteStateStore(StateStore):
    """基于SQLite的状态存储实现"""
    
    def __init__(self, db_path: str = "data/push_him_to_you.db"):
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
                    json.dumps(world_state.location),
                    json.dumps(world_state.time_span),
                    world_state.society_type,
                    json.dumps(world_state.special_settings),
                    world_state.current_time.isoformat(),
                    json.dumps(world_state.environment_state),
                    json.dumps(world_state.social_events),
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
    
    # 其他方法实现类似...
    # 为节省篇幅，这里省略其他方法的完整实现
    # 实际开发时会完整实现所有接口方法
```

### 3.2 事件引擎模块 (Event Engine)

事件引擎是系统的"心脏"，负责驱动整个模拟流程的运转。

#### 3.2.1 事件类型定义

```python
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EventType(str, Enum):
    """系统事件类型枚举"""
    
    # 系统级事件
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    
    # 模拟生命周期事件
    SIMULATION_CREATED = "simulation.created"
    SIMULATION_STARTED = "simulation.started"
    SIMULATION_PAUSED = "simulation.paused"
    SIMULATION_RESUMED = "simulation.resumed"
    SIMULATION_STOPPED = "simulation.stopped"
    SIMULATION_COMPLETED = "simulation.completed"
    
    # 世界事件
    WORLD_CREATED = "world.created"
    WORLD_UPDATED = "world.updated"
    ENVIRONMENT_CHANGED = "environment.changed"
    SOCIAL_EVENT_OCCURRED = "social_event.occurred"
    
    # 人物事件
    CHARACTER_CREATED = "character.created"
    CHARACTER_UPDATED = "character.updated"
    CHARACTER_REACTION_COMPUTED = "character.reaction_computed"
    
    # 命运引擎事件
    EVENTS_GENERATED = "fate.events_generated"
    EVENT_SELECTED = "fate.event_selected"
    CAUSAL_CHAIN_UPDATED = "fate.causal_chain_updated"
    
    # 关系事件
    RELATIONSHIP_ESTABLISHED = "relationship.established"
    RELATIONSHIP_UPDATED = "relationship.updated"
    RELATIONSHIP_ENDED = "relationship.ended"
    
    # 闪光时刻事件
    SPARK_DETECTED = "spark.detected"
    SPARK_RECORDED = "spark.recorded"
    
    # 叙事事件
    NARRATIVE_GENERATED = "narrative.generated"
    NARRATIVE_EXPORTED = "narrative.exported"
    
    # 状态变更事件
    STATE_CHANGED = "state.changed"
    ERROR_OCCURRED = "error.occurred"

class Event(BaseModel):
    """事件基类"""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str  # 事件来源（Agent ID或系统组件）
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

class EventSubscription(BaseModel):
    """事件订阅配置"""
    subscriber_id: str
    event_types: List[EventType]
    callback_path: str  # 回调函数路径
    priority: int = 0  # 优先级，数字越大越先执行
    enabled: bool = True
```

#### 3.2.2 事件总线实现

```python
import asyncio
from typing import Dict, List, Callable, Any
from collections import defaultdict
import logging
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class EventBus:
    """事件总线 - 实现发布/订阅模式"""
    
    def __init__(self, persist_events: bool = True, log_file: str = "logs/events.log"):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: List[Event] = []
        self.persist_events = persist_events
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 事件队列（用于异步处理）
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
    
    async def start(self):
        """启动事件总线"""
        self._running = True
        asyncio.create_task(self._process_events())
        logger.info("Event Bus started")
    
    async def stop(self):
        """停止事件总线"""
        self._running = False
        logger.info("Event Bus stopped")
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event: {event_type}")
    
    async def publish(self, event: Event):
        """发布事件（异步）"""
        await self.event_queue.put(event)
    
    async def _process_events(self):
        """处理事件队列"""
        while self._running:
            try:
                event = await asyncio.wait_for(
                    self.event_queue.get(),
                    timeout=1.0
                )
                await self._dispatch_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}", exc_info=True)
    
    async def _dispatch_event(self, event: Event):
        """分发事件到订阅者"""
        logger.debug(f"Dispatching event: {event.event_type}")
        
        # 记录事件历史
        self.event_history.append(event)
        if self.persist_events:
            self._persist_event(event)
        
        # 获取订阅者
        callbacks = self.subscribers.get(event.event_type, [])
        
        # 并行调用所有订阅者
        tasks = []
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(event))
                else:
                    # 如果是同步函数，在线程池中执行
                    tasks.append(asyncio.get_event_loop().run_in_executor(
                        None, callback, event
                    ))
            except Exception as e:
                logger.error(f"Error creating task for callback: {e}", exc_info=True)
        
        # 等待所有订阅者处理完成
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def _persist_event(self, event: Event):
        """持久化事件到日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event.dict(), default=str) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")
    
    def get_event_history(
        self, 
        event_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Event]:
        """获取事件历史"""
        events = self.event_history
        
        # 过滤
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        
        # 限制数量
        return events[-limit:]
```

#### 3.2.3 事件溯源机制

```python
class EventSourcing:
    """事件溯源 - 通过重放事件重建状态"""
    
    def __init__(self, event_bus: EventBus, state_store: StateStore):
        self.event_bus = event_bus
        self.state_store = state_store
    
    async def replay_events(
        self, 
        simulation_id: str,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None
    ):
        """重放事件以重建状态"""
        # 从事件历史中获取事件
        events = self.event_bus.get_event_history(
            start_time=from_time,
            end_time=to_time
        )
        
        # 按时间排序
        events.sort(key=lambda e: e.timestamp)
        
        # 重放事件
        for event in events:
            await self._apply_event(event)
    
    async def _apply_event(self, event: Event):
        """应用事件到状态"""
        # 根据事件类型更新状态
        if event.event_type == EventType.WORLD_CREATED:
            await self.state_store.create_world(event.data['world_state'])
        
        elif event.event_type == EventType.CHARACTER_CREATED:
            await self.state_store.create_character(event.data['character_state'])
        
        elif event.event_type == EventType.CHARACTER_UPDATED:
            await self.state_store.update_character(
                event.data['character_id'],
                event.data['updates']
            )
        
        # ... 其他事件类型处理
```

### 3.3 Agent协调器 (Master Orchestrator)

Agent协调器是系统的"大脑"，负责调度所有Agent的执行。

#### 3.3.1 协调器架构

```python
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class SimulationStatus(str, Enum):
    """模拟状态"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ERROR = "error"

class MasterOrchestrator:
    """主协调器 - 管理整个模拟流程"""
    
    def __init__(
        self,
        event_bus: EventBus,
        state_store: StateStore,
        agent_registry: AgentRegistry,
        llm_gateway: 'LLMGateway'
    ):
        self.event_bus = event_bus
        self.state_store = state_store
        self.agent_registry = agent_registry
        self.llm_gateway = llm_gateway
        
        # 模拟状态
        self.current_simulation_id: Optional[str] = None
        self.simulation_status: SimulationStatus = SimulationStatus.IDLE
        
        # 任务队列
        self.task_queue: asyncio.Queue = asyncio.Queue()
        
        # 性能监控
        self.metrics = {
            'events_processed': 0,
            'agents_invoked': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    async def start(self):
        """启动协调器"""
        # 启动事件总线
        await self.event_bus.start()
        
        # 启动所有Agent
        await self.agent_registry.start_all()
        
        # 订阅关键事件
        self.event_bus.subscribe(EventType.ERROR_OCCURRED, self._handle_error)
        self.event_bus.subscribe(EventType.SIMULATION_COMPLETED, self._handle_simulation_complete)
        
        logger.info("Master Orchestrator started")
    
    async def stop(self):
        """停止协调器"""
        # 停止所有Agent
        await self.agent_registry.stop_all()
        
        # 停止事件总线
        await self.event_bus.stop()
        
        logger.info("Master Orchestrator stopped")
    
    async def create_simulation(
        self,
        world_config: Dict[str, Any],
        character_configs: List[Dict[str, Any]]
    ) -> str:
        """创建新的模拟"""
        from datetime import datetime
        import uuid
        
        simulation_id = str(uuid.uuid4())
        
        # 创建世界状态
        world_state = WorldState(
            world_id=str(uuid.uuid4()),
            **world_config,
            current_time=datetime.now(),
            environment_state={},
            social_events=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await self.state_store.create_world(world_state)
        
        # 创建人物状态
        character_ids = []
        for char_config in character_configs:
            character_state = CharacterState(
                character_id=str(uuid.uuid4()),
                **char_config,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            await self.state_store.create_character(character_state)
            character_ids.append(character_state.character_id)
        
        # 创建模拟上下文
        simulation_context = SimulationContext(
            simulation_id=simulation_id,
            world_id=world_state.world_id,
            character_ids=character_ids,
            status=SimulationStatus.IDLE.value,
            current_time=datetime.now(),
            current_age=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await self.state_store.create_simulation(simulation_context)
        
        # 发布事件
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_CREATED,
            source="orchestrator",
            data={
                "simulation_id": simulation_id,
                "world_id": world_state.world_id,
                "character_ids": character_ids
            }
        ))
        
        logger.info(f"Simulation created: {simulation_id}")
        return simulation_id
    
    async def start_simulation(self, simulation_id: str):
        """启动模拟"""
        # 获取模拟上下文
        simulation = await self.state_store.get_simulation(simulation_id)
        if not simulation:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        # 更新状态
        self.current_simulation_id = simulation_id
        self.simulation_status = SimulationStatus.RUNNING
        self.metrics['start_time'] = datetime.now()
        
        # 更新数据库
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.RUNNING.value}
        )
        
        # 发布启动事件
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_STARTED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))
        
        # 启动模拟循环
        asyncio.create_task(self._simulation_loop(simulation_id))
        
        logger.info(f"Simulation started: {simulation_id}")
    
    async def pause_simulation(self, simulation_id: str):
        """暂停模拟"""
        self.simulation_status = SimulationStatus.PAUSED
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.PAUSED.value}
        )
        
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_PAUSED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))
        
        logger.info(f"Simulation paused: {simulation_id}")
    
    async def resume_simulation(self, simulation_id: str):
        """恢复模拟"""
        self.simulation_status = SimulationStatus.RUNNING
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.RUNNING.value}
        )
        
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_RESUMED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))
        
        logger.info(f"Simulation resumed: {simulation_id}")
    
    async def stop_simulation(self, simulation_id: str):
        """停止模拟"""
        self.simulation_status = SimulationStatus.STOPPED
        self.metrics['end_time'] = datetime.now()
        
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.STOPPED.value}
        )
        
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_STOPPED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))
        
        logger.info(f"Simulation stopped: {simulation_id}")
    
    async def _simulation_loop(self, simulation_id: str):
        """模拟主循环"""
        try:
            while self.simulation_status == SimulationStatus.RUNNING:
                # 获取模拟上下文
                simulation = await self.state_store.get_simulation(simulation_id)
                
                # 检查是否完成
                if self._check_completion(simulation):
                    await self._complete_simulation(simulation_id)
                    break
                
                # 触发事件生成
                await self.event_bus.publish(Event(
                    event_type=EventType.EVENTS_GENERATED,
                    source="orchestrator",
                    data={"simulation_id": simulation_id}
                ))
                
                # 等待一段时间（根据模拟速度）
                await asyncio.sleep(1.0 / simulation.speed)
                
                # 更新指标
                self.metrics['events_processed'] += 1
        
        except Exception as e:
            logger.error(f"Simulation loop error: {e}", exc_info=True)
            self.simulation_status = SimulationStatus.ERROR
            await self.event_bus.publish(Event(
                event_type=EventType.ERROR_OCCURRED,
                source="orchestrator",
                data={
                    "simulation_id": simulation_id,
                    "error": str(e)
                }
            ))
    
    def _check_completion(self, simulation: SimulationContext) -> bool:
        """检查模拟是否完成"""
        # 检查年龄是否超过阈值
        if simulation.current_age >= 80:  # 假设80岁为终点
            return True
        
        # 检查状态
        if simulation.status == SimulationStatus.COMPLETED.value:
            return True
        
        return False
    
    async def _complete_simulation(self, simulation_id: str):
        """完成模拟"""
        self.simulation_status = SimulationStatus.COMPLETED
        self.metrics['end_time'] = datetime.now()
        
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.COMPLETED.value}
        )
        
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_COMPLETED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))
        
        logger.info(f"Simulation completed: {simulation_id}")
    
    async def _handle_error(self, event: Event):
        """处理错误事件"""
        logger.error(f"Error occurred: {event.data}")
        self.metrics['errors'] += 1
    
    async def _handle_simulation_complete(self, event: Event):
        """处理模拟完成事件"""
        simulation_id = event.data['simulation_id']
        logger.info(f"Simulation {simulation_id} completed successfully")
        
        # 输出性能指标
        duration = (self.metrics['end_time'] - self.metrics['start_time']).total_seconds()
        logger.info(f"Simulation duration: {duration}s")
        logger.info(f"Events processed: {self.metrics['events_processed']}")
        logger.info(f"Agents invoked: {self.metrics['agents_invoked']}")
        logger.info(f"Errors: {self.metrics['errors']}")
```

---

## 四、LLM集成设计

### 4.1 LLM Gateway架构

LLM Gateway是系统的"语言中枢"，负责统一管理所有大模型API的调用。

```
┌─────────────────────────────────────────────────────────────────┐
│                        LLM Gateway                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   统一调用接口 (Unified API)              │  │
│  │  - generate(prompt, model, **kwargs)                     │  │
│  │  - stream_generate(prompt, model, **kwargs)              │  │
│  │  - embed(text, model)                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   模型路由器 (Model Router)               │  │
│  │  - 根据任务类型选择最优模型                               │  │
│  │  - 负载均衡                                               │  │
│  │  - 成本优化                                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   提供商适配器 (Provider Adapters)        │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│  │  │ Qwen    │  │  GLM    │  │ Kimi    │  │Doubao   │    │  │
│  │  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │    │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   监控与限流 (Monitor & Rate Limiter)     │  │
│  │  - 调用统计                                               │  │
│  │  - 成本追踪                                               │  │
│  │  - 速率限制                                               │  │
│  │  - 错误重试                                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 统一LLM接口

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncGenerator
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

class LLMConfig(BaseModel):
    """LLM配置基类"""
    provider: str  # 提供商名称
    model: str  # 模型名称
    api_key: str  # API密钥
    base_url: Optional[str] = None  # API地址
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    
    # 重试配置
    max_retries: int = Field(default=3, ge=0)
    retry_delay: float = Field(default=1.0, ge=0.0)
    
    # 超时配置
    timeout: float = Field(default=30.0, ge=1.0)

class LLMResponse(BaseModel):
    """LLM响应基类"""
    content: str  # 生成的内容
    model: str  # 使用的模型
    provider: str  # 提供商
    
    # 使用统计
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    # 元数据
    finish_reason: str
    created_at: datetime = Field(default_factory=datetime.now)
    latency: float  # 响应时间（秒）
    
    # 额外信息
    metadata: Dict[str, Any] = Field(default_factory=dict)

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
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """生成文本嵌入向量"""
        pass
    
    async def _retry_with_backoff(self, func, *args, **kwargs):
        """带退避的重试机制"""
        import time
        
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

---

**文档未完待续，下一部分将包含：**
- 4.3 国内大模型适配器实现
- 五、API接口设计
- 六、第一阶段开发计划
- 七、附录：国内大模型接入文档

**请确认当前设计是否符合您的预期？**
