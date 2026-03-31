from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class WorldState(BaseModel):
    """世界状态模型"""
    world_id: str = Field(..., description="世界唯一标识")
    era: str = Field(..., description="时代背景")
    location: Dict[str, str] = Field(..., description="地理位置")
    time_span: Dict[str, int] = Field(..., description="时间跨度")
    society_type: str = Field(..., description="社会类型")
    special_settings: List[str] = Field(default_factory=list, description="特殊设定")
    
    current_time: datetime = Field(..., description="当前时间")
    environment_state: Dict[str, Any] = Field(default_factory=dict, description="环境状态")
    social_events: List[Dict[str, Any]] = Field(default_factory=list, description="社会事件列表")
    
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "world_id": "world-001",
                "era": "现代都市",
                "location": {"province": "浙江", "city": "杭州"},
                "time_span": {"start": 1990, "end": 2025},
                "society_type": "平稳发展型",
                "special_settings": ["包含重大社会事件"],
                "current_time": "2024-01-01T00:00:00",
                "environment_state": {},
                "social_events": []
            }
        }
