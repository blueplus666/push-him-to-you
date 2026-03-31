from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """事件类型枚举"""

    LIFE_STAGE = "life_stage"
    CAUSAL = "causal"
    RANDOM = "random"
    CHARACTER_DRIVEN = "character_driven"
    RELATIONSHIP = "relationship"
    ENVIRONMENT = "environment"


class Event(BaseModel):
    """事件模型"""

    event_id: str = Field(..., description="事件唯一标识")
    simulation_id: str = Field(..., description="所属模拟ID")
    event_type: EventType = Field(..., description="事件类型")
    timestamp: datetime = Field(..., description="事件发生时间")
    age_at_event: float = Field(..., ge=0, le=120, description="事件发生时年龄")

    title: str = Field(..., description="事件标题")
    description: str = Field(..., description="事件描述")
    intensity: int = Field(..., ge=1, le=10, description="事件强度1-10")

    participants: List[str] = Field(default_factory=list, description="参与者ID列表")

    causes: List[str] = Field(default_factory=list, description="导致此事件的事件ID列表")
    effects: List[str] = Field(default_factory=list, description="此事件导致的事件ID列表")

    impact: Dict[str, Any] = Field(
        default_factory=dict,
        description="事件影响：personality_changes, relationship_changes, state_changes",
    )

    is_spark_moment: bool = Field(default=False, description="是否为闪光时刻")
    spark_score: Optional[float] = Field(None, ge=0, le=10, description="闪光时刻评分")

    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")

    model_config = ConfigDict(use_enum_values=True)
