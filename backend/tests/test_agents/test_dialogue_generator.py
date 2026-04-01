"""
测试 DialogueGenerator Agent
"""
import pytest
from unittest.mock import MagicMock, AsyncMock

from app.agents.base import AgentConfig, AgentResponse
from app.agents.dialogue_generator import DialogueGeneratorAgent
from app.models.dialogue import DialogueType, DialogueStyle, EmotionalTone


class TestDialogueGeneratorAgentInit:
    """测试Agent初始化"""

    @pytest.fixture
    def agent_config(self):
        """创建Agent配置"""
        return AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )

    @pytest.fixture
    def mock_llm_gateway(self):
        """创建模拟LLM网关"""
        gateway = MagicMock()
        gateway.generate = AsyncMock(return_value="模拟对话内容")
        return gateway

    @pytest.fixture
    def agent(self, agent_config, mock_llm_gateway):
        """创建Agent实例"""
        return DialogueGeneratorAgent(agent_config, mock_llm_gateway)

    def test_agent_creation(self, agent):
        """测试Agent创建"""
        assert agent is not None
        assert agent.config.name == "dialogue_generator"

    def test_agent_inherits_from_base(self, agent):
        """测试Agent继承自BaseAgent"""
        from app.agents.base import BaseAgent
        assert isinstance(agent, BaseAgent)


class TestExecuteGenerateAction:
    """测试生成对话action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_generate_action(self, agent):
        """测试生成对话action"""
        response = await agent.execute({
            "action": "generate",
            "participants": ["char-001", "char-002"],
            "dialogue_type": "casual",
            "style": "casual",
            "topic": "日常聊天"
        })
        assert response.success is True
        assert "dialogue" in response.data

    @pytest.mark.asyncio
    async def test_generate_with_character_profiles(self, agent):
        """测试带角色档案的对话生成"""
        response = await agent.execute({
            "action": "generate",
            "participants": ["char-001"],
            "dialogue_type": "romantic",
            "style": "emotional",
            "character_profiles": {
                "char-001": {"name": "张三", "personality": "浪漫", "values": ["爱情"]}
            }
        })
        assert response.success is True

    @pytest.mark.asyncio
    async def test_generate_with_scene_context(self, agent):
        """测试带场景上下文的对话生成"""
        response = await agent.execute({
            "action": "generate",
            "participants": ["char-001"],
            "dialogue_type": "casual",
            "style": "casual",
            "scene_context": "咖啡厅",
            "topic": "闲聊"
        })
        assert response.success is True


class TestExecuteAnalyzeAction:
    """测试分析对话action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_analyze_action(self, agent):
        """测试分析对话action"""
        response = await agent.execute({
            "action": "analyze",
            "dialogue_content": "你好！我太开心了！"
        })
        assert response.success is True
        assert "emotion" in response.data


class TestExecuteImproveAction:
    """测试改进对话action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_improve_action(self, agent):
        """测试改进对话action"""
        gen_response = await agent.execute({
            "action": "generate",
            "participants": ["char-001"],
            "dialogue_type": "casual"
        })
        dialogue_id = gen_response.data["dialogue"]["dialogue_id"]

        response = await agent.execute({
            "action": "improve",
            "dialogue_id": dialogue_id,
            "improvement_goals": ["增加情感表达"]
        })
        assert response.success is True


class TestExecuteConvertStyleAction:
    """测试转换风格action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_convert_style_action(self, agent):
        """测试转换风格action"""
        gen_response = await agent.execute({
            "action": "generate",
            "participants": ["char-001"],
            "dialogue_type": "casual"
        })
        dialogue_id = gen_response.data["dialogue"]["dialogue_id"]

        response = await agent.execute({
            "action": "convert_style",
            "dialogue_id": dialogue_id,
            "target_style": "formal"
        })
        assert response.success is True


class TestExecuteAddEmotionAction:
    """测试添加情感action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_add_emotion_action(self, agent):
        """测试添加情感action"""
        gen_response = await agent.execute({
            "action": "generate",
            "participants": ["char-001"],
            "dialogue_type": "casual"
        })
        dialogue_id = gen_response.data["dialogue"]["dialogue_id"]

        response = await agent.execute({
            "action": "add_emotion",
            "dialogue_id": dialogue_id,
            "emotion": "happy"
        })
        assert response.success is True


class TestExecuteUnknownAction:
    """测试未知action"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        config = AgentConfig(
            name="dialogue_generator",
            description="对话生成器Agent",
            model="gpt-4",
            temperature=0.7,
        )
        mock_gateway = MagicMock()
        mock_gateway.generate = AsyncMock(return_value="模拟对话")
        return DialogueGeneratorAgent(config, mock_gateway)

    @pytest.mark.asyncio
    async def test_execute_unknown_action(self, agent):
        """测试未知action"""
        response = await agent.execute({
            "action": "unknown_action"
        })
        assert response.success is False
        assert "Unknown action" in response.error
