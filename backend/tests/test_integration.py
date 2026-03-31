import pytest
import asyncio
from datetime import datetime
from app.core.state_store import SQLiteStateStore
from app.core.event_bus import EventBus, Event, EventType
from app.core.orchestrator import MasterOrchestrator
from app.models.world import WorldState
from app.models.character import CharacterState
from app.models.event import Event as EventModel

@pytest.mark.asyncio
async def test_full_simulation_workflow():
    """测试完整的模拟工作流程"""
    # 初始化组件
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=False)
    await bus.start()

    orchestrator = MasterOrchestrator(store, bus)

    # 订阅事件以验证事件流
    events_received = []

    async def event_handler(event: Event):
        events_received.append(event)

    bus.subscribe(EventType.SIMULATION_CREATED, event_handler)
    bus.subscribe(EventType.SIMULATION_STARTED, event_handler)
    bus.subscribe(EventType.SIMULATION_STOPPED, event_handler)

    # 创建模拟
    world_config = {
        "era": "现代都市",
        "location": {"province": "浙江", "city": "杭州"},
        "time_span": {"start": 1990, "end": 2025},
        "society_type": "平稳发展型",
        "special_settings": ["包含重大社会事件"]
    }

    character_configs = [
        {
            "name": "李明",
            "gender": "male",
            "birth_date": datetime(1990, 3, 15),
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
            },
            "needs": {
                "physiological": 85,
                "safety": 78
            },
            "skills": {
                "technical": ["编程", "数据分析"]
            },
            "values": {
                "core_values": ["家庭", "自由"]
            }
        }
    ]

    # 执行完整流程
    simulation_id = await orchestrator.create_simulation(world_config, character_configs)
    await asyncio.sleep(0.1)  # 等待事件处理

    # 验证模拟创建
    simulation = await store.get_simulation(simulation_id)
    assert simulation is not None
    assert simulation.status == "idle"

    # 验证世界创建
    world = await store.get_world(simulation.world_id)
    assert world is not None
    assert world.era == "现代都市"

    # 验证人物创建
    characters = await store.list_characters(simulation.world_id)
    assert len(characters) == 1
    assert characters[0].name == "李明"

    # 启动模拟
    await orchestrator.start_simulation(simulation_id)
    await asyncio.sleep(0.1)

    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "running"

    # 停止模拟
    await orchestrator.stop_simulation(simulation_id)
    await asyncio.sleep(0.1)

    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "stopped"

    # 验证事件流
    assert len(events_received) >= 3
    event_types = [e.event_type for e in events_received]
    assert EventType.SIMULATION_CREATED in event_types
    assert EventType.SIMULATION_STARTED in event_types
    assert EventType.SIMULATION_STOPPED in event_types

    await bus.stop()

@pytest.mark.asyncio
async def test_event_persistence():
    """测试事件持久化"""
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=True, log_file="logs/test_events.log")
    await bus.start()

    # 发布多个事件
    for i in range(5):
        event = Event(
            event_type=EventType.EVENTS_GENERATED,
            source="test",
            data={"index": i}
        )
        await bus.publish(event)

    await asyncio.sleep(0.2)  # 等待事件处理

    # 验证事件历史
    history = bus.get_event_history(limit=10)
    assert len(history) == 5

    # 验证事件顺序
    for i, event in enumerate(history):
        assert event.data["index"] == i

    await bus.stop()

@pytest.mark.asyncio
async def test_multiple_characters_simulation():
    """测试多人物模拟"""
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=False)
    await bus.start()

    orchestrator = MasterOrchestrator(store, bus)

    # 创建包含多个人物的模拟
    world_config = {
        "era": "现代都市",
        "location": {"province": "浙江", "city": "杭州"},
        "time_span": {"start": 1990, "end": 2025},
        "society_type": "平稳发展型",
        "special_settings": []
    }

    character_configs = [
        {
            "name": "李明",
            "gender": "male",
            "birth_date": datetime(1990, 3, 15),
            "age": 25.0,
            "personality": {"openness": 75, "conscientiousness": 68, "extraversion": 45, "agreeableness": 82, "neuroticism": 35},
            "current_state": {},
            "needs": {},
            "skills": {},
            "values": {}
        },
        {
            "name": "王芳",
            "gender": "female",
            "birth_date": datetime(1992, 7, 20),
            "age": 23.0,
            "personality": {"openness": 80, "conscientiousness": 75, "extraversion": 60, "agreeableness": 88, "neuroticism": 30},
            "current_state": {},
            "needs": {},
            "skills": {},
            "values": {}
        },
        {
            "name": "张伟",
            "gender": "male",
            "birth_date": datetime(1988, 11, 5),
            "age": 27.0,
            "personality": {"openness": 65, "conscientiousness": 90, "extraversion": 55, "agreeableness": 70, "neuroticism": 40},
            "current_state": {},
            "needs": {},
            "skills": {},
            "values": {}
        }
    ]

    simulation_id = await orchestrator.create_simulation(world_config, character_configs)

    # 验证所有人物都已创建
    simulation = await store.get_simulation(simulation_id)
    characters = await store.list_characters(simulation.world_id)

    assert len(characters) == 3
    names = [c.name for c in characters]
    assert "李明" in names
    assert "王芳" in names
    assert "张伟" in names

    await bus.stop()

@pytest.mark.asyncio
async def test_event_store_integration():
    """测试事件存储集成"""
    store = SQLiteStateStore(":memory:")

    # 创建模拟和人物
    world = WorldState(
        world_id="world-001",
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

    # 创建事件
    from app.models.event import Event as EventModel, EventType as EventTypeEnum

    event = EventModel(
        event_id="event-001",
        simulation_id="sim-001",
        event_type=EventTypeEnum.LIFE_STAGE,
        timestamp=datetime.now(),
        age_at_event=25.0,
        title="大学毕业",
        description="顺利完成大学学业",
        intensity=7,
        participants=["char-001"],
        causes=[],
        effects=[],
        impact={},
        is_spark_moment=False,
        metadata={}
    )

    event_id = await store.create_event(event)
    assert event_id == "event-001"

    # 查询事件
    retrieved = await store.get_event("event-001")
    assert retrieved is not None
    assert retrieved.title == "大学毕业"

    # 列出事件
    events = await store.list_events("sim-001")
    assert len(events) == 1
