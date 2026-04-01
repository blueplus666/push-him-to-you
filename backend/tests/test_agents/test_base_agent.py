import pytest
from abc import ABC
from unittest.mock import MagicMock, AsyncMock
from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.services.llm_gateway import LLMGateway
from pydantic import ValidationError


class TestAgent(BaseAgent):
    """测试用Agent"""
    
    async def execute(self, input_data: dict) -> AgentResponse:
        return AgentResponse(
            success=True,
            data={"result": "test"},
            metadata={"agent": "test"}
        )


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="test_agent",
        description="Test agent for unit tests",
        model="qwen-max",
        temperature=0.7
    )


@pytest.fixture
def mock_gateway():
    from unittest.mock import MagicMock
    gateway = MagicMock(spec=LLMGateway)
    return gateway


def test_agent_config_creation(agent_config):
    """测试Agent配置创建"""
    assert agent_config.name == "test_agent"
    assert agent_config.model == "qwen-max"
    assert agent_config.temperature == 0.7


def test_agent_response_creation():
    """测试Agent响应创建"""
    response = AgentResponse(
        success=True,
        data={"key": "value"},
        metadata={"time": 0.5}
    )
    assert response.success is True
    assert response.data == {"key": "value"}


def test_base_agent_is_abstract():
    """测试BaseAgent是抽象类"""
    with pytest.raises(TypeError):
        BaseAgent(AgentConfig(name="test", model="test"))


def test_test_agent_creation(agent_config, mock_gateway):
    """测试具体Agent创建"""
    agent = TestAgent(agent_config, mock_gateway)
    assert agent.config.name == "test_agent"


@pytest.mark.asyncio
async def test_test_agent_execute(agent_config, mock_gateway):
    """测试Agent执行"""
    agent = TestAgent(agent_config, mock_gateway)
    response = await agent.execute({"input": "test"})
    assert response.success is True
    assert response.data == {"result": "test"}


def test_get_provider():
    """测试提供商推断"""
    config = AgentConfig(name="test", model="qwen-max")
    agent = TestAgent(config, MagicMock())
    assert agent._get_provider() == "qwen"
    
    config2 = AgentConfig(name="test", model="glm-5")
    agent2 = TestAgent(config2, MagicMock())
    assert agent2._get_provider() == "glm"
    
    config3 = AgentConfig(name="test", model="unknown-model")
    agent3 = TestAgent(config3, MagicMock())
    assert agent3._get_provider() == "qwen"  # 默认


@pytest.mark.asyncio
async def test_generate_success():
    """测试generate方法成功"""
    config = AgentConfig(name="test", model="qwen-max")
    mock_gateway = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Generated text"
    mock_gateway.generate = AsyncMock(return_value=mock_response)
    
    agent = TestAgent(config, mock_gateway)
    result = await agent.generate("test prompt")
    assert result == "Generated text"


@pytest.mark.asyncio
async def test_generate_failure():
    """测试generate方法失败"""
    config = AgentConfig(name="test", model="qwen-max")
    mock_gateway = MagicMock()
    mock_gateway.generate = AsyncMock(side_effect=Exception("API error"))
    
    agent = TestAgent(config, mock_gateway)
    
    with pytest.raises(RuntimeError, match="LLM generation failed"):
        await agent.generate("test prompt")


def test_agent_config_validation():
    """测试配置验证"""
    with pytest.raises(ValidationError):
        AgentConfig(name="test", model="test", temperature=3.0)  # 超出范围
    
    with pytest.raises(ValidationError):
        AgentConfig(name="test", model="test", max_tokens=0)  # 小于1
