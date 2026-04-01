"""
测试对话生成器服务
"""
import pytest
from app.models.dialogue import (
    DialogueType,
    DialogueStyle,
    EmotionalTone,
    DialogueLine,
    Dialogue,
    DialogueGenerationRequest,
)
from app.services.dialogue_generator import DialogueGenerator


class TestDialogueGenerator:
    """测试对话生成器"""

    def test_dialogue_generator_creation(self):
        """测试对话生成器创建"""
        generator = DialogueGenerator()
        assert generator is not None

    def test_generate_dialogue_basic(self):
        """测试基本对话生成"""
        generator = DialogueGenerator()
        request = DialogueGenerationRequest(
            request_id="req-001",
            participants=["char-001", "char-002"],
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            topic="日常聊天"
        )
        character_profiles = {
            "char-001": {"name": "张三", "personality": "外向"},
            "char-002": {"name": "李四", "personality": "内向"}
        }
        dialogue = generator.generate_dialogue(request, character_profiles)
        assert dialogue is not None
        assert dialogue.dialogue_type == DialogueType.CASUAL
        assert len(dialogue.lines) >= request.min_lines

    def test_generate_line(self):
        """测试生成单行对话"""
        generator = DialogueGenerator()
        speaker = {
            "id": "char-001",
            "name": "张三",
            "personality": "外向"
        }
        context = {
            "topic": "讨论工作",
            "previous_lines": [],
            "dialogue_type": DialogueType.CASUAL
        }
        line = generator.generate_line(speaker, context, DialogueStyle.CASUAL)
        assert line is not None
        assert line.speaker_id == "char-001"
        assert len(line.content) > 0

    def test_apply_style_casual(self):
        """测试应用随意风格"""
        generator = DialogueGenerator()
        content = "请问您今天有什么安排？"
        styled = generator.apply_style(
            content,
            DialogueStyle.CASUAL,
            {}
        )
        assert styled is not None
        assert len(styled) > 0

    def test_apply_style_formal(self):
        """测试应用正式风格"""
        generator = DialogueGenerator()
        content = "你今天干啥呢？"
        styled = generator.apply_style(
            content,
            DialogueStyle.FORMAL,
            {}
        )
        assert styled is not None

    def test_ensure_consistency(self):
        """测试确保角色一致性"""
        generator = DialogueGenerator()
        dialogue = Dialogue(
            dialogue_id="dialogue-001",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )
        dialogue.add_line(DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="你好！"
        ))
        character_profiles = {
            "char-001": {"personality": "外向", "values": ["友谊"]}
        }
        score = generator.ensure_consistency(dialogue, character_profiles)
        assert 0 <= score <= 100

    def test_generate_dialogue_with_emotions(self):
        """测试带情感的对话生成"""
        generator = DialogueGenerator()
        request = DialogueGenerationRequest(
            request_id="req-002",
            participants=["char-001"],
            dialogue_type=DialogueType.ROMANTIC,
            style=DialogueStyle.EMOTIONAL,
            scene_context="浪漫场景"
        )
        character_profiles = {"char-001": {"name": "张三", "personality": "浪漫"}}
        dialogue = generator.generate_dialogue(request, character_profiles)
        assert dialogue is not None

    def test_generate_dialogue_conflict(self):
        """测试冲突对话生成"""
        generator = DialogueGenerator()
        request = DialogueGenerationRequest(
            request_id="req-003",
            participants=["char-001", "char-002"],
            dialogue_type=DialogueType.CONFLICT,
            style=DialogueStyle.SERIOUS,
            topic="争执"
        )
        character_profiles = {
            "char-001": {"name": "张三", "personality": "固执"},
            "char-002": {"name": "李四", "personality": "倔强"}
        }
        dialogue = generator.generate_dialogue(request, character_profiles)
        assert dialogue.dialogue_type == DialogueType.CONFLICT

    def test_get_dialogue_templates(self):
        """测试获取对话模板"""
        generator = DialogueGenerator()
        templates = generator.get_dialogue_templates()
        assert DialogueType.CASUAL in templates
        assert DialogueType.FORMAL in templates
        assert DialogueType.CONFLICT in templates

    def test_format_character_info(self):
        """测试格式化角色信息"""
        generator = DialogueGenerator()
        participants = [
            {"id": "char-001", "name": "张三", "role": "主角"},
            {"id": "char-002", "name": "李四", "role": "配角"}
        ]
        profiles = {
            "char-001": {"name": "张三", "personality": "外向"},
            "char-002": {"name": "李四", "personality": "内向"}
        }
        info = generator.format_character_info(participants, profiles)
        assert "张三" in info
        assert "李四" in info
