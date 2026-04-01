"""
对话生成器Agent
负责生成、分析、改进和转换对话
"""
from typing import Dict, Any
import uuid

from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.services.dialogue_generator import DialogueGenerator
from app.services.emotion_analyzer import EmotionAnalyzer
from app.services.style_manager import StyleManager
from app.prompts.dialogue_prompts import DialogueGeneratorPrompts
from app.models.dialogue import (
    DialogueType,
    DialogueStyle,
    EmotionalTone,
    Dialogue,
    DialogueLine,
    DialogueGenerationRequest,
)


class DialogueGeneratorAgent(BaseAgent):
    """对话生成器Agent

    负责生成、分析、改进和转换对话。
    """

    def __init__(self, config: AgentConfig, llm_gateway):
        """初始化对话生成器Agent

        Args:
            config: Agent配置
            llm_gateway: LLM网关
        """
        super().__init__(config, llm_gateway)
        self.dialogue_generator = DialogueGenerator()
        self.emotion_analyzer = EmotionAnalyzer()
        self.style_manager = StyleManager()
        self.prompts = DialogueGeneratorPrompts()
        self.dialogues: Dict[str, Dialogue] = {}

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行Agent任务

        Actions:
        - generate: 生成对话
        - analyze: 分析对话
        - improve: 改进对话
        - convert_style: 转换风格
        - add_emotion: 添加情感

        Args:
            input_data: 输入数据

        Returns:
            AgentResponse: Agent响应
        """
        action = input_data.get("action", "generate")

        action_handlers = {
            "generate": self._generate_dialogue,
            "analyze": self._analyze_dialogue,
            "improve": self._improve_dialogue,
            "convert_style": self._convert_style,
            "add_emotion": self._add_emotion,
        }

        handler = action_handlers.get(action)
        if not handler:
            return AgentResponse(
                success=False,
                error=f"Unknown action: {action}"
            )

        return await handler(input_data)

    async def _generate_dialogue(self, input_data: Dict[str, Any]) -> AgentResponse:
        """生成对话

        Args:
            input_data: 输入数据，包含:
                - participants: 参与者ID列表
                - dialogue_type: 对话类型
                - style: 对话风格
                - topic: 话题
                - scene_context: 场景上下文
                - min_lines: 最小行数
                - character_profiles: 角色档案

        Returns:
            AgentResponse: 包含生成的对话
        """
        participants = input_data.get("participants")
        if not participants:
            return AgentResponse(
                success=False,
                error="Missing required parameter: participants"
            )

        dialogue_type_str = input_data.get("dialogue_type", "casual")
        style_str = input_data.get("style", "casual")
        topic = input_data.get("topic", "")
        scene_context = input_data.get("scene_context", "")
        min_lines = input_data.get("min_lines", 5)
        character_profiles = input_data.get("character_profiles", {})

        try:
            dialogue_type = DialogueType(dialogue_type_str)
            style = DialogueStyle(style_str)
        except ValueError as e:
            return AgentResponse(
                success=False,
                error=f"Invalid dialogue type or style: {e}"
            )

        request = DialogueGenerationRequest(
            request_id=f"req_{uuid.uuid4().hex[:8]}",
            participants=participants,
            dialogue_type=dialogue_type,
            style=style,
            scene_context=scene_context,
            topic=topic,
            min_lines=min_lines,
            character_profiles=character_profiles
        )

        dialogue = self.dialogue_generator.generate_dialogue(request, character_profiles)

        self.dialogues[dialogue.dialogue_id] = dialogue

        return AgentResponse(
            success=True,
            data={"dialogue": dialogue.model_dump()},
            metadata={"action": "generate"}
        )

    async def _analyze_dialogue(self, input_data: Dict[str, Any]) -> AgentResponse:
        """分析对话

        Args:
            input_data: 输入数据，包含:
                - dialogue_content: 对话内容

        Returns:
            AgentResponse: 包含情感分析结果
        """
        dialogue_content = input_data.get("dialogue_content")
        if not dialogue_content:
            return AgentResponse(
                success=False,
                error="Missing required parameter: dialogue_content"
            )

        emotion = self.emotion_analyzer.analyze(dialogue_content)

        return AgentResponse(
            success=True,
            data={"emotion": emotion.value},
            metadata={"action": "analyze"}
        )

    async def _improve_dialogue(self, input_data: Dict[str, Any]) -> AgentResponse:
        """改进对话

        Args:
            input_data: 输入数据，包含:
                - dialogue_id: 对话ID
                - character_profiles: 角色档案
                - improvement_goals: 改进目标列表

        Returns:
            AgentResponse: 包含改进后的对话
        """
        dialogue_id = input_data.get("dialogue_id")
        if not dialogue_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: dialogue_id"
            )

        dialogue = self.dialogues.get(dialogue_id)
        if not dialogue:
            return AgentResponse(
                success=False,
                error=f"Dialogue not found: {dialogue_id}"
            )

        character_profiles = input_data.get("character_profiles", {})
        improvement_goals = input_data.get("improvement_goals", [])

        consistency_score = self.dialogue_generator.ensure_consistency(
            dialogue, character_profiles
        )

        dialogue_data = dialogue.model_dump()
        dialogue_data["consistency_score"] = consistency_score
        dialogue_data["improvement_goals"] = improvement_goals

        return AgentResponse(
            success=True,
            data={"dialogue": dialogue_data},
            metadata={"action": "improve"}
        )

    async def _convert_style(self, input_data: Dict[str, Any]) -> AgentResponse:
        """转换对话风格

        Args:
            input_data: 输入数据，包含:
                - dialogue_id: 对话ID
                - target_style: 目标风格
                - character_profiles: 角色档案

        Returns:
            AgentResponse: 包含转换后的对话
        """
        dialogue_id = input_data.get("dialogue_id")
        target_style_str = input_data.get("target_style")

        if not dialogue_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: dialogue_id"
            )

        if not target_style_str:
            return AgentResponse(
                success=False,
                error="Missing required parameter: target_style"
            )

        dialogue = self.dialogues.get(dialogue_id)
        if not dialogue:
            return AgentResponse(
                success=False,
                error=f"Dialogue not found: {dialogue_id}"
            )

        try:
            target_style = DialogueStyle(target_style_str)
        except ValueError as e:
            return AgentResponse(
                success=False,
                error=f"Invalid target style: {e}"
            )

        character_profiles = input_data.get("character_profiles", {})

        dialogue.style = target_style

        for line in dialogue.lines:
            speaker_profile = character_profiles.get(line.speaker_id, {})
            character_voice = speaker_profile.get("voice", {})
            line.content = self.dialogue_generator.apply_style(
                line.content, target_style, character_voice
            )

        return AgentResponse(
            success=True,
            data={"dialogue": dialogue.model_dump()},
            metadata={"action": "convert_style"}
        )

    async def _add_emotion(self, input_data: Dict[str, Any]) -> AgentResponse:
        """添加情感表达

        Args:
            input_data: 输入数据，包含:
                - dialogue_id: 对话ID
                - emotion: 情感类型
                - character_profiles: 角色档案

        Returns:
            AgentResponse: 包含添加情感后的对话
        """
        dialogue_id = input_data.get("dialogue_id")
        emotion_str = input_data.get("emotion")

        if not dialogue_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: dialogue_id"
            )

        if not emotion_str:
            return AgentResponse(
                success=False,
                error="Missing required parameter: emotion"
            )

        dialogue = self.dialogues.get(dialogue_id)
        if not dialogue:
            return AgentResponse(
                success=False,
                error=f"Dialogue not found: {dialogue_id}"
            )

        try:
            emotion = EmotionalTone(emotion_str)
        except ValueError as e:
            return AgentResponse(
                success=False,
                error=f"Invalid emotion: {e}"
            )

        for line in dialogue.lines:
            line.emotion = emotion.value

        return AgentResponse(
            success=True,
            data={"dialogue": dialogue.model_dump()},
            metadata={"action": "add_emotion"}
        )
