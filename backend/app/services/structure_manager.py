"""
叙事结构管理器
管理叙事结构的创建、模板、验证
"""
from typing import Dict, Any
from datetime import datetime
import uuid

from app.models.narrative import (
    NarrativeStructureType,
    Story,
    Act,
)


class StructureManager:
    """叙事结构管理器"""

    STRUCTURE_TEMPLATES = {
        NarrativeStructureType.THREE_ACT: {
            "acts": [
                {"name": "铺垫", "function": "建立背景、人物和冲突"},
                {"name": "冲突", "function": "发展冲突,提升张力"},
                {"name": "解决", "function": "解决冲突,完成叙事"},
            ],
            "tension_pattern": [30, 50, 70, 60, 40],
        },
        NarrativeStructureType.HERO_JOURNEY: {
            "acts": [
                {"name": "平凡世界", "function": "建立英雄的日常生活"},
                {"name": "冒险召唤", "function": "英雄受到召唤"},
                {"name": "拒绝召唤", "function": "英雄犹豫"},
                {"name": "遇见导师", "function": "获得指导和帮助"},
                {"name": "跨越门槛", "function": "进入特殊世界"},
                {"name": "试炼之路", "function": "面对挑战和敌人"},
                {"name": "接近洞穴", "function": "准备面对最大挑战"},
                {"name": "磨难", "function": "面对死亡或最大恐惧"},
                {"name": "奖赏", "function": "获得胜利和奖赏"},
                {"name": "返回之路", "function": "返回平凡世界"},
                {"name": "复活", "function": "最后的考验"},
                {"name": "携宝归来", "function": "带着奖赏回归"},
            ],
            "tension_pattern": [20, 30, 35, 40, 50, 60, 70, 90, 80, 60, 50, 40],
        },
        NarrativeStructureType.FIVE_ACT: {
            "acts": [
                {"name": "铺垫", "function": "建立背景和人物"},
                {"name": "上升", "function": "发展冲突"},
                {"name": "高潮", "function": "冲突达到顶点"},
                {"name": "下降", "function": "冲突后果展现"},
                {"name": "结局", "function": "解决和收尾"},
            ],
            "tension_pattern": [30, 45, 60, 80, 65, 50, 35],
        },
    }

    def __init__(self):
        """初始化结构管理器"""
        pass

    def create_structure(
        self,
        structure_type: NarrativeStructureType,
        story_config: Dict[str, Any]
    ) -> Story:
        """创建叙事结构"""
        template = self.STRUCTURE_TEMPLATES.get(structure_type)
        if not template:
            raise ValueError(f"Unsupported structure type: {structure_type}")

        acts = []
        for i, act_template in enumerate(template["acts"]):
            act = Act(
                act_id=f"act-{uuid.uuid4().hex[:8]}",
                act_number=i + 1,
                title=act_template["name"],
                description=act_template["function"],
                tension_arc=[template["tension_pattern"][i]]
                if i < len(template["tension_pattern"])
                else [50.0],
            )
            acts.append(act)

        return Story(
            story_id=story_config.get("story_id", f"story-{uuid.uuid4().hex[:8]}"),
            world_id=story_config.get("world_id", "default-world"),
            title=story_config.get("title", "Untitled"),
            description=story_config.get("description", ""),
            structure_type=structure_type,
            acts=acts,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def get_act_template(
        self,
        structure_type: NarrativeStructureType,
        act_number: int
    ) -> Dict[str, Any]:
        """获取幕模板"""
        if structure_type not in self.STRUCTURE_TEMPLATES:
            return {}

        template = self.STRUCTURE_TEMPLATES[structure_type]
        acts = template.get("acts", [])

        if 1 <= act_number <= len(acts):
            return acts[act_number - 1]
        return {}

    def validate_structure(self, story: Story) -> bool:
        """验证叙事结构完整性"""
        if not story.acts:
            return False

        template = self.STRUCTURE_TEMPLATES.get(story.structure_type)
        if not template:
            return True

        expected_act_count = len(template["acts"])
        return len(story.acts) >= expected_act_count
