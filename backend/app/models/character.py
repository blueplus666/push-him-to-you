# Character Data Models
"""Character 数据模型
包含人物的所有属性和行为
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime, date


class OCEANDimensions(BaseModel):
    """大五人格维度 (OCEAN)"""
    openness: float = Field(ge=0, le=100, description="开放性")
    conscientiousness: float = Field(ge=0, le=100, description="尽责性")
    extraversion: float = Field(ge=0, le=100, description="外向性")
    agreeableness: float = Field(ge=0, le=100, description="宜人性")
    neuroticism: float = Field(ge=0, le=100, description="神经质")
    model_config = ConfigDict(extra="allow")


class SubDimensions(BaseModel):
    """人格子维度"""
    imagination: float = Field(default=50, ge=0, le=100, description="想象力")
    aesthetics: float = Field(default=50, ge=0, le=100, description="审美")
    trust: float = Field(default=50, ge=0, le=100, description="信任")
    anxiety: float = Field(default=50, ge=0, le=100, description="焦虑")
    self_discipline: float = Field(default=50, ge=0, le=100, description="自律")
    assertiveness: float = Field(default=50, ge=0, le=100, description="自信")
    model_config = ConfigDict(extra="allow")


class Personality(BaseModel):
    """人格模型"""
    ocean: OCEANDimensions
    sub_dimensions: Optional[SubDimensions] = None
    model_config = ConfigDict(extra="allow")

    def get_personality_summary(self) -> str:
        """获取人格摘要"""
        summary_parts = []
        if self.ocean.openness >= 70:
            summary_parts.append("开放性高，富有想象力和创造力")
        elif self.ocean.openness >= 40:
            summary_parts.append("开放性中等，既务实又有一定想象力")
        else:
            summary_parts.append("开放性较低，更注重实际和传统")
        if self.ocean.conscientiousness >= 70:
            summary_parts.append("尽责性高，自律且有组织能力")
        elif self.ocean.conscientiousness >= 40:
            summary_parts.append("尽责性中等，有一定的自我管理能力")
        else:
            summary_parts.append("尽责性较低，较为随性")
        if self.ocean.extraversion >= 70:
            summary_parts.append("外向性高，善于社交和表达")
        elif self.ocean.extraversion >= 40:
            summary_parts.append("外向性中等，能在社交和独处间平衡")
        else:
            summary_parts.append("外向性较低，更享受独处时光")
        if self.ocean.agreeableness >= 70:
            summary_parts.append("宜人性高，富有同情心和合作精神")
        elif self.ocean.agreeableness >= 40:
            summary_parts.append("宜人性中等，能与他人和谐相处")
        else:
            summary_parts.append("宜人性较低，更注重竞争和自我利益")
        if self.ocean.neuroticism >= 70:
            summary_parts.append("神经质较高，情绪波动较大")
        elif self.ocean.neuroticism >= 40:
            summary_parts.append("神经质中等，情绪较为稳定")
        else:
            summary_parts.append("神经质较低，情绪非常稳定")
        return "；".join(summary_parts)


class FamilyBackground(BaseModel):
    """家庭背景"""
    father_occupation: str = Field(default="", description="父亲职业")
    mother_occupation: str = Field(default="", description="母亲职业")
    family_economic_status: str = Field(default="middle", description="家庭经济状况")
    family_atmosphere: str = Field(default="harmonious", description="家庭氛围")
    siblings: int = Field(default=0, ge=0, description="兄弟姐妹数量")
    birth_order: int = Field(default=1, ge=1, description="出生顺序")
    model_config = ConfigDict(extra="allow")


class EducationBackground(BaseModel):
    """教育背景"""
    highest_degree: str = Field(default="", description="最高学历")
    major: str = Field(default="", description="专业")
    school_tier: str = Field(default="", description="学校层次")
    academic_performance: str = Field(default="average", description="学业表现")
    model_config = ConfigDict(extra="allow")


class Background(BaseModel):
    """背景信息"""
    family: FamilyBackground
    education: Optional[EducationBackground] = None
    birth_place: Optional[Dict[str, str]] = None
    model_config = ConfigDict(extra="allow")


class CurrentState(BaseModel):
    """当前状态"""
    age: int = Field(ge=0, description="年龄")
    occupation: str = Field(default="", description="职业")
    income_level: int = Field(default=5, ge=1, le=10, description="收入等级")
    relationship_status: str = Field(default="single", description="感情状态")
    health_status: str = Field(default="good", description="健康状态")
    mental_state: str = Field(default="stable", description="心理状态")
    life_satisfaction: float = Field(default=50, ge=0, le=100, description="生活满意度")
    model_config = ConfigDict(extra="allow")

    def get_life_stage(self) -> str:
        """获取人生阶段"""
        if self.age < 12:
            return "儿童期"
        elif self.age < 18:
            return "青少年期"
        elif self.age < 35:
            return "青年期"
        elif self.age < 60:
            return "中年期"
        else:
            return "老年期"


class Needs(BaseModel):
    """需求层次（马斯洛需求层次理论）"""
    physiological: float = Field(default=50, ge=0, le=100, description="生理需求")
    safety: float = Field(default=50, ge=0, le=100, description="安全需求")
    belonging: float = Field(default=50, ge=0, le=100, description="归属需求")
    esteem: float = Field(default=50, ge=0, le=100, description="尊重需求")
    self_actualization: float = Field(default=50, ge=0, le=100, description="自我实现需求")
    model_config = ConfigDict(extra="allow")

    def get_dominant_need(self) -> str:
        """获取主导需求"""
        needs = {
            "生理": self.physiological,
            "安全": self.safety,
            "归属": self.belonging,
            "尊重": self.esteem,
            "自我实现": self.self_actualization
        }
        return max(needs, key=needs.get)


class Skills(BaseModel):
    """技能"""
    technical: List[str] = Field(default_factory=list, description="技术技能")
    social: List[str] = Field(default_factory=list, description="社交技能")
    creative: List[str] = Field(default_factory=list, description="创造技能")
    physical: List[str] = Field(default_factory=list, description="体能技能")
    model_config = ConfigDict(extra="allow")


class Values(BaseModel):
    """价值观"""
    core_values: List[str] = Field(default_factory=list, description="核心价值观")
    life_goal: str = Field(default="", description="人生目标")
    fear: str = Field(default="", description="恐惧")
    priorities: List[str] = Field(default_factory=list, description="优先级")
    model_config = ConfigDict(extra="allow")


class PersonalityChangeRecord(BaseModel):
    """人格变化记录"""
    record_id: str
    timestamp: datetime
    character_age: float
    trigger_event: str
    event_type: str
    event_intensity: float = Field(ge=1, le=10, description="事件强度")
    changes: Dict[str, float]
    coping_style: str = Field(default="neutral", description="应对方式")
    reasoning: str = Field(default="", description="推理过程")
    model_config = ConfigDict(extra="allow")


class Character(BaseModel):
    """人物模型"""
    character_id: str
    name: str
    gender: str
    birth_date: date
    personality: Personality
    background: Background
    current_state: CurrentState
    needs: Needs = Field(default_factory=Needs)
    skills: Skills = Field(default_factory=Skills)
    values: Values = Field(default_factory=Values)
    personality_history: List[PersonalityChangeRecord] = Field(default_factory=list)
    world_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(extra="allow")

    def get_personality_stability(self) -> float:
        """获取人格稳定性"""
        if len(self.personality_history) == 0:
            return 100.0
        total_intensity = sum(record.event_intensity for record in self.personality_history)
        change_count = len(self.personality_history)
        stability = max(0.0, 100.0 - (change_count * 2) - (total_intensity * 0.5))
        return stability

    def apply_personality_change(self, change: PersonalityChangeRecord) -> None:
        """应用人格变化"""
        for trait, delta in change.changes.items():
            if hasattr(self.personality.ocean, trait):
                current_value = getattr(self.personality.ocean, trait)
                new_value = max(0.0, min(100.0, current_value + delta))
                setattr(self.personality.ocean, trait, new_value)
        self.personality_history.append(change)
        self.updated_at = datetime.now()

    def to_summary(self) -> str:
        """生成人物摘要"""
        life_stage = self.current_state.get_life_stage()
        personality_summary = self.personality.get_personality_summary()
        summary = f"{self.name}，{self.gender}，{self.current_state.age}岁（{life_stage}），"
        summary += f"职业：{self.current_state.occupation}。"
        summary += f"人格特征：{personality_summary}"
        return summary
