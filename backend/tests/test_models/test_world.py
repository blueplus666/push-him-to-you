import pytest
from datetime import datetime
from app.models.world import (
    WorldState,
    WorldSetting,
    SocialStructure,
    CulturalFeature,
    EnvironmentDescription,
    ConflictSource
)


def test_world_setting_creation():
    """测试世界设定创建"""
    setting = WorldSetting(
        era="现代都市",
        location={"province": "浙江", "city": "杭州"},
        society_type="平稳发展型",
        special_settings=["包含重大社会事件"]
    )
    assert setting.era == "现代都市"
    assert setting.location["city"] == "杭州"


def test_social_structure_creation():
    """测试社会结构创建"""
    structure = SocialStructure(
        classes=["上层", "中层", "底层"],
        power_distribution={"政府": 40, "企业": 35, "民间": 25},
        social_mobility="中等流动性"
    )
    assert len(structure.classes) == 3


def test_cultural_feature_creation():
    """测试文化特征创建"""
    culture = CulturalFeature(
        core_values=["勤劳", "诚信", "创新"],
        customs=["春节团圆", "中秋赏月"],
        taboos=["不孝", "欺诈"]
    )
    assert "勤劳" in culture.core_values


def test_environment_description_creation():
    """测试环境描述创建"""
    env = EnvironmentDescription(
        natural_environment="江南水乡，四季分明",
        urban_environment="现代化都市，高楼林立",
        key_locations=["西湖", "钱塘江", "高新区"]
    )
    assert "西湖" in env.key_locations


def test_conflict_source_creation():
    """测试冲突源创建"""
    conflict = ConflictSource(
        social_contradictions=["贫富差距", "代际冲突"],
        resource_competition=["房价", "教育资源"],
        potential_events=["经济危机", "技术革命"]
    )
    assert len(conflict.social_contradictions) == 2


def test_world_state_creation():
    """测试世界状态创建"""
    world = WorldState(
        world_id="world-001",
        setting=WorldSetting(
            era="现代都市",
            location={"province": "浙江", "city": "杭州"},
            society_type="平稳发展型"
        ),
        social_structure=SocialStructure(
            classes=["上层", "中层", "底层"],
            power_distribution={"政府": 40, "企业": 35, "民间": 25}
        ),
        cultural_features=CulturalFeature(
            core_values=["勤劳", "诚信"]
        ),
        environment=EnvironmentDescription(
            natural_environment="江南水乡"
        ),
        conflict_sources=[
            ConflictSource(
                social_contradictions=["贫富差距"]
            )
        ]
    )
    assert world.world_id == "world-001"
    assert world.setting.era == "现代都市"
