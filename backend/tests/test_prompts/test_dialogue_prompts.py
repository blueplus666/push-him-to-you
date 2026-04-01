"""
测试对话提示词模板
"""
import pytest
from app.models.dialogue import DialogueType, DialogueStyle
from app.prompts.dialogue_prompts import (
    DIALOGUE_GENERATOR_SYSTEM_PROMPT,
    DIALOGUE_GENERATION_PROMPT,
    DialogueGeneratorPrompts,
)


class TestDialoguePrompts:
    """测试对话提示词模板"""

    def test_system_prompt_exists(self):
        """测试系统提示词存在"""
        assert DIALOGUE_GENERATOR_SYSTEM_PROMPT is not None
        assert len(DIALOGUE_GENERATOR_SYSTEM_PROMPT) > 0
        assert "对话" in DIALOGUE_GENERATOR_SYSTEM_PROMPT

    def test_dialogue_generation_prompt_exists(self):
        """测试对话生成提示词存在"""
        assert DIALOGUE_GENERATION_PROMPT is not None
        assert len(DIALOGUE_GENERATION_PROMPT) > 0
        assert "{scene_info}" in DIALOGUE_GENERATION_PROMPT

    def test_dialogue_generator_prompts_creation(self):
        """测试提示词管理器创建"""
        prompts = DialogueGeneratorPrompts()
        assert prompts is not None

    def test_get_system_prompt(self):
        """测试获取系统提示词"""
        prompts = DialogueGeneratorPrompts()
        system_prompt = prompts.get_system_prompt()
        assert system_prompt == DIALOGUE_GENERATOR_SYSTEM_PROMPT

    def test_get_dialogue_generation_prompt(self):
        """测试获取对话生成提示词"""
        prompts = DialogueGeneratorPrompts()
        formatted = prompts.get_dialogue_generation_prompt(
            scene_info={"location": "咖啡厅", "time": "下午", "atmosphere": "轻松"},
            participants=[{"name": "张三", "role": "主角", "personality": "外向"}],
            dialogue_type="casual",
            context="朋友相遇",
            requirements="自然对话"
        )
        assert "咖啡厅" in formatted
        assert "张三" in formatted

    def test_get_emotion_analysis_prompt(self):
        """测试获取情感分析提示词"""
        prompts = DialogueGeneratorPrompts()
        formatted = prompts.get_emotion_analysis_prompt(
            dialogue_content="你好！我太开心了！",
            context="朋友分享好消息"
        )
        assert "你好" in formatted

    def test_get_style_conversion_prompt(self):
        """测试获取风格转换提示词"""
        prompts = DialogueGeneratorPrompts()
        formatted = prompts.get_style_conversion_prompt(
            original_text="你今天干啥呢？",
            target_style="formal",
            character_profile={"name": "张三", "personality": "正式"}
        )
        assert "formal" in formatted or "正式" in formatted

    def test_format_participants(self):
        """测试格式化参与者"""
        prompts = DialogueGeneratorPrompts()
        participants = [
            {"name": "张三", "role": "speaker", "personality": "外向"},
            {"name": "李四", "role": "listener", "personality": "内向"}
        ]
        formatted = prompts._format_participants(participants)
        assert "张三" in formatted
        assert "李四" in formatted
