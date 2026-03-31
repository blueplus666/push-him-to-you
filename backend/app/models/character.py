from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any, Optional
from datetime import datetime


class CharacterState(BaseModel):
    """人物状态模型"""

    character_id: str = Field(..., description="人物唯一标识")
    world_id: str = Field(..., description="所属世界ID")
    name: str = Field(..., description="姓名")
    gender: str = Field(..., description="性别")
    birth_date: datetime = Field(..., description="出生日期")
    age: float = Field(..., ge=0, le=120, description="年龄")

    personality: Dict[str, int] = Field(
        ...,
        description="大五人格维度：openness, conscientiousness, extraversion, agreeableness, neuroticism",
    )

    current_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="当前状态：occupation, income_level, relationship_status, health_status, mental_state, life_satisfaction",
    )

    needs: Dict[str, int] = Field(
        default_factory=dict,
        description="马斯洛需求层次：physiological, safety, belonging, esteem, self_actualization",
    )

    skills: Dict[str, List[str]] = Field(
        default_factory=dict, description="技能分类：technical, social, creative, physical"
    )

    values: Dict[str, Any] = Field(
        default_factory=dict, description="价值观：core_values, life_goal, fear"
    )

    relationship_graph_id: Optional[str] = Field(None, description="关系网络ID")
    event_timeline_id: Optional[str] = Field(None, description="事件时间线ID")

    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    @field_validator("personality")
    @classmethod
    def validate_personality(cls, v):
        """验证人格值范围"""
        for key, value in v.items():
            if not (0 <= value <= 100):
                raise ValueError(f"Personality value for {key} must be between 0 and 100")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "character_id": "char-001",
                "world_id": "world-001",
                "name": "李明",
                "gender": "male",
                "birth_date": "1990-03-15T00:00:00",
                "age": 25.0,
                "personality": {
                    "openness": 75,
                    "conscientiousness": 68,
                    "extraversion": 45,
                    "agreeableness": 82,
                    "neuroticism": 35,
                },
                "current_state": {"occupation": "软件工程师", "income_level": 4},
            }
        }
