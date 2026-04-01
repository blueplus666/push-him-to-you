"""
Narrative 数据模型
包含叙事结构、场景、幕、故事等相关模型
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class NarrativeStructureType(str, Enum):
    """叙事结构类型"""
    THREE_ACT = "three_act"
    HERO_JOURNEY = "hero_journey"
    FIVE_ACT = "five_act"
    CUSTOM = "custom"


class SceneType(str, Enum):
    """场景类型"""
    EXPOSITION = "exposition"
    RISING_ACTION = "rising_action"
    CLIMAX = "climax"
    FALLING_ACTION = "falling_action"
    RESOLUTION = "resolution"


class NarrativeTensionType(str, Enum):
    """叙事张力类型"""
    CONFLICT = "conflict"
    SUSPENSE = "suspense"
    EMOTIONAL = "emotional"
    PACING = "pacing"


class SceneStatus(str, Enum):
    """场景状态"""
    DRAFT = "draft"
    OUTLINE = "outline"
    DETAILED = "detailed"
    COMPLETE = "complete"


class SceneCharacter(BaseModel):
    """场景角色模型"""
    character_id: str
    role: str
    emotional_state: Optional[str] = None
    objective: Optional[str] = None
    model_config = ConfigDict(extra="allow")


class SceneEvent(BaseModel):
    """场景事件模型"""
    event_id: str
    description: str
    event_type: str
    intensity: float = Field(ge=1, le=10, default=5)
    consequences: List[str] = []
    model_config = ConfigDict(extra="allow")


class Scene(BaseModel):
    """场景模型"""
    scene_id: str
    scene_type: SceneType
    title: str
    description: str
    time: Optional[datetime] = None
    location: str = ""
    setting: Dict[str, Any] = {}
    characters: List[SceneCharacter] = []
    pov_character: Optional[str] = None
    events: List[SceneEvent] = []
    tension_level: float = Field(ge=0, le=100, default=50)
    emotional_tone: str = "neutral"
    pacing: str = "normal"
    word_count: int = Field(ge=0, default=0)
    status: SceneStatus = SceneStatus.DRAFT
    content: str = ""
    outline: str = ""
    metadata: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")


class Act(BaseModel):
    """幕模型"""
    act_id: str
    act_number: int
    title: str
    description: str = ""
    scenes: List[Scene] = []
    current_scene_index: int = 0
    act_tension: float = Field(ge=0, le=100, default=50)
    tension_arc: List[float] = []
    purpose: str = ""
    key_events: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(extra="allow")

    def get_current_scene(self) -> Optional[Scene]:
        """获取当前场景"""
        if 0 <= self.current_scene_index < len(self.scenes):
            return self.scenes[self.current_scene_index]
        return None

    def advance_scene(self) -> bool:
        """推进到下一个场景"""
        if self.current_scene_index < len(self.scenes) - 1:
            self.current_scene_index += 1
            self.updated_at = datetime.now()
            return True
        return False

    def calculate_act_tension(self) -> float:
        """计算幕的平均张力"""
        if not self.tension_arc:
            return 50.0
        return sum(self.tension_arc) / len(self.tension_arc)


class Story(BaseModel):
    """故事模型"""
    story_id: str
    world_id: str
    title: str
    description: str
    structure_type: NarrativeStructureType
    acts: List[Act] = []
    current_act_index: int = 0
    themes: List[str] = []
    central_conflict: Optional[str] = None
    narrative_arc: Dict[str, Any] = {}
    overall_tension: float = Field(ge=0, le=100, default=50)
    tension_history: List[float] = []
    timeline_start: Optional[datetime] = None
    timeline_end: Optional[datetime] = None
    status: str = "draft"
    word_count: int = Field(ge=0, default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(extra="allow")

    def get_current_act(self) -> Optional[Act]:
        """获取当前幕"""
        if 0 <= self.current_act_index < len(self.acts):
            return self.acts[self.current_act_index]
        return None

    def advance_act(self) -> bool:
        """推进到下一幕"""
        if self.current_act_index < len(self.acts) - 1:
            self.current_act_index += 1
            self.updated_at = datetime.now()
            return True
        return False

    def get_all_scenes(self) -> List[Scene]:
        """获取所有场景"""
        all_scenes = []
        for act in self.acts:
            all_scenes.extend(act.scenes)
        return all_scenes


class NarrativeReport(BaseModel):
    """叙事报告模型"""
    report_id: str
    story_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    structure_analysis: Dict[str, Any] = {}
    act_summaries: List[Dict[str, Any]] = []
    tension_analysis: Dict[str, Any] = {}
    tension_curve: List[float] = []
    pacing_analysis: Dict[str, Any] = {}
    pacing_recommendations: List[str] = []
    total_scenes: int = 0
    completed_scenes: int = 0
    total_word_count: int = 0
    narrative_health: float = Field(ge=0, le=100, default=50)
    recommendations: List[str] = []
    next_actions: List[str] = []
    model_config = ConfigDict(extra="allow")
