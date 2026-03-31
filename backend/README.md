# "把他推向你" - 核心框架

AI驱动的命运模拟与小说生成系统的核心框架实现。

## 功能特性

- **状态管理** - 基于SQLite的持久化状态存储
- **事件驱动** - 异步事件总线，支持发布/订阅模式
- **模拟协调** - 完整的模拟生命周期管理
- **类型安全** - 使用Pydantic进行数据验证

## 技术栈

- Python 3.10+
- FastAPI - Web框架
- SQLite - 数据库
- Pydantic - 数据验证
- asyncio - 异步IO

## 快速开始

### 安装依赖

```bash
cd backend
poetry install
```

### 运行测试

```bash
poetry run pytest
```

### 运行测试并生成覆盖率报告

```bash
poetry run pytest --cov=app --cov-report=term-missing
```

## 项目结构

```
backend/
├── app/
│   ├── core/           # 核心模块
│   │   ├── state_store.py    # 状态存储
│   │   ├── event_bus.py      # 事件总线
│   │   ├── orchestrator.py   # 协调器
│   │   └── exceptions.py     # 异常定义
│   └── models/         # 数据模型
│       ├── world.py          # 世界状态
│       ├── character.py      # 人物状态
│       ├── event.py          # 事件模型
│       └── simulation.py     # 模拟上下文
├── tests/              # 测试文件
│   ├── test_core/            # 核心模块测试
│   ├── test_models/          # 数据模型测试
│   └── test_integration.py   # 集成测试
└── data/               # 数据目录
    └── db/                   # 数据库文件
```

## 核心组件

### StateStore

状态存储接口，提供数据的CRUD操作。

```python
from app.core.state_store import SQLiteStateStore
from app.models.world import WorldState

store = SQLiteStateStore("data/db/app.db")

# 创建世界
world = WorldState(...)
world_id = await store.create_world(world)

# 获取世界
world = await store.get_world(world_id)
```

### EventBus

事件总线，实现发布/订阅模式。

```python
from app.core.event_bus import EventBus, Event, EventType

bus = EventBus()
await bus.start()

# 订阅事件
async def handler(event: Event):
    print(f"Received: {event.event_type}")

bus.subscribe(EventType.SIMULATION_STARTED, handler)

# 发布事件
event = Event(
    event_type=EventType.SIMULATION_STARTED,
    source="test",
    data={"simulation_id": "test-001"}
)
await bus.publish(event)
```

### MasterOrchestrator

主协调器，管理模拟生命周期。

```python
from app.core.orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator(store, bus)

# 创建模拟
simulation_id = await orchestrator.create_simulation(
    world_config={...},
    character_configs=[...]
)

# 启动模拟
await orchestrator.start_simulation(simulation_id)

# 暂停模拟
await orchestrator.pause_simulation(simulation_id)

# 停止模拟
await orchestrator.stop_simulation(simulation_id)
```

## 测试

项目采用TDD（测试驱动开发）方法，所有核心功能都有完整的测试覆盖。

- 单元测试覆盖率: > 80%
- 集成测试: 验证模块间协作
- 端到端测试: 验证完整工作流

## 文档

- [核心框架设计文档](../docs/specs/2026-04-01-core-framework-design.md)
- [国内大模型接入文档](../docs/llm-providers/国内大模型接入文档.md)
- [第一阶段开发计划](../docs/development/phase1-development-plan.md)

## 许可证

MIT License
