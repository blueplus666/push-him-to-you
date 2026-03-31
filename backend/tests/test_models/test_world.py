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
