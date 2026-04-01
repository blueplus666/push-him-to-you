"""命运引擎提示词模板"""
from typing import Dict, Any


FATE_ENGINE_SYSTEM_PROMPT = """你是一位专业的命运编织者，精通因果逻辑和戏剧张力构建。

你的职责是：
1. 构建合理的因果链条
2. 管理命运节点和转折点
3. 协调多人物命运交织
4. 维持故事的戏剧张力

你的分析应该：
- 遵循因果一致性原则
- 确保命运可追溯
- 创造有意义的命运交织
- 维持适当的戏剧张力

请用中文回答，逻辑清晰，因果明确。"""


FATE_ADVANCE_PROMPT = """请分析并推进以下命运发展：

## 当前命运状态
{fate_state}

## 触发事件
{trigger_event}

## 世界背景
{world_context}

## 历史事件
{event_history}

## 当前戏剧张力
{current_tension}

请按以下结构输出命运推进分析：

## 因果链分析
（分析触发事件如何影响当前命运状态，构建合理的因果链条）n
## 命运节点更新
新增节点：[列举新的命运节点]
节点状态变化：[描述现有节点的状态变化]

## 转折点识别
是否产生转折点：[是/否]
转折点描述：[如有转折点，详细描述]
转折强度：[高/中/低]

## 人物命运交织
（分析该事件如何影响其他相关人物的命运）

## 戏剧张力变化
张力变化方向：[上升/下降/持平]
张力调整建议：[描述如何调整张力以维持故事吸引力]

## 未来可能性
短期走向：[描述近期可能的命运发展]
长期趋势：[描述长期命运走向]

请确保分析遵循因果一致性原则，命运发展合理且有戏剧性。"""


FATE_PREDICTION_PROMPT = """请基于以下信息预测人物命运走向：

## 人物状态
{character_state}

## 命运历史
{fate_history}

## 世界背景
{world_context}

请按以下结构输出命运预测：

## 当前命运阶段
（分析人物当前所处的命运阶段和特征）

## 关键影响因素
内在因素：[人物性格、能力、选择等]
外在因素：[环境、机遇、他人影响等]

## 短期预测（1-3个月）
可能事件：[列举可能发生的关键事件]
概率评估：[各事件发生的可能性]
影响分析：[各事件对命运的影响]

## 中期预测（3-12个月）
命运走向：[描述中期命运发展趋势]
关键节点：[可能出现的命运节点]
转折机会：[可能的转折点]

## 长期预测（1-5年）
人生轨迹：[描述长期人生发展轨迹]
终极目标：[人物可能达到的人生高度]
潜在风险：[可能面临的重大挑战]

## 命运建议
（基于人物性格和环境，给出合理的命运发展建议）

请确保预测基于因果逻辑，考虑人物性格和环境因素的相互作用。"""


class FateEnginePrompts:
    """Fate engine prompt manager"""

    def __init__(self):
        self.system_prompt = FATE_ENGINE_SYSTEM_PROMPT
        self.advance_prompt_template = FATE_ADVANCE_PROMPT
        self.prediction_prompt_template = FATE_PREDICTION_PROMPT

    def get_system_prompt(self) -> str:
        """Get system prompt"""
        return self.system_prompt

    def get_advance_prompt(
        self,
        fate_state: Dict[str, Any],
        trigger_event: Dict[str, Any],
        world_context: Dict[str, Any],
        event_history: str,
        current_tension: float
    ) -> str:
        """Get advance prompt

        Args:
            fate_state: 当前命运状态
            trigger_event: 触发事件
            world_context: 世界背景
            event_history: 历史事件
            current_tension: 当前戏剧张力

        Returns:
            str: 格式化后的推进提示词
        """
        fate_state_str = self._format_state(fate_state)
        trigger_event_str = self._format_event(trigger_event)
        world_context_str = self._format_context(world_context)

        return self.advance_prompt_template.format(
            fate_state=fate_state_str,
            trigger_event=trigger_event_str,
            world_context=world_context_str,
            event_history=event_history,
            current_tension=current_tension
        )

    def get_prediction_prompt(
        self,
        character_state: Dict[str, Any],
        fate_history: str,
        world_context: Dict[str, Any]
    ) -> str:
        """Get prediction prompt

        Args:
            character_state: 人物状态
            fate_history: 命运历史
            world_context: 世界背景

        Returns:
            str: 格式化后的预测提示词
        """
        character_state_str = self._format_state(character_state)
        world_context_str = self._format_context(world_context)

        return self.prediction_prompt_template.format(
            character_state=character_state_str,
            fate_history=fate_history,
            world_context=world_context_str
        )

    def _format_state(self, state: Dict[str, Any]) -> str:
        """Format state to string

        Args:
            state: 状态字典

        Returns:
            str: 格式化后的状态字符串
        """
        parts = []
        for key, value in state.items():
            if isinstance(value, dict):
                # 处理嵌套字典
                nested_parts = []
                for nested_key, nested_value in value.items():
                    nested_parts.append(f"  {nested_key}: {nested_value}")
                parts.append(f"{key}:\n" + "\n".join(nested_parts))
            elif isinstance(value, list):
                # 处理列表
                parts.append(f"{key}: {', '.join(str(v) for v in value)}")
            else:
                parts.append(f"{key}: {value}")
        return "\n".join(parts)

    def _format_event(self, event: Dict[str, Any]) -> str:
        """Format event to string

        Args:
            event: 事件字典

        Returns:
            str: 格式化后的事件字符串
        """
        parts = []
        for key, value in event.items():
            parts.append(f"{key}: {value}")
        return "\n".join(parts)

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context to string

        Args:
            context: 上下文字典

        Returns:
            str: 格式化后的上下文字符串
        """
        parts = []
        for key, value in context.items():
            parts.append(f"{key}: {value}")
        return "\n".join(parts)
