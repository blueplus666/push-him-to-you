"""测试 Fate Prompts"""
import pytest
from app.prompts.fate_prompts import (
    FateEnginePrompts,
    FATE_ENGINE_SYSTEM_PROMPT,
    FATE_ADVANCE_PROMPT,
    FATE_PREDICTION_PROMPT
)


def test_system_prompt_exists():
    """测试系统提示词存在"""
    assert FATE_ENGINE_SYSTEM_PROMPT is not None
    assert len(FATE_ENGINE_SYSTEM_PROMPT) > 100
    assert "命运编织者" in FATE_ENGINE_SYSTEM_PROMPT
    assert "因果逻辑" in FATE_ENGINE_SYSTEM_PROMPT


def test_advance_prompt_template():
    """测试命运推进提示词模板"""
    assert FATE_ADVANCE_PROMPT is not None
    assert "{fate_state}" in FATE_ADVANCE_PROMPT
    assert "{trigger_event}" in FATE_ADVANCE_PROMPT


def test_prediction_prompt_template():
    """测试命运预测提示词模板"""
    assert FATE_PREDICTION_PROMPT is not None
    assert "{character_state}" in FATE_PREDICTION_PROMPT
    assert "{fate_history}" in FATE_PREDICTION_PROMPT


def test_fate_engine_prompts_class():
    """测试FateEnginePrompts类初始化"""
    prompts = FateEnginePrompts()

    assert prompts.system_prompt == FATE_ENGINE_SYSTEM_PROMPT
    assert prompts.advance_prompt_template == FATE_ADVANCE_PROMPT
    assert prompts.prediction_prompt_template == FATE_PREDICTION_PROMPT


def test_get_system_prompt():
    """测试获取系统提示词"""
    prompts = FateEnginePrompts()
    system_prompt = prompts.get_system_prompt()

    assert system_prompt is not None
    assert system_prompt == FATE_ENGINE_SYSTEM_PROMPT


def test_get_advance_prompt():
    """测试获取命运推进提示词"""
    prompts = FateEnginePrompts()

    fate_state = {
        "character_id": "char_001",
        "current_fate": "事业上升期",
        "fate_nodes": ["节点1", "节点2"],
        "destiny_points": ["转折点1"]
    }
    trigger_event = {
        "type": "职业",
        "description": "获得重要项目机会",
        "impact": "高"
    }
    world_context = {
        "era": "现代都市",
        "location": "杭州",
        "economic_state": "快速发展"
    }
    event_history = "2024-01: 入职新公司\n2024-03: 完成首个项目"
    current_tension = 0.6

    prompt = prompts.get_advance_prompt(
        fate_state=fate_state,
        trigger_event=trigger_event,
        world_context=world_context,
        event_history=event_history,
        current_tension=current_tension
    )

    assert "事业上升期" in prompt
    assert "获得重要项目机会" in prompt
    assert "现代都市" in prompt
    assert "杭州" in prompt
    assert "2024-01" in prompt
    assert "0.6" in prompt


def test_get_prediction_prompt():
    """测试获取命运预测提示词"""
    prompts = FateEnginePrompts()

    character_state = {
        "name": "张三",
        "age": 30,
        "personality": {
            "openness": "高",
            "conscientiousness": "中高"
        },
        "current_status": "事业稳定"
    }
    fate_history = "2020: 毕业\n2022: 升职\n2024: 转型"
    world_context = {
        "era": "现代都市",
        "location": "北京",
        "social_trends": "数字化转型"
    }

    prompt = prompts.get_prediction_prompt(
        character_state=character_state,
        fate_history=fate_history,
        world_context=world_context
    )

    assert "张三" in prompt
    assert "2020" in prompt
    assert "现代都市" in prompt
    assert "北京" in prompt


def test_format_state():
    """测试状态格式化功能"""
    prompts = FateEnginePrompts()

    state = {
        "key1": "value1",
        "key2": "value2",
        "nested": {
            "inner_key": "inner_value"
        }
    }

    formatted = prompts._format_state(state)

    assert "key1" in formatted
    assert "value1" in formatted
    assert "key2" in formatted


def test_format_event():
    """测试事件格式化功能"""
    prompts = FateEnginePrompts()

    event = {
        "type": "职业",
        "description": "获得晋升机会",
        "impact": "高",
        "timestamp": "2024-06"
    }

    formatted = prompts._format_event(event)

    assert "职业" in formatted
    assert "获得晋升机会" in formatted
    assert "高" in formatted


def test_format_context():
    """测试上下文格式化功能"""
    prompts = FateEnginePrompts()

    context = {
        "era": "现代都市",
        "location": "上海",
        "economic_state": "稳定发展",
        "social_trends": "科技创新"
    }

    formatted = prompts._format_context(context)

    assert "现代都市" in formatted
    assert "上海" in formatted
    assert "稳定发展" in formatted
