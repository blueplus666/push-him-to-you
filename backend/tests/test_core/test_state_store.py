import pytest
from datetime import datetime
from app.core.state_store import SQLiteStateStore
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
        updated_at=datetime.now(),
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
        updated_at=datetime.now(),
    )

    await store.create_world(world)

    # 更新世界
    success = await store.update_world("test-001", {"era": "古代", "society_type": "封建社会"})
    assert success is True

    # 验证更新
    updated = await store.get_world("test-001")
    assert updated.era == "古代"
    assert updated.society_type == "封建社会"
