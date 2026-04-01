"""
情感分析器
分析对话文本的情感和情感变化
"""
from typing import Dict, Any, List

from app.models.dialogue import EmotionalTone, DialogueLine


EMOTION_KEYWORDS = {
    EmotionalTone.HAPPY: [
        "开心", "高兴", "快乐", "棒", "好", "喜欢", "爱", "幸福", "兴奋", "愉快"
    ],
    EmotionalTone.SAD: [
        "难过", "悲伤", "伤心", "哭", "泪", "失望", "沮丧", "失落", "痛苦", "遗憾"
    ],
    EmotionalTone.ANGRY: [
        "生气", "愤怒", "恼火", "讨厌", "恨", "火", "烦", "气死", "暴怒", "不爽"
    ],
    EmotionalTone.FEARFUL: [
        "害怕", "恐惧", "担心", "焦虑", "紧张", "不安", "惊恐", "惶恐", "畏惧"
    ],
    EmotionalTone.SURPRISED: [
        "惊讶", "吃惊", "意外", "震惊", "没想到", "天哪", "居然", "竟然", "啊"
    ],
    EmotionalTone.NEUTRAL: [],
}


class EmotionAnalyzer:
    """情感分析器类"""

    def __init__(self):
        """初始化情感分析器"""
        self.keywords = EMOTION_KEYWORDS

    def analyze(self, text: str) -> EmotionalTone:
        """分析文本情感"""
        return analyze_emotion(text)

    def analyze_arc(self, lines: List[DialogueLine]) -> List[EmotionalTone]:
        """分析情感变化弧线"""
        return analyze_emotional_arc(lines)

    def suggest(self, context: Dict[str, Any], speaker_profile: Dict[str, Any]) -> EmotionalTone:
        """建议合适的情感"""
        return suggest_emotion(context, speaker_profile)


def analyze_emotion(text: str) -> EmotionalTone:
    """
    分析文本情感

    Args:
        text: 要分析的文本

    Returns:
        检测到的情感基调
    """
    emotion_scores: Dict[EmotionalTone, int] = {tone: 0 for tone in EmotionalTone}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                emotion_scores[emotion] += 1

    max_score = max(emotion_scores.values())
    if max_score == 0:
        return EmotionalTone.NEUTRAL

    for emotion, score in emotion_scores.items():
        if score == max_score:
            return emotion

    return EmotionalTone.NEUTRAL


def analyze_emotional_arc(lines: List[DialogueLine]) -> List[EmotionalTone]:
    """
    分析情感变化弧线

    Args:
        lines: 对话行列表

    Returns:
        情感基调列表，每行对话对应一个情感
    """
    return [analyze_emotion(line.content) for line in lines]


def suggest_emotion(context: Dict[str, Any], speaker_profile: Dict[str, Any]) -> EmotionalTone:
    """
    建议合适的情感

    Args:
        context: 场景上下文信息
        speaker_profile: 说话者档案

    Returns:
        建议的情感基调
    """
    scene_type = context.get("scene_type", "")
    tension_level = context.get("tension_level", 50)
    personality = speaker_profile.get("personality", "")

    if scene_type == "conflict" or tension_level >= 70:
        if "hot-tempered" in personality or "急躁" in personality:
            return EmotionalTone.ANGRY
        return EmotionalTone.FEARFUL
    elif scene_type == "romantic":
        return EmotionalTone.HAPPY
    elif tension_level <= 30:
        return EmotionalTone.NEUTRAL
    else:
        return EmotionalTone.NEUTRAL


def get_emotion_keywords(emotion: EmotionalTone) -> List[str]:
    """
    获取情感关键词

    Args:
        emotion: 情感基调

    Returns:
        该情感的关键词列表
    """
    return EMOTION_KEYWORDS.get(emotion, []).copy()


def get_all_emotion_keywords() -> Dict[EmotionalTone, List[str]]:
    """
    获取所有情感关键词

    Returns:
        所有情感的关键词字典
    """
    return EMOTION_KEYWORDS.copy()
