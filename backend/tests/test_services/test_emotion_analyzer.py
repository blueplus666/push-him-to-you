"""
测试情感分析器服务
"""
import pytest
from app.models.dialogue import EmotionalTone, DialogueLine
from app.services.emotion_analyzer import (
    EmotionAnalyzer,
    analyze_emotion,
    analyze_emotional_arc,
    suggest_emotion,
    get_emotion_keywords,
    get_all_emotion_keywords
)


class TestEmotionAnalyzer:
    """测试情感分析器"""

    def test_emotion_analyzer_creation(self):
        """测试情感分析器创建"""
        analyzer = EmotionAnalyzer()
        assert analyzer is not None

    def test_analyze_emotion_happy(self):
        """测试分析开心情感"""
        emotion = analyze_emotion("太棒了！我真的很开心！")
        assert emotion == EmotionalTone.HAPPY

    def test_analyze_emotion_sad(self):
        """测试分析悲伤情感"""
        emotion = analyze_emotion("我好难过，事情怎么会变成这样...")
        assert emotion == EmotionalTone.SAD

    def test_analyze_emotion_angry(self):
        """测试分析愤怒情感"""
        emotion = analyze_emotion("我真的很生气！你怎么能这样做！")
        assert emotion == EmotionalTone.ANGRY

    def test_analyze_emotion_fearful(self):
        """测试分析恐惧情感"""
        emotion = analyze_emotion("我好害怕，不知道会发生什么...")
        assert emotion == EmotionalTone.FEARFUL

    def test_analyze_emotion_surprised(self):
        """测试分析惊讶情感"""
        emotion = analyze_emotion("天哪！我完全没想到会是这样！")
        assert emotion == EmotionalTone.SURPRISED

    def test_analyze_emotion_neutral(self):
        """测试分析中性情感"""
        emotion = analyze_emotion("今天天气不错。")
        assert emotion == EmotionalTone.NEUTRAL

    def test_analyze_emotional_arc(self):
        """测试分析情感变化弧线"""
        lines = [
            DialogueLine(line_id="1", speaker_id="a", content="你好，今天怎么样？"),
            DialogueLine(line_id="2", speaker_id="b", content="太棒了！我升职了！"),
            DialogueLine(line_id="3", speaker_id="a", content="真的吗？太好了！"),
        ]
        arc = analyze_emotional_arc(lines)
        assert len(arc) == 3
        assert arc[0] == EmotionalTone.NEUTRAL
        assert arc[1] == EmotionalTone.HAPPY

    def test_analyze_emotional_arc_empty(self):
        """测试空对话行的情感弧线"""
        arc = analyze_emotional_arc([])
        assert arc == []

    def test_suggest_emotion_context_based(self):
        """测试基于上下文建议情感"""
        context = {
            "scene_type": "conflict",
            "tension_level": 80,
        }
        speaker_profile = {
            "personality": "热情",
        }
        emotion = suggest_emotion(context, speaker_profile)
        assert emotion in EmotionalTone

    def test_suggest_emotion_romantic_scene(self):
        """测试浪漫场景情感建议"""
        context = {
            "scene_type": "romantic",
            "tension_level": 50,
        }
        speaker_profile = {}
        emotion = suggest_emotion(context, speaker_profile)
        assert emotion in [EmotionalTone.HAPPY, EmotionalTone.NEUTRAL]

    def test_get_emotion_keywords(self):
        """测试获取情感关键词"""
        keywords = get_emotion_keywords(EmotionalTone.HAPPY)
        assert "开心" in keywords or "高兴" in keywords or "快乐" in keywords

    def test_get_all_emotion_keywords(self):
        """测试获取所有情感关键词"""
        all_keywords = get_all_emotion_keywords()
        assert EmotionalTone.HAPPY in all_keywords
        assert EmotionalTone.SAD in all_keywords
        assert EmotionalTone.ANGRY in all_keywords
