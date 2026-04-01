from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional
from datetime import datetime


class WorldSetting(BaseModel):
    """世界基础设定"""
    era: str = Field(..., description="时代背景")
    location: Dict[str, str] = Field(..., description="地理位置")
    society_type: str = Field(..., description="社会类型")
    special_settings: List[str] = Field(default_factory=list, description="特殊设定")
    time_span: Dict[str, int] = Field(
        default_factory=lambda: {"start": 1990, "end": 2025},
        description="时间跨度"
    )

    model_config = ConfigDict(extra="allow")


class SocialStructure(BaseModel):
    """社会结构"""
    classes: List[str] = Field(default_factory=list, description="社会阶层")
    power_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="权力分布（百分比）"
    )
    social_mobility: str = Field(default="中等流动性", description="社会流动性")

    model_config = ConfigDict(extra="allow")


class CulturalFeature(BaseModel):
    """文化特征"""
    core_values: List[str] = Field(default_factory=list, description="核心价值观")
    customs: List[str] = Field(default_factory=list, description="习俗")
    taboos: List[str] = Field(default_factory=list, description="禁忌")
    religion: Optional[str] = Field(None, description="主要宗教")

    model_config = ConfigDict(extra="allow")


class EnvironmentDescription(BaseModel):
    """环境描述"""
    natural_environment: str = Field(default="", description="自然环境")
    urban_environment: str = Field(default="", description="城市环境")
    key_locations: List[str] = Field(default_factory=list, description="关键地点")
    climate: Optional[str] = Field(None, description="气候特征")

    model_config = ConfigDict(extra="allow")


class ConflictSource(BaseModel):
    """冲突源"""
    social_contradictions: List[str] = Field(default_factory=list, description="社会矛盾")
    resource_competition: List[str] = Field(default_factory=list, description="资源争夺")
    potential_events: List[str] = Field(default_factory=list, description="潜在事件")

    model_config = ConfigDict(extra="allow")


class WorldState(BaseModel):
    """世界状态模型"""
    world_id: str = Field(..., description="世界唯一标识")
    setting: WorldSetting = Field(..., description="世界设定")
    social_structure: Optional[SocialStructure] = Field(None, description="社会结构")
    cultural_features: Optional[CulturalFeature] = Field(None, description="文化特征")
    environment: Optional[EnvironmentDescription] = Field(None, description="环境描述")
    conflict_sources: List[ConflictSource] = Field(
        default_factory=list,
        description="冲突源列表"
    )

    current_time: datetime = Field(
        default_factory=datetime.now,
        description="当前时间"
    )
    environment_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="环境状态"
    )
    social_events: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="社会事件列表"
    )

    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "world_id": "world-001",
                "setting": {
                    "era": "现代都市",
                    "location": {"province": "浙江", "city": "杭州"},
                    "society_type": "平稳发展型"
                },
                "social_structure": {
                    "classes": ["上层", "中层", "底层"],
                    "power_distribution": {"政府": 40, "企业": 35, "民间": 25}
                }
            }
        }
    )

    def update_time(self, new_time: datetime) -> None:
        """更新当前时间"""
        self.current_time = new_time
        self.updated_at = datetime.now()

    def add_social_event(self, event: Dict[str, Any]) -> None:
        """添加社会事件"""
        self.social_events.append(event)
        self.updated_at = datetime.now()
