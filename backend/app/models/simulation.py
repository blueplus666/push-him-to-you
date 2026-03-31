from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime
from enum import Enum


class SimulationStatus(str, Enum):
    """模拟状态枚举"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ERROR = "error"


class SimulationContext(BaseModel):
    """模拟上下文模型"""

    simulation_id: str = Field(..., description="模拟唯一标识")
    world_id: str = Field(..., description="所属世界ID")
    character_ids: List[str] = Field(default_factory=list, description="参与人物ID列表")

    status: SimulationStatus = Field(default=SimulationStatus.IDLE, description="模拟状态")
    current_time: datetime = Field(..., description="当前时间")
    current_age: float = Field(default=0.0, ge=0, le=120, description="当前年龄")

    total_events: int = Field(default=0, ge=0, description="总事件数")
    spark_moments_count: int = Field(default=0, ge=0, description="闪光时刻数")

    speed: float = Field(default=1.0, ge=0.1, le=10.0, description="模拟速度")

    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    model_config = ConfigDict(use_enum_values=True)
