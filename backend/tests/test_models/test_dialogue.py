"""
测试 Dialogue 数据模型
TDD: RED 阶段 - 编写失败的测试
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.dialogue import (
    DialogueType,
    DialogueStyle,
    EmotionalTone,
    DialogueLine,
    DialogueParticipant,
    Dialogue,
    DialogueGenerationRequest,
    DialogueGenerationResult
)


class TestDialogueType:
    """测试对话类型枚举"""

    def test_dialogue_type_values(self):
        """测试对话类型枚举值"""
        assert DialogueType.CASUAL == "casual"
        assert DialogueType.FORMAL == "formal"
        assert DialogueType.CONFLICT == "conflict"
        assert DialogueType.ROMANTIC == "romantic"
        assert DialogueType.PHILOSOPHICAL == "philosophical"

    def test_dialogue_type_string_conversion(self):
        """测试对话类型字符串转换"""
        assert DialogueType.CASUAL.value == "casual"
        assert DialogueType.CONFLICT.value == "conflict"


class TestDialogueStyle:
    """测试对话风格枚举"""

    def test_dialogue_style_values(self):
        """测试对话风格枚举值"""
        assert DialogueStyle.FORMAL == "formal"
        assert DialogueStyle.CASUAL == "casual"
        assert DialogueStyle.EMOTIONAL == "emotional"
        assert DialogueStyle.HUMOROUS == "humorous"
        assert DialogueStyle.SERIOUS == "serious"

    def test_dialogue_style_string_conversion(self):
        """测试对话风格字符串转换"""
        assert DialogueStyle.EMOTIONAL.value == "emotional"
        assert DialogueStyle.HUMOROUS.value == "humorous"


class TestEmotionalTone:
    """测试情感基调枚举"""

    def test_emotional_tone_values(self):
        """测试情感基调枚举值"""
        assert EmotionalTone.NEUTRAL == "neutral"
        assert EmotionalTone.HAPPY == "happy"
        assert EmotionalTone.SAD == "sad"
        assert EmotionalTone.ANGRY == "angry"
        assert EmotionalTone.FEARFUL == "fearful"
        assert EmotionalTone.SURPRISED == "surprised"

    def test_emotional_tone_string_conversion(self):
        """测试情感基调字符串转换"""
        assert EmotionalTone.HAPPY.value == "happy"
        assert EmotionalTone.ANGRY.value == "angry"


class TestDialogueLine:
    """测试对话行模型"""

    def test_dialogue_line_creation(self):
        """测试对话行创建"""
        line = DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="你好，今天天气真不错。",
            subtext="想要开启一段轻松的对话",
            emotion="happy",
            action="微笑着看向窗外",
            pause_before=1.0,
            pause_after=0.5
        )
        assert line.line_id == "line-001"
        assert line.speaker_id == "char-001"
        assert line.content == "你好，今天天气真不错。"
        assert line.subtext == "想要开启一段轻松的对话"
        assert line.emotion == "happy"
        assert line.action == "微笑着看向窗外"
        assert line.pause_before == 1.0
        assert line.pause_after == 0.5

    def test_dialogue_line_minimal(self):
        """测试最小对话行"""
        line = DialogueLine(
            line_id="line-002",
            speaker_id="char-002",
            content="是的，很适合散步。"
        )
        assert line.line_id == "line-002"
        assert line.speaker_id == "char-002"
        assert line.content == "是的，很适合散步。"
        assert line.subtext is None
        assert line.emotion is None
        assert line.action is None
        assert line.pause_before is None
        assert line.pause_after is None

    def test_dialogue_line_with_metadata(self):
        """测试带元数据的对话行"""
        line = DialogueLine(
            line_id="line-003",
            speaker_id="char-001",
            content="测试内容",
            metadata={"timestamp": "2024-01-01", "location": "公园"}
        )
        assert line.metadata["timestamp"] == "2024-01-01"
        assert line.metadata["location"] == "公园"

    def test_dialogue_line_extra_fields(self):
        """测试对话行额外字段"""
        line = DialogueLine(
            line_id="line-004",
            speaker_id="char-001",
            content="测试内容",
            custom_field="自定义值"
        )
        assert line.custom_field == "自定义值"


class TestDialogueParticipant:
    """测试对话参与者模型"""

    def test_dialogue_participant_creation(self):
        """测试对话参与者创建"""
        participant = DialogueParticipant(
            character_id="char-001",
            character_name="张三",
            role="主角",
            initial_emotion="neutral",
            final_emotion="happy",
            lines_spoken=10,
            total_words=250
        )
        assert participant.character_id == "char-001"
        assert participant.character_name == "张三"
        assert participant.role == "主角"
        assert participant.initial_emotion == "neutral"
        assert participant.final_emotion == "happy"
        assert participant.lines_spoken == 10
        assert participant.total_words == 250

    def test_dialogue_participant_minimal(self):
        """测试最小对话参与者"""
        participant = DialogueParticipant(
            character_id="char-002",
            character_name="李四",
            role="配角"
        )
        assert participant.character_id == "char-002"
        assert participant.character_name == "李四"
        assert participant.role == "配角"
        assert participant.initial_emotion is None
        assert participant.final_emotion is None
        assert participant.lines_spoken == 0
        assert participant.total_words == 0

    def test_dialogue_participant_boundary_values(self):
        """测试对话参与者边界值"""
        participant_min = DialogueParticipant(
            character_id="char-003",
            character_name="测试",
            role="测试",
            lines_spoken=0,
            total_words=0
        )
        assert participant_min.lines_spoken == 0
        assert participant_min.total_words == 0

        participant_max = DialogueParticipant(
            character_id="char-004",
            character_name="测试",
            role="测试",
            lines_spoken=1000,
            total_words=50000
        )
        assert participant_max.lines_spoken == 1000
        assert participant_max.total_words == 50000

    def test_dialogue_participant_invalid_values(self):
        """测试对话参与者无效值"""
        with pytest.raises(ValidationError):
            DialogueParticipant(
                character_id="char-005",
                character_name="测试",
                role="测试",
                lines_spoken=-1
            )

        with pytest.raises(ValidationError):
            DialogueParticipant(
                character_id="char-006",
                character_name="测试",
                role="测试",
                total_words=-1
            )

    def test_dialogue_participant_extra_fields(self):
        """测试对话参与者额外字段"""
        participant = DialogueParticipant(
            character_id="char-007",
            character_name="测试",
            role="测试",
            custom_field="自定义值"
        )
        assert participant.custom_field == "自定义值"


class TestDialogue:
    """测试对话模型"""

    def test_dialogue_creation(self):
        """测试对话创建"""
        participant1 = DialogueParticipant(
            character_id="char-001",
            character_name="张三",
            role="主角"
        )
        participant2 = DialogueParticipant(
            character_id="char-002",
            character_name="李四",
            role="配角"
        )
        line1 = DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="你好！"
        )
        line2 = DialogueLine(
            line_id="line-002",
            speaker_id="char-002",
            content="你好，很高兴见到你。"
        )

        dialogue = Dialogue(
            dialogue_id="dialogue-001",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            participants=[participant1, participant2],
            lines=[line1, line2],
            scene_id="scene-001",
            location="咖啡馆",
            mood="轻松",
            tension_level=30.0,
            summary="两个角色的初次见面",
            key_points=["问候", "自我介绍"],
            total_lines=2,
            total_words=15,
            duration_estimate=5.0
        )

        assert dialogue.dialogue_id == "dialogue-001"
        assert dialogue.dialogue_type == DialogueType.CASUAL
        assert dialogue.style == DialogueStyle.CASUAL
        assert len(dialogue.participants) == 2
        assert len(dialogue.lines) == 2
        assert dialogue.scene_id == "scene-001"
        assert dialogue.location == "咖啡馆"
        assert dialogue.mood == "轻松"
        assert dialogue.tension_level == 30.0
        assert dialogue.summary == "两个角色的初次见面"
        assert len(dialogue.key_points) == 2
        assert dialogue.total_lines == 2
        assert dialogue.total_words == 15
        assert dialogue.duration_estimate == 5.0

    def test_dialogue_default_values(self):
        """测试对话默认值"""
        dialogue = Dialogue(
            dialogue_id="dialogue-002",
            dialogue_type=DialogueType.FORMAL,
            style=DialogueStyle.FORMAL
        )
        assert dialogue.participants == []
        assert dialogue.lines == []
        assert dialogue.scene_id is None
        assert dialogue.location == ""
        assert dialogue.mood == ""
        assert dialogue.tension_level == 50.0
        assert dialogue.summary == ""
        assert dialogue.key_points == []
        assert dialogue.total_lines == 0
        assert dialogue.total_words == 0
        assert dialogue.duration_estimate == 0.0
        assert isinstance(dialogue.created_at, datetime)
        assert isinstance(dialogue.updated_at, datetime)

    def test_dialogue_add_line(self):
        """测试添加对话行"""
        dialogue = Dialogue(
            dialogue_id="dialogue-003",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )

        line = DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="测试对话"
        )

        dialogue.add_line(line)
        assert len(dialogue.lines) == 1
        assert dialogue.lines[0].line_id == "line-001"
        assert dialogue.total_lines == 1

    def test_dialogue_get_speaker_lines(self):
        """测试获取说话者的对话行"""
        line1 = DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="第一句"
        )
        line2 = DialogueLine(
            line_id="line-002",
            speaker_id="char-002",
            content="第二句"
        )
        line3 = DialogueLine(
            line_id="line-003",
            speaker_id="char-001",
            content="第三句"
        )

        dialogue = Dialogue(
            dialogue_id="dialogue-004",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            lines=[line1, line2, line3]
        )

        speaker_lines = dialogue.get_speaker_lines("char-001")
        assert len(speaker_lines) == 2
        assert speaker_lines[0].line_id == "line-001"
        assert speaker_lines[1].line_id == "line-003"

        no_lines = dialogue.get_speaker_lines("char-999")
        assert len(no_lines) == 0

    def test_dialogue_calculate_statistics(self):
        """测试计算统计数据"""
        line1 = DialogueLine(
            line_id="line-001",
            speaker_id="char-001",
            content="这是一句测试对话"
        )
        line2 = DialogueLine(
            line_id="line-002",
            speaker_id="char-002",
            content="这是另一句对话"
        )

        dialogue = Dialogue(
            dialogue_id="dialogue-005",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            lines=[line1, line2]
        )

        stats = dialogue.calculate_statistics()
        assert stats["total_lines"] == 2
        assert stats["total_words"] == 15
        assert "avg_words_per_line" in stats

    def test_dialogue_boundary_values(self):
        """测试对话边界值"""
        dialogue_min = Dialogue(
            dialogue_id="dialogue-006",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            tension_level=0.0,
            total_lines=0,
            total_words=0,
            duration_estimate=0.0
        )
        assert dialogue_min.tension_level == 0.0

        dialogue_max = Dialogue(
            dialogue_id="dialogue-007",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            tension_level=100.0,
            total_lines=1000,
            total_words=100000,
            duration_estimate=3600.0
        )
        assert dialogue_max.tension_level == 100.0

    def test_dialogue_invalid_values(self):
        """测试对话无效值"""
        with pytest.raises(ValidationError):
            Dialogue(
                dialogue_id="dialogue-008",
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                tension_level=-1.0
            )

        with pytest.raises(ValidationError):
            Dialogue(
                dialogue_id="dialogue-009",
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                tension_level=101.0
            )

        with pytest.raises(ValidationError):
            Dialogue(
                dialogue_id="dialogue-010",
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                total_lines=-1
            )

        with pytest.raises(ValidationError):
            Dialogue(
                dialogue_id="dialogue-011",
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                total_words=-1
            )

    def test_dialogue_extra_fields(self):
        """测试对话额外字段"""
        dialogue = Dialogue(
            dialogue_id="dialogue-012",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            custom_field="自定义值"
        )
        assert dialogue.custom_field == "自定义值"


class TestDialogueGenerationRequest:
    """测试对话生成请求模型"""

    def test_dialogue_generation_request_creation(self):
        """测试对话生成请求创建"""
        request = DialogueGenerationRequest(
            request_id="request-001",
            participants=["char-001", "char-002"],
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            scene_context="在咖啡馆的初次见面",
            topic="日常闲聊",
            goal="建立友谊",
            min_lines=10,
            max_lines=20,
            include_actions=True,
            include_subtext=True,
            character_profiles={"char-001": {"name": "张三", "personality": "开朗"}}
        )

        assert request.request_id == "request-001"
        assert len(request.participants) == 2
        assert request.dialogue_type == DialogueType.CASUAL
        assert request.style == DialogueStyle.CASUAL
        assert request.scene_context == "在咖啡馆的初次见面"
        assert request.topic == "日常闲聊"
        assert request.goal == "建立友谊"
        assert request.min_lines == 10
        assert request.max_lines == 20
        assert request.include_actions is True
        assert request.include_subtext is True
        assert "char-001" in request.character_profiles

    def test_dialogue_generation_request_minimal(self):
        """测试最小对话生成请求"""
        request = DialogueGenerationRequest(
            request_id="request-002",
            participants=["char-001"],
            dialogue_type=DialogueType.FORMAL,
            style=DialogueStyle.FORMAL
        )
        assert request.request_id == "request-002"
        assert len(request.participants) == 1
        assert request.scene_context is None
        assert request.topic is None
        assert request.goal is None
        assert request.min_lines == 5
        assert request.max_lines == 20
        assert request.include_actions is False
        assert request.include_subtext is False
        assert request.character_profiles == {}

    def test_dialogue_generation_request_boundary_values(self):
        """测试对话生成请求边界值"""
        request_min = DialogueGenerationRequest(
            request_id="request-003",
            participants=["char-001"],
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            min_lines=1,
            max_lines=1
        )
        assert request_min.min_lines == 1
        assert request_min.max_lines == 1

        request_max = DialogueGenerationRequest(
            request_id="request-004",
            participants=["char-001"],
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            min_lines=100,
            max_lines=100
        )
        assert request_max.min_lines == 100
        assert request_max.max_lines == 100

    def test_dialogue_generation_request_invalid_values(self):
        """测试对话生成请求无效值"""
        with pytest.raises(ValidationError):
            DialogueGenerationRequest(
                request_id="request-005",
                participants=["char-001"],
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                min_lines=0
            )

        with pytest.raises(ValidationError):
            DialogueGenerationRequest(
                request_id="request-006",
                participants=["char-001"],
                dialogue_type=DialogueType.CASUAL,
                style=DialogueStyle.CASUAL,
                max_lines=0
            )

    def test_dialogue_generation_request_extra_fields(self):
        """测试对话生成请求额外字段"""
        request = DialogueGenerationRequest(
            request_id="request-007",
            participants=["char-001"],
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL,
            custom_field="自定义值"
        )
        assert request.custom_field == "自定义值"


class TestDialogueGenerationResult:
    """测试对话生成结果模型"""

    def test_dialogue_generation_result_creation(self):
        """测试对话生成结果创建"""
        dialogue = Dialogue(
            dialogue_id="dialogue-001",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )

        result = DialogueGenerationResult(
            result_id="result-001",
            request_id="request-001",
            dialogue=dialogue,
            generation_method="ai",
            quality_score=85.0,
            character_consistency=90.0,
            emotional_arc=["neutral", "happy", "excited"],
            improvements=["增加更多情感描述", "加强角色互动"],
            alternative_versions=[]
        )

        assert result.result_id == "result-001"
        assert result.request_id == "request-001"
        assert result.dialogue.dialogue_id == "dialogue-001"
        assert result.generation_method == "ai"
        assert result.quality_score == 85.0
        assert result.character_consistency == 90.0
        assert len(result.emotional_arc) == 3
        assert len(result.improvements) == 2
        assert len(result.alternative_versions) == 0

    def test_dialogue_generation_result_minimal(self):
        """测试最小对话生成结果"""
        dialogue = Dialogue(
            dialogue_id="dialogue-002",
            dialogue_type=DialogueType.FORMAL,
            style=DialogueStyle.FORMAL
        )

        result = DialogueGenerationResult(
            result_id="result-002",
            request_id="request-002",
            dialogue=dialogue,
            generation_method="template"
        )

        assert result.result_id == "result-002"
        assert result.request_id == "request-002"
        assert result.quality_score == 0.0
        assert result.character_consistency == 0.0
        assert result.emotional_arc == []
        assert result.improvements == []
        assert result.alternative_versions == []

    def test_dialogue_generation_result_boundary_values(self):
        """测试对话生成结果边界值"""
        dialogue = Dialogue(
            dialogue_id="dialogue-003",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )

        result_min = DialogueGenerationResult(
            result_id="result-003",
            request_id="request-003",
            dialogue=dialogue,
            generation_method="ai",
            quality_score=0.0,
            character_consistency=0.0
        )
        assert result_min.quality_score == 0.0
        assert result_min.character_consistency == 0.0

        result_max = DialogueGenerationResult(
            result_id="result-004",
            request_id="request-004",
            dialogue=dialogue,
            generation_method="ai",
            quality_score=100.0,
            character_consistency=100.0
        )
        assert result_max.quality_score == 100.0
        assert result_max.character_consistency == 100.0

    def test_dialogue_generation_result_invalid_values(self):
        """测试对话生成结果无效值"""
        dialogue = Dialogue(
            dialogue_id="dialogue-004",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )

        with pytest.raises(ValidationError):
            DialogueGenerationResult(
                result_id="result-005",
                request_id="request-005",
                dialogue=dialogue,
                generation_method="ai",
                quality_score=-1.0
            )

        with pytest.raises(ValidationError):
            DialogueGenerationResult(
                result_id="result-006",
                request_id="request-006",
                dialogue=dialogue,
                generation_method="ai",
                quality_score=101.0
            )

        with pytest.raises(ValidationError):
            DialogueGenerationResult(
                result_id="result-007",
                request_id="request-007",
                dialogue=dialogue,
                generation_method="ai",
                character_consistency=-1.0
            )

        with pytest.raises(ValidationError):
            DialogueGenerationResult(
                result_id="result-008",
                request_id="request-008",
                dialogue=dialogue,
                generation_method="ai",
                character_consistency=101.0
            )

    def test_dialogue_generation_result_extra_fields(self):
        """测试对话生成结果额外字段"""
        dialogue = Dialogue(
            dialogue_id="dialogue-005",
            dialogue_type=DialogueType.CASUAL,
            style=DialogueStyle.CASUAL
        )

        result = DialogueGenerationResult(
            result_id="result-009",
            request_id="request-009",
            dialogue=dialogue,
            generation_method="ai",
            custom_field="自定义值"
        )
        assert result.custom_field == "自定义值"
