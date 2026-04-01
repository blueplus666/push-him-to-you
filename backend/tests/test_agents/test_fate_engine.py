"""
Fate Engine Agent 测试
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, date

from app.agents.fate_engine import FateEngineAgent
from app.agents.base import AgentConfig, AgentResponse
from app.models.fate import (
    FateThread, FateState, FateNode, FateNodeType,
    CausalEvent, EventType, CausalChain, FateReport, PredictedEvent,
    FateTrend
)
from app.models.character import (
    Character, Personality, OCEANDimensions, Background,
    FamilyBackground, CurrentState
)


@pytest.fixture
def agent_config():
    """Agent配置fixture"""
    return AgentConfig(
        name="fate_engine",
        description="Fate Engine Agent for managing fate threads",
        model="qwen-max",
        temperature=0.7
    )


@pytest.fixture
def mock_gateway():
    """Mock LLM Gateway"""
    gateway = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Mocked LLM response"
    gateway.generate = AsyncMock(return_value=mock_response)
    return gateway


@pytest.fixture
def sample_character():
    """示例人物"""
    return Character(
        character_id="char-001",
        name="张三",
        gender="男",
        birth_date=date(1990, 1, 1),
        personality=Personality(
            ocean=OCEANDimensions(
                openness=65.0,
                conscientiousness=70.0,
                extraversion=55.0,
                agreeableness=60.0,
                neuroticism=40.0
            )
        ),
        background=Background(
            family=FamilyBackground(
                father_occupation="教师",
                mother_occupation="医生",
                family_economic_status="middle"
            )
        ),
        current_state=CurrentState(
            age=30,
            occupation="工程师",
            income_level=6,
            relationship_status="single"
        ),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_event():
    """示例因果事件"""
    return CausalEvent(
        event_id="event-001",
        event_type=EventType.LIFE_STAGE,
        description="获得重要晋升机会",
        timestamp=datetime.now(),
        affected_characters=["char-001"],
        affected_aspects=["career", "income"],
        intensity=7.0
    )


@pytest.fixture
def sample_fate_thread(sample_character):
    """示例命运线"""
    initial_state = FateState(
        state_id="state-001",
        character_id=sample_character.character_id,
        fortune_level=50.0,
        challenge_level=50.0,
        growth_potential=60.0,
        trend=FateTrend.STABLE
    )

    return FateThread(
        thread_id="thread-001",
        character_id=sample_character.character_id,
        world_id="world-001",
        nodes=[],
        current_state=initial_state,
        tension_arc=[50.0],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


# 测试Agent初始化
def test_agent_initialization(agent_config, mock_gateway):
    """测试Agent初始化"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    assert agent.config.name == "fate_engine"
    assert agent.config.model == "qwen-max"
    assert agent.causal_engine is not None
    assert agent.fate_manager is not None
    assert agent.tension_calculator is not None
    assert agent.prompts is not None
    assert agent.chains == {}


# 测试advance action
@pytest.mark.asyncio
async def test_advance_fate(agent_config, mock_gateway, sample_event):
    """测试推进命运"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "advance",
        "event": sample_event.model_dump(),
        "world_id": "world-001",
        "context": {"current_tension": 50.0}
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "consequences" in response.data
    assert "tension_change" in response.data
    assert "analysis" in response.data


# 测试add_event action
@pytest.mark.asyncio
async def test_add_event(agent_config, mock_gateway, sample_event):
    """测试添加事件到因果链"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "add_event",
        "event": sample_event.model_dump(),
        "chain_id": "chain-001",
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "chain_id" in response.data
    assert "event_id" in response.data
    assert "current_tension" in response.data


# 测试get_report action
@pytest.mark.asyncio
async def test_get_report(agent_config, mock_gateway, sample_fate_thread):
    """测试获取命运报告"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    # 先创建一条命运线
    agent.fate_manager.threads[sample_fate_thread.thread_id] = sample_fate_thread

    input_data = {
        "action": "get_report",
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "report" in response.data
    assert "overall_tension" in response.data["report"]
    assert "active_threads" in response.data["report"]


# 测试create_thread action
@pytest.mark.asyncio
async def test_create_thread(agent_config, mock_gateway, sample_character):
    """测试创建命运线"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "create_thread",
        "character": sample_character.model_dump(),
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "thread_id" in response.data
    assert "character_id" in response.data
    assert "initial_state" in response.data


# 测试detect_intersection action
@pytest.mark.asyncio
async def test_detect_intersection(agent_config, mock_gateway, sample_fate_thread):
    """测试检测命运交织"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    # 创建两条命运线
    agent.fate_manager.threads[sample_fate_thread.thread_id] = sample_fate_thread

    # 创建第二条命运线
    second_thread = FateThread(
        thread_id="thread-002",
        character_id="char-002",
        world_id="world-001",
        nodes=[
            FateNode(
                node_id="node-001",
                node_type=FateNodeType.TURNING_POINT,
                trigger_event="event-001",
                affected_characters=["char-001", "char-002"]
            )
        ],
        current_state=sample_fate_thread.current_state,
        tension_arc=[50.0],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    agent.fate_manager.threads[second_thread.thread_id] = second_thread

    input_data = {
        "action": "detect_intersection",
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "intersections" in response.data


# 测试predict action
@pytest.mark.asyncio
async def test_predict_fate(agent_config, mock_gateway, sample_character, sample_fate_thread):
    """测试预测命运"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    agent.fate_manager.threads[sample_fate_thread.thread_id] = sample_fate_thread

    input_data = {
        "action": "predict",
        "character_id": sample_character.character_id,
        "world_context": {"world_id": "world-001"}
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "predictions" in response.data
    assert "short_term" in response.data["predictions"]
    assert "long_term" in response.data["predictions"]


# 测试未知action处理
@pytest.mark.asyncio
async def test_unknown_action(agent_config, mock_gateway):
    """测试未知action处理"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "unknown_action"
    }

    response = await agent.execute(input_data)

    assert response.success is False
    assert "Unknown action" in response.error


# 测试缺失数据处理 - 缺少action
@pytest.mark.asyncio
async def test_missing_action(agent_config, mock_gateway):
    """测试缺少action字段"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {}

    response = await agent.execute(input_data)

    assert response.success is False
    assert "action" in response.error.lower()


# 测试缺失数据处理 - advance缺少event
@pytest.mark.asyncio
async def test_advance_missing_event(agent_config, mock_gateway):
    """测试advance缺少event字段"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "advance",
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is False
    assert "event" in response.error.lower()


# 测试缺失数据处理 - create_thread缺少character
@pytest.mark.asyncio
async def test_create_thread_missing_character(agent_config, mock_gateway):
    """测试create_thread缺少character字段"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "create_thread",
        "world_id": "world-001"
    }

    response = await agent.execute(input_data)

    assert response.success is False
    assert "character" in response.error.lower()


# 测试因果链管理
@pytest.mark.asyncio
async def test_chain_management(agent_config, mock_gateway, sample_event):
    """测试因果链管理"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    # 添加第一个事件
    input_data1 = {
        "action": "add_event",
        "event": sample_event.model_dump(),
        "chain_id": "chain-001",
        "world_id": "world-001"
    }

    response1 = await agent.execute(input_data1)
    assert response1.success is True
    assert "chain-001" in agent.chains

    # 添加第二个事件
    second_event = CausalEvent(
        event_id="event-002",
        event_type=EventType.CAUSAL,
        description="晋升后的变化",
        timestamp=datetime.now(),
        causes=["event-001"],
        affected_characters=["char-001"],
        intensity=6.0
    )

    input_data2 = {
        "action": "add_event",
        "event": second_event.model_dump(),
        "chain_id": "chain-001",
        "world_id": "world-001"
    }

    response2 = await agent.execute(input_data2)
    assert response2.success is True
    assert len(agent.chains["chain-001"].events) == 2


# 测试张力计算集成
@pytest.mark.asyncio
async def test_tension_calculation_integration(agent_config, mock_gateway, sample_event):
    """测试张力计算集成"""
    agent = FateEngineAgent(agent_config, mock_gateway)

    input_data = {
        "action": "advance",
        "event": sample_event.model_dump(),
        "world_id": "world-001",
        "context": {"current_tension": 50.0}
    }

    response = await agent.execute(input_data)

    assert response.success is True
    assert "tension_change" in response.data
    # 高强度事件应该增加张力
    assert response.data["tension_change"] > 0
