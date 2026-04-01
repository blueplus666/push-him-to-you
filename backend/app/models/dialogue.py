"""
Dialogue 数据模型
包含对话类型、风格、情感基调、对话行、对话参与者等相关模型
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class DialogueType(str, Enum):
    """对话类型"""
    CASUAL = "casual"
    FORMAL = "formal"
    CONFLICT = "conflict"
    ROMANTIC = "romantic"
    PHILOSOPHICAL = "philosophical"


class DialogueStyle(str, Enum):
    """对话风格"""
    FORMAL = "formal"
    CASUAL = "casual"
    EMOTIONAL = "emotional"
    HUMOROUS = "humorous"
    SERIOUS = "serious"


class EmotionalTone(str, Enum):
    """情感基调"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"


class DialogueLine(BaseModel):
    """对话行模型"""
    line_id: str
    speaker_id: str
    content: str
    subtext: Optional[str] = None
    emotion: Optional[str] = None
    action: Optional[str] = None
    pause_before: Optional[float] = None
    pause_after: Optional[float] = None
    metadata: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")


class DialogueParticipant(BaseModel):
    """对话参与者模型"""
    character_id: str
    character_name: str
    role: str
    initial_emotion: Optional[str] = None
    final_emotion: Optional[str] = None
    lines_spoken: int = Field(ge=0, default=0)
    total_words: int = Field(ge=0, default=0)
    model_config = ConfigDict(extra="allow")


class Dialogue(BaseModel):
    """对话模型"""
    dialogue_id: str
    dialogue_type: DialogueType
    style: DialogueStyle
    participants: List[DialogueParticipant] = []
    lines: List[DialogueLine] = []
    scene_id: Optional[str] = None
    location: str = ""
    mood: str = ""
    tension_level: float = Field(ge=0, le=100, default=50)
    summary: str = ""
    key_points: List[str] = []
    total_lines: int = Field(ge=0, default=0)
    total_words: int = Field(ge=0, default=0)
    duration_estimate: float = Field(ge=0, default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(extra="allow")

    def add_line(self, line: DialogueLine) -> None:
        """添加对话行"""
        self.lines.append(line)
        self.total_lines = len(self.lines)
        self.updated_at = datetime.now()

    def get_speaker_lines(self, speaker_id: str) -> List[DialogueLine]:
        """获取指定说话者的所有对话行"""
        return [line for line in self.lines if line.speaker_id == speaker_id]

    def calculate_statistics(self) -> Dict[str, Any]:
        """计算对话统计数据"""
        total_words = sum(len(line.content) for line in self.lines)
        total_lines = len(self.lines)
        avg_words_per_line = total_words / total_lines if total_lines > 0 else 0.0

        return {
            "total_lines": total_lines,
            "total_words": total_words,
            "avg_words_per_line": avg_words_per_line
        }


class DialogueGenerationRequest(BaseModel):
    """对话生成请求模型"""
    request_id: str
    participants: List[str]
    dialogue_type: DialogueType
    style: DialogueStyle
    scene_context: Optional[str] = None
    topic: Optional[str] = None
    goal: Optional[str] = None
    min_lines: int = Field(ge=1, default=5)
    max_lines: int = Field(ge=1, default=20)
    include_actions: bool = False
    include_subtext: bool = False
    character_profiles: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")


class DialogueGenerationResult(BaseModel):
    """对话生成结果模型"""
    result_id: str
    request_id: str
    dialogue: Dialogue
    generation_method: str = "ai"
    quality_score: float = Field(ge=0, le=100, default=0.0)
    character_consistency: float = Field(ge=0, le=100, default=0.0)
    emotional_arc: List[str] = []
    improvements: List[str] = []
    alternative_versions: List[Dialogue] = []
    model_config = ConfigDict(extra="allow")
