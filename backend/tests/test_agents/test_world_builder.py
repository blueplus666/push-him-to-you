import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.world_builder import WorldBuilderAgent
from app.agents.base import AgentConfig, AgentResponse
from app.services.llm_gateway import LLMGateway


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="world_builder",
        description="World building agent",
        model="qwen-max",
        temperature=0.8
    )


@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=LLMGateway)
    return gateway


@pytest.fixture
def world_builder(agent_config, mock_gateway):
    return WorldBuilderAgent(agent_config, mock_gateway)


def test_world_builder_creation(world_builder):
    """测试WorldBuilder创建"""
    assert world_builder.config.name == "world_builder"
    assert world_builder.config.model == "qwen-max"


@pytest.mark.asyncio
async def test_world_builder_execute(world_builder, mock_gateway):
    """测试WorldBuilder执行"""
    mock_response = MagicMock()
    mock_response.content = """
## 世界概述
这是一个现代都市世界，位于江南水乡杭州。

## 社会结构
- 上层：企业家、高管
- 中层：白领、技术人员
- 底层：工人、服务业从业者

## 文化特征
- 核心价值观：勤劳、诚信、创新

## 环境特点
- 自然环境：江南水乡，四季分明

## 潜在冲突源
- 社会矛盾：贫富差距
"""
    mock_gateway.generate = AsyncMock(return_value=mock_response)

    input_data = {
        "era": "现代都市",
        "location": "杭州",
        "society_type": "平稳发展型",
        "special_settings": "无"
    }

    response = await world_builder.execute(input_data)

    assert response.success is True
    assert "world_state" in response.data


@pytest.mark.asyncio
async def test_world_builder_with_invalid_input(world_builder):
    """测试无效输入处理"""
    input_data = {}

    response = await world_builder.execute(input_data)

    assert response.success is False
    assert response.error is not None
