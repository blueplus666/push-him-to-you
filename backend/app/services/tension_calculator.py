"""
张力计算器
用于戏剧张力管理

该模块提供了张力计算器，用于计算和预测戏剧张力。
"""
from typing import List, Dict, Any, Tuple
from app.models.fate import CausalEvent, FateThread, CausalChain


class TensionCalculator:
    """
    戏剧张力管理计算器
    
    用于计算事件、命运线和整体张力，预测张力弧线，并调整张力到目标范围。
    
    Attributes:
        TENSION_MIN: 最小张力阈值（默认40）
        TENSION_MAX: 最大张力阈值（默认70）
        tension_history: 张力历史记录
    """

    TENSION_MIN = 40  # 最小张力阈值
    TENSION_MAX = 70  # 最大张力阈值

    def __init__(self):
        """初始化张力计算器"""
        self.tension_history: List[float] = []

    def calculate_event_tension(
        self,
        event: CausalEvent,
        context: Dict[str, Any] = None
    ) -> float:
        """
        计算事件的张力贡献
        
        Args:
            event: 因果事件对象
            context: 上下文信息，可包含 multiplier 等参数
        
        Returns:
            事件的张力值（0-100）
        
        Examples:
            >>> event = CausalEvent(intensity=5.0, ...)
            >>> tension = calculator.calculate_event_tension(event)
            >>> print(tension)  # 25.0
        """
        base_tension = event.intensity * 5

        # 应用 context 中的倍数
        if context and "multiplier" in context:
            base_tension *= context["multiplier"]

        # TODO: 添加转折点和高潮事件的倍数逻辑
        # 目前 EventType 枚举没有 turning_point 和 climax 类型
        # 需要根据实际需求调整

        return min(100, base_tension)

    def calculate_thread_tension(self, thread: FateThread) -> float:
        """
        计算命运线的张力
        
        Args:
            thread: 命运线对象
        
        Returns:
            命运线的张力值（0-100），如果没有历史记录则返回50.0
        """
        if not thread.tension_arc:
            return 50.0
        return thread.tension_arc[-1] if thread.tension_arc else 50.0

    def calculate_overall_tension(
        self,
        threads: List[FateThread] = None,
        chain: CausalChain = None
    ) -> float:
        """
        计算整体张力
        
        综合考虑命运线和因果链的张力，计算整体张力值。
        
        Args:
            threads: 命运线列表
            chain: 因果链对象
        
        Returns:
            整体张力值（0-100），如果没有数据则返回50.0
        """
        tensions = []

        # 计算命运线的平均张力
        if threads:
            thread_tensions = [self.calculate_thread_tension(t) for t in threads]
            if thread_tensions:
                avg_tension = sum(thread_tensions) / len(thread_tensions)
                tensions.append(avg_tension)

        # 添加因果链张力
        if chain and chain.tension_history:
            chain_tension = chain.current_tension
            tensions.append(chain_tension)

        # 返回平均张力
        if tensions:
            avg_tension = sum(tensions) / len(tensions)
            return min(100, max(0, avg_tension))

        return 50.0

    def predict_tension_arc(
        self,
        thread: FateThread,
        steps: int = 5
    ) -> List[float]:
        """
        预测张力弧线
        
        根据命运线的趋势预测未来的张力变化。
        
        Args:
            thread: 命运线对象
            steps: 预测步数（默认5）
        
        Returns:
            预测的张力值列表
        
        Examples:
            >>> # 上升趋势
            >>> predictions = calculator.predict_tension_arc(thread, steps=5)
            >>> # 返回 [65.0, 70.0, 75.0, 80.0, 85.0]
        """
        if not thread.tension_arc:
            return [50.0] * steps

        last_tension = thread.tension_arc[-1]
        trend = thread.current_state.trend.value

        predictions = []
        current = last_tension

        for _ in range(steps):
            if trend == "rising":
                current = min(100, current + 5)
            elif trend == "falling":
                current = max(0, current - 5)
            # stable 趋势保持不变

            predictions.append(current)

        return predictions

    def adjust_tension(
        self,
        current_tension: float,
        target_range: Tuple[float, float] = None
    ) -> float:
        """
        调整张力到目标范围
        
        如果张力低于最小阈值，会调整到接近最小阈值。
        如果张力高于最大阈值，会调整到最大阈值。
        
        Args:
            current_tension: 当前张力值
            target_range: 目标范围（最小值，最大值），默认使用 TENSION_MIN 和 TENSION_MAX
        
        Returns:
            调整后的张力值
        
        Examples:
            >>> adjusted = calculator.adjust_tension(30.0)
            >>> print(adjusted)  # 45.0 (40 + (40 - 30) * 0.5)
        """
        if target_range is None:
            target_range = (self.TENSION_MIN, self.TENSION_MAX)

        min_tension, max_tension = target_range

        if current_tension < min_tension:
            return min_tension + (min_tension - current_tension) * 0.5
        elif current_tension > max_tension:
            return max_tension

        return current_tension
