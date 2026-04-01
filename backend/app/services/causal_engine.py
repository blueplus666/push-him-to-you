"""
因果引擎
处理事件之间的因果关系
"""
from typing import Dict, Any, List
from app.models.fate import CausalEvent, CausalChain


class CausalEngine:
    """因果引擎类"""

    MAX_CAUSAL_DEPTH = 3  # 最大因果追溯深度

    def process_event(
        self, event: CausalEvent, context: Dict[str, Any]
    ) -> List[CausalEvent]:
        """
        处理事件，生成后果事件

        Args:
            event: 要处理的因果事件
            context: 上下文信息，包含世界ID等

        Returns:
            生成的有效后果事件列表
        """
        # 生成后果事件
        consequences = self.generate_consequences(event, context)
        # 验证因果关系
        valid_consequences = [
            consequence
            for consequence in consequences
            if self.validate_causality(event, consequence)
        ]
        return valid_consequences

    def validate_causality(
        self, cause: CausalEvent, effect: CausalEvent
    ) -> bool:
        """
        验证因果关系是否合理

        Args:
            cause: 原因事件
            effect: 结果事件

        Returns:
            因果关系是否有效
        """
        # 同一事件不能是自己的原因和结果
        if cause.event_id == effect.event_id:
            return False

        # 检查是否有角色重叠
        cause_characters = set(cause.affected_characters)
        effect_characters = set(effect.affected_characters)

        # 如果没有角色重叠，因果关系无效
        if not cause_characters.intersection(effect_characters):
            return False

        # 如果有角色重叠，因果关系有效
        return True

    def generate_consequences(
        self, event: CausalEvent, context: Dict[str, Any]
    ) -> List[CausalEvent]:
        """
        生成事件的后果

        Args:
            event: 触发事件
            context: 上下文信息

        Returns:
            生成的后果事件列表
        """
        consequences = []

        # 根据事件强度决定是否生成后果
        # 高强度事件（强度>=7）生成后果
        if event.intensity >= 7.0:
            # 生成一个后果事件
            consequence = CausalEvent(
                event_id=f"{event.event_id}_consequence",
                event_type=event.event_type,
                description=f"{event.description}的后果",
                timestamp=event.timestamp,
                causes=[event.event_id],
                affected_characters=event.affected_characters,
                affected_aspects=event.affected_aspects,
                intensity=max(1.0, event.intensity - 1.0),  # 强度递减
            )
            consequences.append(consequence)

        return consequences

    def trace_causes(
        self,
        event: CausalEvent,
        chain: CausalChain,
        depth: int = 0,
    ) -> List[CausalEvent]:
        """
        追溯事件原因

        Args:
            event: 要追溯的事件
            chain: 因果链
            depth: 当前追溯深度

        Returns:
            原因事件列表（按追溯顺序）
        """
        # 如果超过最大深度，停止追溯
        if depth >= self.MAX_CAUSAL_DEPTH:
            return []

        # 如果事件没有原因，返回空列表
        if not event.causes:
            return []

        # 在因果链中查找原因事件
        causes = []
        for cause_id in event.causes:
            # 在链中查找原因事件
            for chain_event in chain.events:
                if chain_event.event_id == cause_id:
                    causes.append(chain_event)
                    # 递归追溯原因的原因
                    deeper_causes = self.trace_causes(
                        chain_event, chain, depth + 1
                    )
                    causes.extend(deeper_causes)
                    break

        return causes
