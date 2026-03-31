import pytest
from datetime import datetime
from app.core.orchestrator import MasterOrchestrator
from app.core.state_store import SQLiteStateStore
from app.core.event_bus import EventBus
from app.models.world import WorldState
from app.models.character import CharacterState
from app.models.simulation import SimulationContext

@pytest.mark.asyncio
async def test_orchestrator_create_simulation():
    """测试创建模拟"""
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=False)
    orchestrator = MasterOrchestrator(store, bus)

    world_config = {
        "era": "现代都市",
        "location": {"province": "浙江", "city": "杭州"},
        "time_span": {"start": 1990, "end": 2025},
        "society_type": "平稳发展型",
        "special_settings": []
    }

    character_configs = [{
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
        "current_state": {},
        "needs": {},
        "skills": {},
        "values": {}
    }]

    simulation_id = await orchestrator.create_simulation(world_config, character_configs)

    assert simulation_id is not None

    # 验证世界已创建
    simulation = await store.get_simulation(simulation_id)
    assert simulation is not None
    assert simulation.status == "idle"

@pytest.mark.asyncio
async def test_orchestrator_start_stop_simulation():
    """测试启动和停止模拟"""
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=False)
    orchestrator = MasterOrchestrator(store, bus)

    # 创建模拟
    world_config = {
        "era": "现代都市",
        "location": {"province": "浙江", "city": "杭州"},
        "time_span": {"start": 1990, "end": 2025},
        "society_type": "平稳发展型",
        "special_settings": []
    }

    character_configs = [{
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
        "current_state": {},
        "needs": {},
        "skills": {},
        "values": {}
    }]

    simulation_id = await orchestrator.create_simulation(world_config, character_configs)

    # 启动模拟
    await orchestrator.start_simulation(simulation_id)
    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "running"

    # 停止模拟
    await orchestrator.stop_simulation(simulation_id)
    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "stopped"

@pytest.mark.asyncio
async def test_orchestrator_pause_resume_simulation():
    """测试暂停和恢复模拟"""
    store = SQLiteStateStore(":memory:")
    bus = EventBus(persist_events=False)
    orchestrator = MasterOrchestrator(store, bus)

    # 创建并启动模拟
    world_config = {
        "era": "现代都市",
        "location": {"province": "浙江", "city": "杭州"},
        "time_span": {"start": 1990, "end": 2025},
        "society_type": "平稳发展型",
        "special_settings": []
    }

    character_configs = [{
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
        "current_state": {},
        "needs": {},
        "skills": {},
        "values": {}
    }]

    simulation_id = await orchestrator.create_simulation(world_config, character_configs)
    await orchestrator.start_simulation(simulation_id)

    # 暂停模拟
    await orchestrator.pause_simulation(simulation_id)
    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "paused"

    # 恢复模拟
    await orchestrator.resume_simulation(simulation_id)
    simulation = await store.get_simulation(simulation_id)
    assert simulation.status == "running"

    # 清理
    await orchestrator.stop_simulation(simulation_id)
