"""
Fate 数据模型
包含命运引擎的所有数据模型
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """事件类型枚举"""
    LIFE_STAGE = "life_stage"
    CAUSAL = "causal"
    RANDOM = "random"
    CHARACTER_DRIVEN = "character"
    RELATIONSHIP = "relationship"
    ENVIRONMENT = "environment"


class FateNodeType(str, Enum):
    """命运节点类型枚举"""
    TURNING_POINT = "turning_point"
    CLIMAX = "climax"
    RESOLUTION = "resolution"


class FateTrend(str, Enum):
    """命运趋势枚举"""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"


class CausalEvent(BaseModel):
    """因果事件模型"""
    event_id: str
    event_type: EventType
    description: str
    timestamp: datetime
    causes: List[str] = []
    effects: List[str] = []
    affected_characters: List[str] = []
    affected_aspects: List[str] = []
    intensity: float = Field(ge=1, le=10, default=5)
    tension_contribution: float = Field(ge=0, le=100, default=0)
    world_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

    model_config = ConfigDict(extra="allow")


class FateNode(BaseModel):
    """命运节点模型"""
    node_id: str
    node_type: FateNodeType
    trigger_event: str
    consequences: List[str] = []
    affected_characters: List[str] = []
    narrative_weight: float = Field(ge=0, le=100, default=50)
    is_resolved: bool = False
    resolution_event: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class FateState(BaseModel):
    """命运状态模型"""
    state_id: str
    character_id: str
    fortune_level: float = Field(ge=0, le=100, default=50)
    challenge_level: float = Field(ge=0, le=100, default=50)
    growth_potential: float = Field(ge=0, le=100, default=50)
    trend: FateTrend = FateTrend.STABLE
    momentum: float = Field(ge=-1, le=1, default=0)
    is_at_turning_point: bool = False
    pending_resolution: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class FateThread(BaseModel):
    """命运线模型"""
    thread_id: str
    character_id: str
    world_id: str
    nodes: List[FateNode] = []
    current_node_index: int = 0
    current_state: FateState
    tension_arc: List[float] = []
    fate_endpoint: Optional[str] = None
    endpoint_type: str = "dynamic"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="allow")


class CausalChain(BaseModel):
    """因果链条模型"""
    chain_id: str
    world_id: str
    events: List[CausalEvent] = []
    current_position: int = 0
    current_tension: float = Field(ge=0, le=100, default=50)
    tension_history: List[float] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="allow")

    def get_current_event(self) -> Optional[CausalEvent]:
        """获取当前事件"""
        if 0 <= self.current_position < len(self.events):
            return self.events[self.current_position]
        return None

    def advance(self) -> bool:
        """推进链条到下一个事件"""
        if self.current_position < len(self.events) - 1:
            self.current_position += 1
            return True
        return False


class PredictedEvent(BaseModel):
    """预测事件模型"""
    event_description: str
    probability: float = Field(ge=0, le=1)
    estimated_time: Optional[datetime] = None
    impact_characters: List[str] = []

    model_config = ConfigDict(extra="allow")


class FateReport(BaseModel):
    """命运报告模型"""
    report_id: str
    timestamp: datetime
    world_id: str
    overall_tension: float = Field(ge=0, le=100, default=50)
    active_threads: int = 0
    pending_nodes: int = 0
    character_states: Dict[str, FateState] = {}
    active_chains: List[str] = []
    upcoming_events: List[PredictedEvent] = []
    recommended_actions: List[str] = []

    model_config = ConfigDict(extra="allow")
