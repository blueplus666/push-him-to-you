"""
测试 Fate 数据模型
TDD: RED 阶段 - 编写失败的测试
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.fate import (
    EventType,
    FateNodeType,
    FateTrend,
    CausalEvent,
    FateNode,
    FateState,
    FateThread,
    CausalChain,
    PredictedEvent,
    FateReport
)


class TestEventType:
    """测试事件类型枚举"""

    def test_event_type_values(self):
        """测试事件类型枚举值"""
        assert EventType.LIFE_STAGE == "life_stage"
        assert EventType.CAUSAL == "causal"
        assert EventType.RANDOM == "random"
        assert EventType.CHARACTER_DRIVEN == "character"
        assert EventType.RELATIONSHIP == "relationship"
        assert EventType.ENVIRONMENT == "environment"

    def test_event_type_string_conversion(self):
        """测试事件类型字符串转换"""
        assert EventType.LIFE_STAGE.value == "life_stage"
        assert EventType.CAUSAL.value == "causal"


class TestFateNodeType:
    """测试命运节点类型枚举"""

    def test_fate_node_type_values(self):
        """测试命运节点类型枚举值"""
        assert FateNodeType.TURNING_POINT == "turning_point"
        assert FateNodeType.CLIMAX == "climax"
        assert FateNodeType.RESOLUTION == "resolution"

    def test_fate_node_type_string_conversion(self):
        """测试命运节点类型字符串转换"""
        assert FateNodeType.TURNING_POINT.value == "turning_point"
        assert FateNodeType.CLIMAX.value == "climax"


class TestFateTrend:
    """测试命运趋势枚举"""

    def test_fate_trend_values(self):
        """测试命运趋势枚举值"""
        assert FateTrend.RISING == "rising"
        assert FateTrend.FALLING == "falling"
        assert FateTrend.STABLE == "stable"

    def test_fate_trend_string_conversion(self):
        """测试命运趋势字符串转换"""
        assert FateTrend.RISING.value == "rising"
        assert FateTrend.STABLE.value == "stable"


class TestCausalEvent:
    """测试因果事件模型"""

    def test_causal_event_creation(self):
        """测试因果事件创建"""
        event = CausalEvent(
            event_id="event-001",
            event_type=EventType.LIFE_STAGE,
            description="大学毕业",
            timestamp=datetime(2024, 6, 1, 10, 0, 0)
        )
        assert event.event_id == "event-001"
        assert event.event_type == EventType.LIFE_STAGE
        assert event.description == "大学毕业"
        assert event.timestamp == datetime(2024, 6, 1, 10, 0, 0)

    def test_causal_event_default_values(self):
        """测试因果事件默认值"""
        event = CausalEvent(
            event_id="event-002",
            event_type=EventType.CAUSAL,
            description="测试事件",
            timestamp=datetime.now()
        )
        assert event.causes == []
        assert event.effects == []
        assert event.affected_characters == []
        assert event.affected_aspects == []
        assert event.intensity == 5.0
        assert event.tension_contribution == 0.0
        assert event.world_id is None
        assert event.metadata == {}

    def test_causal_event_with_all_fields(self):
        """测试因果事件完整字段"""
        event = CausalEvent(
            event_id="event-003",
            event_type=EventType.CHARACTER_DRIVEN,
            description="重要决定",
            timestamp=datetime.now(),
            causes=["event-001", "event-002"],
            effects=["event-004"],
            affected_characters=["char-001", "char-002"],
            affected_aspects=["career", "relationship"],
            intensity=8.0,
            tension_contribution=75.0,
            world_id="world-001",
            metadata={"key": "value"}
        )
        assert len(event.causes) == 2
        assert len(event.effects) == 1
        assert len(event.affected_characters) == 2
        assert event.intensity == 8.0
        assert event.tension_contribution == 75.0
        assert event.world_id == "world-001"

    def test_causal_event_boundary_values(self):
        """测试因果事件边界值"""
        # 测试最小强度
        event_min = CausalEvent(
            event_id="event-004",
            event_type=EventType.RANDOM,
            description="测试",
            timestamp=datetime.now(),
            intensity=1.0
        )
        assert event_min.intensity == 1.0

        # 测试最大强度
        event_max = CausalEvent(
            event_id="event-005",
            event_type=EventType.RANDOM,
            description="测试",
            timestamp=datetime.now(),
            intensity=10.0
        )
        assert event_max.intensity == 10.0

        # 测试最小张力贡献
        event_tension_min = CausalEvent(
            event_id="event-006",
            event_type=EventType.RANDOM,
            description="测试",
            timestamp=datetime.now(),
            tension_contribution=0.0
        )
        assert event_tension_min.tension_contribution == 0.0

        # 测试最大张力贡献
        event_tension_max = CausalEvent(
            event_id="event-007",
            event_type=EventType.RANDOM,
            description="测试",
            timestamp=datetime.now(),
            tension_contribution=100.0
        )
        assert event_tension_max.tension_contribution == 100.0

    def test_causal_event_invalid_values(self):
        """测试因果事件无效值"""
        # 测试强度过小
        with pytest.raises(ValidationError):
            CausalEvent(
                event_id="event-008",
                event_type=EventType.RANDOM,
                description="测试",
                timestamp=datetime.now(),
                intensity=0.0
            )

        # 测试强度过大
        with pytest.raises(ValidationError):
            CausalEvent(
                event_id="event-009",
                event_type=EventType.RANDOM,
                description="测试",
                timestamp=datetime.now(),
                intensity=11.0
            )

        # 测试张力贡献过小
        with pytest.raises(ValidationError):
            CausalEvent(
                event_id="event-010",
                event_type=EventType.RANDOM,
                description="测试",
                timestamp=datetime.now(),
                tension_contribution=-1.0
            )

        # 测试张力贡献过大
        with pytest.raises(ValidationError):
            CausalEvent(
                event_id="event-011",
                event_type=EventType.RANDOM,
                description="测试",
                timestamp=datetime.now(),
                tension_contribution=101.0
            )


class TestFateNode:
    """测试命运节点模型"""

    def test_fate_node_creation(self):
        """测试命运节点创建"""
        node = FateNode(
            node_id="node-001",
            node_type=FateNodeType.TURNING_POINT,
            trigger_event="event-001"
        )
        assert node.node_id == "node-001"
        assert node.node_type == FateNodeType.TURNING_POINT
        assert node.trigger_event == "event-001"

    def test_fate_node_default_values(self):
        """测试命运节点默认值"""
        node = FateNode(
            node_id="node-002",
            node_type=FateNodeType.CLIMAX,
            trigger_event="event-002"
        )
        assert node.consequences == []
        assert node.affected_characters == []
        assert node.narrative_weight == 50.0
        assert node.is_resolved is False
        assert node.resolution_event is None

    def test_fate_node_with_all_fields(self):
        """测试命运节点完整字段"""
        node = FateNode(
            node_id="node-003",
            node_type=FateNodeType.RESOLUTION,
            trigger_event="event-003",
            consequences=["consequence-1", "consequence-2"],
            affected_characters=["char-001"],
            narrative_weight=80.0,
            is_resolved=True,
            resolution_event="event-004"
        )
        assert len(node.consequences) == 2
        assert len(node.affected_characters) == 1
        assert node.narrative_weight == 80.0
        assert node.is_resolved is True
        assert node.resolution_event == "event-004"

    def test_fate_node_boundary_values(self):
        """测试命运节点边界值"""
        # 测试最小叙事权重
        node_min = FateNode(
            node_id="node-004",
            node_type=FateNodeType.TURNING_POINT,
            trigger_event="event-004",
            narrative_weight=0.0
        )
        assert node_min.narrative_weight == 0.0

        # 测试最大叙事权重
        node_max = FateNode(
            node_id="node-005",
            node_type=FateNodeType.CLIMAX,
            trigger_event="event-005",
            narrative_weight=100.0
        )
        assert node_max.narrative_weight == 100.0

    def test_fate_node_invalid_values(self):
        """测试命运节点无效值"""
        # 测试叙事权重过小
        with pytest.raises(ValidationError):
            FateNode(
                node_id="node-006",
                node_type=FateNodeType.TURNING_POINT,
                trigger_event="event-006",
                narrative_weight=-1.0
            )

        # 测试叙事权重过大
        with pytest.raises(ValidationError):
            FateNode(
                node_id="node-007",
                node_type=FateNodeType.CLIMAX,
                trigger_event="event-007",
                narrative_weight=101.0
            )


class TestFateState:
    """测试命运状态模型"""

    def test_fate_state_creation(self):
        """测试命运状态创建"""
        state = FateState(
            state_id="state-001",
            character_id="char-001"
        )
        assert state.state_id == "state-001"
        assert state.character_id == "char-001"

    def test_fate_state_default_values(self):
        """测试命运状态默认值"""
        state = FateState(
            state_id="state-002",
            character_id="char-002"
        )
        assert state.fortune_level == 50.0
        assert state.challenge_level == 50.0
        assert state.growth_potential == 50.0
        assert state.trend == FateTrend.STABLE
        assert state.momentum == 0.0
        assert state.is_at_turning_point is False
        assert state.pending_resolution is None

    def test_fate_state_with_all_fields(self):
        """测试命运状态完整字段"""
        state = FateState(
            state_id="state-003",
            character_id="char-003",
            fortune_level=75.0,
            challenge_level=60.0,
            growth_potential=80.0,
            trend=FateTrend.RISING,
            momentum=0.5,
            is_at_turning_point=True,
            pending_resolution="node-001"
        )
        assert state.fortune_level == 75.0
        assert state.challenge_level == 60.0
        assert state.growth_potential == 80.0
        assert state.trend == FateTrend.RISING
        assert state.momentum == 0.5
        assert state.is_at_turning_point is True
        assert state.pending_resolution == "node-001"

    def test_fate_state_boundary_values(self):
        """测试命运状态边界值"""
        # 测试最小值
        state_min = FateState(
            state_id="state-004",
            character_id="char-004",
            fortune_level=0.0,
            challenge_level=0.0,
            growth_potential=0.0,
            momentum=-1.0
        )
        assert state_min.fortune_level == 0.0
        assert state_min.momentum == -1.0

        # 测试最大值
        state_max = FateState(
            state_id="state-005",
            character_id="char-005",
            fortune_level=100.0,
            challenge_level=100.0,
            growth_potential=100.0,
            momentum=1.0
        )
        assert state_max.fortune_level == 100.0
        assert state_max.momentum == 1.0

    def test_fate_state_invalid_values(self):
        """测试命运状态无效值"""
        # 测试运势等级过小
        with pytest.raises(ValidationError):
            FateState(
                state_id="state-006",
                character_id="char-006",
                fortune_level=-1.0
            )

        # 测试运势等级过大
        with pytest.raises(ValidationError):
            FateState(
                state_id="state-007",
                character_id="char-007",
                fortune_level=101.0
            )

        # 测试动量过小
        with pytest.raises(ValidationError):
            FateState(
                state_id="state-008",
                character_id="char-008",
                momentum=-2.0
            )

        # 测试动量过大
        with pytest.raises(ValidationError):
            FateState(
                state_id="state-009",
                character_id="char-009",
                momentum=2.0
            )


class TestFateThread:
    """测试命运线模型"""

    @pytest.fixture
    def sample_fate_state(self):
        """创建示例命运状态"""
        return FateState(
            state_id="state-001",
            character_id="char-001"
        )

    def test_fate_thread_creation(self, sample_fate_state):
        """测试命运线创建"""
        thread = FateThread(
            thread_id="thread-001",
            character_id="char-001",
            world_id="world-001",
            current_state=sample_fate_state,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        assert thread.thread_id == "thread-001"
        assert thread.character_id == "char-001"
        assert thread.world_id == "world-001"
        assert thread.current_state == sample_fate_state

    def test_fate_thread_default_values(self, sample_fate_state):
        """测试命运线默认值"""
        thread = FateThread(
            thread_id="thread-002",
            character_id="char-002",
            world_id="world-002",
            current_state=sample_fate_state,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert thread.nodes == []
        assert thread.current_node_index == 0
        assert thread.tension_arc == []
        assert thread.fate_endpoint is None
        assert thread.endpoint_type == "dynamic"

    def test_fate_thread_with_all_fields(self, sample_fate_state):
        """测试命运线完整字段"""
        node1 = FateNode(
            node_id="node-001",
            node_type=FateNodeType.TURNING_POINT,
            trigger_event="event-001"
        )
        node2 = FateNode(
            node_id="node-002",
            node_type=FateNodeType.CLIMAX,
            trigger_event="event-002"
        )

        thread = FateThread(
            thread_id="thread-003",
            character_id="char-003",
            world_id="world-003",
            nodes=[node1, node2],
            current_node_index=1,
            current_state=sample_fate_state,
            tension_arc=[50.0, 60.0, 75.0],
            fate_endpoint="endpoint-001",
            endpoint_type="predetermined",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 2, 12, 0, 0)
        )
        assert len(thread.nodes) == 2
        assert thread.current_node_index == 1
        assert len(thread.tension_arc) == 3
        assert thread.fate_endpoint == "endpoint-001"
        assert thread.endpoint_type == "predetermined"


class TestCausalChain:
    """测试因果链条模型"""

    def test_causal_chain_creation(self):
        """测试因果链条创建"""
        chain = CausalChain(
            chain_id="chain-001",
            world_id="world-001",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        assert chain.chain_id == "chain-001"
        assert chain.world_id == "world-001"

    def test_causal_chain_default_values(self):
        """测试因果链条默认值"""
        chain = CausalChain(
            chain_id="chain-002",
            world_id="world-002",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert chain.events == []
        assert chain.current_position == 0
        assert chain.current_tension == 50.0
        assert chain.tension_history == []

    def test_causal_chain_with_events(self):
        """测试带事件的因果链条"""
        event1 = CausalEvent(
            event_id="event-001",
            event_type=EventType.LIFE_STAGE,
            description="事件1",
            timestamp=datetime(2024, 1, 1, 10, 0, 0)
        )
        event2 = CausalEvent(
            event_id="event-002",
            event_type=EventType.CAUSAL,
            description="事件2",
            timestamp=datetime(2024, 1, 2, 10, 0, 0)
        )

        chain = CausalChain(
            chain_id="chain-003",
            world_id="world-003",
            events=[event1, event2],
            current_position=1,
            current_tension=65.0,
            tension_history=[50.0, 55.0, 65.0],
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 2, 12, 0, 0)
        )
        assert len(chain.events) == 2
        assert chain.current_position == 1
        assert chain.current_tension == 65.0
        assert len(chain.tension_history) == 3

    def test_causal_chain_boundary_values(self):
        """测试因果链条边界值"""
        # 测试最小张力
        chain_min = CausalChain(
            chain_id="chain-004",
            world_id="world-004",
            current_tension=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert chain_min.current_tension == 0.0

        # 测试最大张力
        chain_max = CausalChain(
            chain_id="chain-005",
            world_id="world-005",
            current_tension=100.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert chain_max.current_tension == 100.0

    def test_causal_chain_invalid_values(self):
        """测试因果链条无效值"""
        # 测试张力过小
        with pytest.raises(ValidationError):
            CausalChain(
                chain_id="chain-006",
                world_id="world-006",
                current_tension=-1.0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        # 测试张力过大
        with pytest.raises(ValidationError):
            CausalChain(
                chain_id="chain-007",
                world_id="world-007",
                current_tension=101.0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

    def test_get_current_event(self):
        """测试获取当前事件"""
        event1 = CausalEvent(
            event_id="event-001",
            event_type=EventType.LIFE_STAGE,
            description="事件1",
            timestamp=datetime(2024, 1, 1, 10, 0, 0)
        )
        event2 = CausalEvent(
            event_id="event-002",
            event_type=EventType.CAUSAL,
            description="事件2",
            timestamp=datetime(2024, 1, 2, 10, 0, 0)
        )

        # 测试有事件的情况
        chain = CausalChain(
            chain_id="chain-008",
            world_id="world-008",
            events=[event1, event2],
            current_position=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        current_event = chain.get_current_event()
        assert current_event is not None
        assert current_event.event_id == "event-001"

        # 测试改变当前位置
        chain.current_position = 1
        current_event = chain.get_current_event()
        assert current_event.event_id == "event-002"

    def test_get_current_event_empty(self):
        """测试空链条获取当前事件"""
        chain = CausalChain(
            chain_id="chain-009",
            world_id="world-009",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        current_event = chain.get_current_event()
        assert current_event is None

    def test_get_current_event_out_of_range(self):
        """测试位置超出范围"""
        event = CausalEvent(
            event_id="event-001",
            event_type=EventType.LIFE_STAGE,
            description="事件1",
            timestamp=datetime(2024, 1, 1, 10, 0, 0)
        )
        chain = CausalChain(
            chain_id="chain-010",
            world_id="world-010",
            events=[event],
            current_position=5,  # 超出范围
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        current_event = chain.get_current_event()
        assert current_event is None

    def test_advance(self):
        """测试推进链条"""
        event1 = CausalEvent(
            event_id="event-001",
            event_type=EventType.LIFE_STAGE,
            description="事件1",
            timestamp=datetime(2024, 1, 1, 10, 0, 0)
        )
        event2 = CausalEvent(
            event_id="event-002",
            event_type=EventType.CAUSAL,
            description="事件2",
            timestamp=datetime(2024, 1, 2, 10, 0, 0)
        )

        chain = CausalChain(
            chain_id="chain-011",
            world_id="world-011",
            events=[event1, event2],
            current_position=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # 推进一次
        result = chain.advance()
        assert result is True
        assert chain.current_position == 1

        # 再推进一次（已到最后）
        result = chain.advance()
        assert result is False
        assert chain.current_position == 1

    def test_advance_empty(self):
        """测试空链条推进"""
        chain = CausalChain(
            chain_id="chain-012",
            world_id="world-012",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        result = chain.advance()
        assert result is False


class TestPredictedEvent:
    """测试预测事件模型"""

    def test_predicted_event_creation(self):
        """测试预测事件创建"""
        event = PredictedEvent(
            event_description="即将发生的重大转折",
            probability=0.75
        )
        assert event.event_description == "即将发生的重大转折"
        assert event.probability == 0.75

    def test_predicted_event_default_values(self):
        """测试预测事件默认值"""
        event = PredictedEvent(
            event_description="测试事件",
            probability=0.5
        )
        assert event.estimated_time is None
        assert event.impact_characters == []

    def test_predicted_event_with_all_fields(self):
        """测试预测事件完整字段"""
        event = PredictedEvent(
            event_description="重大事件",
            probability=0.9,
            estimated_time=datetime(2024, 12, 31, 12, 0, 0),
            impact_characters=["char-001", "char-002"]
        )
        assert event.probability == 0.9
        assert event.estimated_time == datetime(2024, 12, 31, 12, 0, 0)
        assert len(event.impact_characters) == 2

    def test_predicted_event_boundary_values(self):
        """测试预测事件边界值"""
        # 测试最小概率
        event_min = PredictedEvent(
            event_description="测试",
            probability=0.0
        )
        assert event_min.probability == 0.0

        # 测试最大概率
        event_max = PredictedEvent(
            event_description="测试",
            probability=1.0
        )
        assert event_max.probability == 1.0

    def test_predicted_event_invalid_values(self):
        """测试预测事件无效值"""
        # 测试概率过小
        with pytest.raises(ValidationError):
            PredictedEvent(
                event_description="测试",
                probability=-0.1
            )

        # 测试概率过大
        with pytest.raises(ValidationError):
            PredictedEvent(
                event_description="测试",
                probability=1.1
            )


class TestFateReport:
    """测试命运报告模型"""

    def test_fate_report_creation(self):
        """测试命运报告创建"""
        report = FateReport(
            report_id="report-001",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            world_id="world-001"
        )
        assert report.report_id == "report-001"
        assert report.world_id == "world-001"

    def test_fate_report_default_values(self):
        """测试命运报告默认值"""
        report = FateReport(
            report_id="report-002",
            timestamp=datetime.now(),
            world_id="world-002"
        )
        assert report.overall_tension == 50.0
        assert report.active_threads == 0
        assert report.pending_nodes == 0
        assert report.character_states == {}
        assert report.active_chains == []
        assert report.upcoming_events == []
        assert report.recommended_actions == []

    def test_fate_report_with_all_fields(self):
        """测试命运报告完整字段"""
        state1 = FateState(
            state_id="state-001",
            character_id="char-001",
            fortune_level=75.0
        )
        predicted_event = PredictedEvent(
            event_description="即将发生的事件",
            probability=0.8
        )

        report = FateReport(
            report_id="report-003",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            world_id="world-003",
            overall_tension=65.0,
            active_threads=3,
            pending_nodes=5,
            character_states={"char-001": state1},
            active_chains=["chain-001", "chain-002"],
            upcoming_events=[predicted_event],
            recommended_actions=["增加冲突", "推进主线"]
        )
        assert report.overall_tension == 65.0
        assert report.active_threads == 3
        assert report.pending_nodes == 5
        assert len(report.character_states) == 1
        assert len(report.active_chains) == 2
        assert len(report.upcoming_events) == 1
        assert len(report.recommended_actions) == 2

    def test_fate_report_boundary_values(self):
        """测试命运报告边界值"""
        # 测试最小张力
        report_min = FateReport(
            report_id="report-004",
            timestamp=datetime.now(),
            world_id="world-004",
            overall_tension=0.0
        )
        assert report_min.overall_tension == 0.0

        # 测试最大张力
        report_max = FateReport(
            report_id="report-005",
            timestamp=datetime.now(),
            world_id="world-005",
            overall_tension=100.0
        )
        assert report_max.overall_tension == 100.0

    def test_fate_report_invalid_values(self):
        """测试命运报告无效值"""
        # 测试张力过小
        with pytest.raises(ValidationError):
            FateReport(
                report_id="report-006",
                timestamp=datetime.now(),
                world_id="world-006",
                overall_tension=-1.0
            )

        # 测试张力过大
        with pytest.raises(ValidationError):
            FateReport(
                report_id="report-007",
                timestamp=datetime.now(),
                world_id="world-007",
                overall_tension=101.0
            )
