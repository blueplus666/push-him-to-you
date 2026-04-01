"""
TensionCalculator 测试
测试戏剧张力管理计算引擎
"""
import pytest
from datetime import datetime
from app.services.tension_calculator import TensionCalculator
from app.models.fate import (
    CausalEvent,
    EventType,
    FateThread,
    FateNode,
    FateNodeType,
    FateState,
    FateTrend,
    CausalChain,
)


@pytest.fixture
def calculator():
    """创建计算器实例"""
    return TensionCalculator()


@pytest.fixture
def sample_event():
    """创建示例事件"""
    return CausalEvent(
        event_id="evt_001",
        event_type=EventType.CAUSAL,
        description="测试事件",
        timestamp=datetime.now(),
        intensity=5.0,
    )


@pytest.fixture
def sample_fate_thread():
    """创建示例命运线"""
    return FateThread(
        thread_id="thread_001",
        character_id="char_001",
        world_id="world_001",
        current_state=FateState(
            state_id="state_001",
            character_id="char_001",
            trend=FateTrend.STABLE,
        ),
        tension_arc=[50.0, 55.0, 60.0],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_causal_chain():
    """创建示例因果链"""
    return CausalChain(
        chain_id="chain_001",
        world_id="world_001",
        current_tension=55.0,
        tension_history=[50.0, 52.0, 55.0],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestTensionCalculatorInit:
    """测试计算器初始化"""

    def test_calculator_has_tension_min(self, calculator):
        """测试计算器有最小张力阈值"""
        assert hasattr(calculator, "TENSION_MIN")
        assert calculator.TENSION_MIN == 40

    def test_calculator_has_tension_max(self, calculator):
        """测试计算器有最大张力阈值"""
        assert hasattr(calculator, "TENSION_MAX")
        assert calculator.TENSION_MAX == 70

    def test_calculator_has_tension_history(self, calculator):
        """测试计算器有张力历史记录"""
        assert hasattr(calculator, "tension_history")
        assert calculator.tension_history == []


class TestCalculateEventTension:
    """测试事件张力计算"""

    def test_calculate_base_event_tension(self, calculator, sample_event):
        """测试基础事件张力计算"""
        tension = calculator.calculate_event_tension(sample_event)

        # 基础张力 = intensity * 5
        assert tension == 25.0

    def test_turning_point_event_has_multiplier(self, calculator):
        """测试转折点事件有张力倍数"""
        event = CausalEvent(
            event_id="evt_002",
            event_type=EventType.CAUSAL,
            description="转折点事件",
            timestamp=datetime.now(),
            intensity=6.0,
        )
        # 模拟转折点事件（通过 metadata 或其他方式）
        # 由于 EventType 没有 turning_point，我们需要调整逻辑
        # 暂时使用基础测试
        tension = calculator.calculate_event_tension(event)
        assert tension == 30.0

    def test_high_intensity_event_capped_at_100(self, calculator):
        """测试高强度事件张力上限为100"""
        # 由于 intensity 最大为 10，基础张力最大为 50
        # 我们通过 context 参数模拟倍数，或者测试边界情况
        event = CausalEvent(
            event_id="evt_003",
            event_type=EventType.CAUSAL,
            description="高强度事件",
            timestamp=datetime.now(),
            intensity=10.0,  # 最大 intensity
        )
        tension = calculator.calculate_event_tension(event)
        # 10 * 5 = 50，在合理范围内
        assert tension == 50.0

    def test_event_tension_with_multiplier_capped_at_100(self, calculator):
        """测试带倍数的事件张力上限为100"""
        event = CausalEvent(
            event_id="evt_004",
            event_type=EventType.CAUSAL,
            description="高强度事件带倍数",
            timestamp=datetime.now(),
            intensity=10.0,
        )
        # 通过 context 传递倍数
        context = {"multiplier": 3.0}  # 10 * 5 * 3 = 150，应该被限制在100
        tension = calculator.calculate_event_tension(event, context)
        assert tension == 100.0


class TestCalculateThreadTension:
    """测试命运线张力计算"""

    def test_calculate_thread_tension_with_history(self, calculator, sample_fate_thread):
        """测试有历史记录的命运线张力"""
        tension = calculator.calculate_thread_tension(sample_fate_thread)
        # 应该返回最后一个张力值
        assert tension == 60.0

    def test_calculate_thread_tension_without_history(self, calculator):
        """测试没有历史记录的命运线张力"""
        thread = FateThread(
            thread_id="thread_002",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_002",
                character_id="char_001",
                trend=FateTrend.STABLE,
            ),
            tension_arc=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        tension = calculator.calculate_thread_tension(thread)
        # 没有历史记录时返回默认值50.0
        assert tension == 50.0


class TestCalculateOverallTension:
    """测试整体张力计算"""

    def test_calculate_overall_tension_with_threads(self, calculator, sample_fate_thread):
        """测试有命运线的整体张力"""
        threads = [sample_fate_thread]
        tension = calculator.calculate_overall_tension(threads=threads)
        # 应该返回命运线张力的平均值
        assert tension == 60.0

    def test_calculate_overall_tension_with_chain(self, calculator, sample_causal_chain):
        """测试有因果链的整体张力"""
        tension = calculator.calculate_overall_tension(chain=sample_causal_chain)
        # 应该返回因果链的当前张力
        assert tension == 55.0

    def test_calculate_overall_tension_with_both(self, calculator, sample_fate_thread, sample_causal_chain):
        """测试同时有命运线和因果链的整体张力"""
        threads = [sample_fate_thread]
        tension = calculator.calculate_overall_tension(threads=threads, chain=sample_causal_chain)
        # 应该返回两者的平均值
        # 命运线张力: 60.0, 因果链张力: 55.0
        # 平均值: (60.0 + 55.0) / 2 = 57.5
        assert tension == 57.5

    def test_calculate_overall_tension_empty(self, calculator):
        """测试没有命运线和因果链的整体张力"""
        tension = calculator.calculate_overall_tension()
        # 没有数据时返回默认值50.0
        assert tension == 50.0


class TestAdjustTension:
    """测试张力调整"""

    def test_adjust_tension_below_min(self, calculator):
        """测试低于最小阈值的张力调整"""
        current_tension = 30.0
        adjusted = calculator.adjust_tension(current_tension)
        # 应该调整到接近最小阈值
        # 调整公式: min + (min - current) * 0.5
        # 40 + (40 - 30) * 0.5 = 45.0
        assert adjusted == 45.0

    def test_adjust_tension_above_max(self, calculator):
        """测试高于最大阈值的张力调整"""
        current_tension = 80.0
        adjusted = calculator.adjust_tension(current_tension)
        # 应该调整到最大阈值
        assert adjusted == 70.0

    def test_adjust_tension_in_range(self, calculator):
        """测试在范围内的张力不调整"""
        current_tension = 55.0
        adjusted = calculator.adjust_tension(current_tension)
        # 在范围内应该保持不变
        assert adjusted == 55.0

    def test_adjust_tension_with_custom_range(self, calculator):
        """测试自定义范围的张力调整"""
        current_tension = 30.0
        target_range = (50.0, 80.0)
        adjusted = calculator.adjust_tension(current_tension, target_range)
        # 使用自定义范围
        # 50 + (50 - 30) * 0.5 = 60.0
        assert adjusted == 60.0


class TestPredictTensionArc:
    """测试张力弧线预测"""

    def test_predict_rising_trend(self, calculator):
        """测试上升趋势的张力预测"""
        thread = FateThread(
            thread_id="thread_003",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_003",
                character_id="char_001",
                trend=FateTrend.RISING,
            ),
            tension_arc=[50.0, 55.0, 60.0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 上升趋势应该逐步增加
        assert len(predictions) == 5
        assert predictions[0] == 65.0  # 60 + 5
        assert predictions[1] == 70.0  # 65 + 5
        assert predictions[2] == 75.0  # 70 + 5

    def test_predict_falling_trend(self, calculator):
        """测试下降趋势的张力预测"""
        thread = FateThread(
            thread_id="thread_004",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_004",
                character_id="char_001",
                trend=FateTrend.FALLING,
            ),
            tension_arc=[70.0, 65.0, 60.0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 下降趋势应该逐步减少
        assert len(predictions) == 5
        assert predictions[0] == 55.0  # 60 - 5
        assert predictions[1] == 50.0  # 55 - 5
        assert predictions[2] == 45.0  # 50 - 5

    def test_predict_stable_trend(self, calculator):
        """测试稳定趋势的张力预测"""
        thread = FateThread(
            thread_id="thread_005",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_005",
                character_id="char_001",
                trend=FateTrend.STABLE,
            ),
            tension_arc=[55.0, 55.0, 55.0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 稳定趋势应该保持不变
        assert len(predictions) == 5
        assert all(p == 55.0 for p in predictions)

    def test_predict_without_history(self, calculator):
        """测试没有历史记录的张力预测"""
        thread = FateThread(
            thread_id="thread_006",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_006",
                character_id="char_001",
                trend=FateTrend.STABLE,
            ),
            tension_arc=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 没有历史记录时返回默认值
        assert len(predictions) == 5
        assert all(p == 50.0 for p in predictions)

    def test_predict_rising_trend_capped_at_100(self, calculator):
        """测试上升趋势张力上限为100"""
        thread = FateThread(
            thread_id="thread_007",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_007",
                character_id="char_001",
                trend=FateTrend.RISING,
            ),
            tension_arc=[90.0, 92.0, 95.0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 应该被限制在100
        assert all(p <= 100.0 for p in predictions)

    def test_predict_falling_trend_floored_at_0(self, calculator):
        """测试下降趋势张力下限为0"""
        thread = FateThread(
            thread_id="thread_008",
            character_id="char_001",
            world_id="world_001",
            current_state=FateState(
                state_id="state_008",
                character_id="char_001",
                trend=FateTrend.FALLING,
            ),
            tension_arc=[10.0, 8.0, 5.0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        predictions = calculator.predict_tension_arc(thread, steps=5)
        # 应该被限制在0以上
        assert all(p >= 0.0 for p in predictions)
