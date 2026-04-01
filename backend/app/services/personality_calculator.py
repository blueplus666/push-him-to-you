# PersonalityCalculator - 人格变化计算引擎
"""基于心理学公式计算人格变化"""
from typing import Dict, Any
from datetime import datetime
import uuid

from app.models.character import Character, PersonalityChangeRecord


class PersonalityCalculator:
    """人格变化计算器"""

    BASE_CHANGE_COEFFICIENT = 0.02

    TYPE_MATCH_MATRIX = {
        "positive_reward": {"openness": 0.3, "conscientiousness": 0.5, "extraversion": 0.4, "agreeableness": 0.3, "neuroticism": -0.3},
        "negative_stress": {"openness": -0.2, "conscientiousness": -0.1, "extraversion": -0.3, "agreeableness": -0.2, "neuroticism": 0.8},
        "social_positive": {"openness": 0.2, "conscientiousness": 0.1, "extraversion": 0.6, "agreeableness": 0.5, "neuroticism": -0.2},
        "achievement": {"openness": 0.2, "conscientiousness": 0.7, "extraversion": 0.3, "agreeableness": 0.1, "neuroticism": -0.4},
        "trauma": {"openness": -0.3, "conscientiousness": -0.2, "extraversion": -0.5, "agreeableness": -0.3, "neuroticism": 0.9},
        "growth": {"openness": 0.5, "conscientiousness": 0.3, "extraversion": 0.2, "agreeableness": 0.2, "neuroticism": -0.3},
        "neutral": {"openness": 0.0, "conscientiousness": 0.0, "extraversion": 0.0, "agreeableness": 0.0, "neuroticism": 0.0},
    }

    COPING_MODIFIERS = {"positive": 0.8, "neutral": 1.0, "negative": 1.3}

    def calculate_change(self, character: Character, event: Dict[str, Any], coping_style: str = "neutral") -> PersonalityChangeRecord:
        """计算人格变化
        公式: ΔP = α × E × T × R × (1 - S)
        """
        event_type = event.get("event_type", "neutral")
        event_intensity = event.get("intensity", 5.0)
        event_description = event.get("description", "")
        R = self._get_coping_modifier(coping_style)
        S = self._calculate_stability(character.current_state.age)
        changes = {}
        for dimension in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            T = self._get_type_match(dimension, event_type)
            current_value = getattr(character.personality.ocean, dimension)
            delta = self.BASE_CHANGE_COEFFICIENT * event_intensity * T * R * (1 - S)
            new_value = current_value + delta
            if new_value > 100:
                delta = 100 - current_value
            elif new_value < 0:
                delta = -current_value
            changes[dimension] = delta
        reasoning = self._generate_reasoning(character, event, changes)
        return PersonalityChangeRecord(
            record_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            character_age=float(character.current_state.age),
            trigger_event=event_description,
            event_type=event_type,
            event_intensity=event_intensity,
            changes=changes,
            coping_style=coping_style,
            reasoning=reasoning,
        )

    def _get_type_match(self, dimension: str, event_type: str) -> float:
        if event_type not in self.TYPE_MATCH_MATRIX:
            return 0.0
        return self.TYPE_MATCH_MATRIX[event_type].get(dimension, 0.0)

    def _get_coping_modifier(self, coping_style: str) -> float:
        return self.COPING_MODIFIERS.get(coping_style, 1.0)

    def _calculate_stability(self, age: int) -> float:
        if age < 20:
            return 0.2
        elif age < 30:
            return 0.3
        elif age < 40:
            return 0.4
        elif age < 50:
            return 0.5
        elif age < 60:
            return 0.6
        else:
            return 0.7

    def _generate_reasoning(self, character: Character, event: Dict[str, Any], changes: Dict[str, float]) -> str:
        event_description = event.get("description", "")
        event_type = event.get("event_type", "neutral")
        type_names = {"positive_reward": "正向奖励", "negative_stress": "负向压力", "social_positive": "积极社交", "achievement": "成就事件", "trauma": "创伤事件", "growth": "成长事件", "neutral": "中性事件"}
        reasoning_parts = [f"事件: {event_description}", f"事件类型: {type_names.get(event_type, '未知')}"]
        significant_changes = [(dim, change) for dim, change in changes.items() if abs(change) > 0.1]
        if significant_changes:
            change_desc = ", ".join([f"{dim}: {change:+.2f}" for dim, change in significant_changes])
            reasoning_parts.append(f"主要变化: {change_desc}")
        return " | ".join(reasoning_parts)
