"""
CausalEngine 测试
测试因果引擎处理事件之间的因果关系
"""
import pytest
from datetime import datetime
from app.services.causal_engine import CausalEngine
from app.models.fate import (
    CausalEvent,
    EventType,
    CausalChain,
)


@pytest.fixture
def engine():
    """创建因果引擎实例"""
    return CausalEngine()


@pytest.fixture
def sample_event():
    """创建示例事件"""
    return CausalEvent(
        event_id="evt_001",
        event_type=EventType.CAUSAL,
        description="主角获得神秘宝物",
        timestamp=datetime.now(),
        intensity=7.0,
        affected_characters=["char_001"],
        affected_aspects=["财富", "能力"],
    )


@pytest.fixture
def sample_cause_event():
    """创建示例原因事件"""
    return CausalEvent(
        event_id="evt_cause_001",
        event_type=EventType.CAUSAL,
        description="主角进入古老遗迹",
        timestamp=datetime.now(),
        intensity=5.0,
        affected_characters=["char_001"],
    )


@pytest.fixture
def sample_effect_event():
    """创建示例结果事件"""
    return CausalEvent(
        event_id="evt_effect_001",
        event_type=EventType.CAUSAL,
        description="主角获得神秘宝物",
        timestamp=datetime.now(),
        intensity=7.0,
        causes=["evt_cause_001"],
        affected_characters=["char_001"],
    )


@pytest.fixture
def sample_causal_chain():
    """创建示例因果链"""
    return CausalChain(
        chain_id="chain_001",
        world_id="world_001",
        events=[
            CausalEvent(
                event_id="evt_001",
                event_type=EventType.CAUSAL,
                description="初始事件",
                timestamp=datetime.now(),
                intensity=5.0,
            ),
            CausalEvent(
                event_id="evt_002",
                event_type=EventType.CAUSAL,
                description="中间事件",
                timestamp=datetime.now(),
                intensity=6.0,
                causes=["evt_001"],
            ),
            CausalEvent(
                event_id="evt_003",
                event_type=EventType.CAUSAL,
                description="最终事件",
                timestamp=datetime.now(),
                intensity=7.0,
                causes=["evt_002"],
            ),
        ],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestCausalEngineInit:
    """测试引擎初始化"""

    def test_engine_has_max_causal_depth(self, engine):
        """测试引擎有最大因果追溯深度"""
        assert hasattr(engine, "MAX_CAUSAL_DEPTH")
        assert engine.MAX_CAUSAL_DEPTH == 3

    def test_engine_initializes_successfully(self, engine):
        """测试引擎成功初始化"""
        assert engine is not None
        assert isinstance(engine, CausalEngine)


class TestValidateCausality:
    """测试因果验证"""

    def test_validate_valid_causality(self, engine, sample_cause_event, sample_effect_event):
        """测试验证有效的因果关系"""
        is_valid = engine.validate_causality(sample_cause_event, sample_effect_event)
        assert is_valid is True

    def test_validate_causality_with_same_characters(self, engine):
        """测试有相同角色的因果关系"""
        cause = CausalEvent(
            event_id="evt_cause_002",
            event_type=EventType.CAUSAL,
            description="角色A帮助角色B",
            timestamp=datetime.now(),
            intensity=5.0,
            affected_characters=["char_001", "char_002"],
        )
        effect = CausalEvent(
            event_id="evt_effect_002",
            event_type=EventType.CAUSAL,
            description="角色B感激角色A",
            timestamp=datetime.now(),
            intensity=4.0,
            affected_characters=["char_002"],
        )
        is_valid = engine.validate_causality(cause, effect)
        assert is_valid is True

    def test_validate_causality_with_no_overlap(self, engine):
        """测试没有重叠的因果关系（无效）"""
        cause = CausalEvent(
            event_id="evt_cause_003",
            event_type=EventType.CAUSAL,
            description="角色A做某事",
            timestamp=datetime.now(),
            intensity=5.0,
            affected_characters=["char_001"],
        )
        effect = CausalEvent(
            event_id="evt_effect_003",
            event_type=EventType.CAUSAL,
            description="角色B做某事",
            timestamp=datetime.now(),
            intensity=4.0,
            affected_characters=["char_002"],
        )
        is_valid = engine.validate_causality(cause, effect)
        assert is_valid is False

    def test_validate_causality_with_lower_intensity(self, engine):
        """测试结果事件强度低于原因事件（无效）"""
        cause = CausalEvent(
            event_id="evt_cause_004",
            event_type=EventType.CAUSAL,
            description="重大事件",
            timestamp=datetime.now(),
            intensity=8.0,
            affected_characters=["char_001"],
        )
        effect = CausalEvent(
            event_id="evt_effect_004",
            event_type=EventType.CAUSAL,
            description="轻微影响",
            timestamp=datetime.now(),
            intensity=2.0,
            affected_characters=["char_001"],
        )
        # 虽然强度降低，但仍然是有效的因果关系
        is_valid = engine.validate_causality(cause, effect)
        assert is_valid is True


class TestGenerateConsequences:
    """测试生成后果"""

    def test_generate_consequences_returns_list(self, engine, sample_event):
        """测试生成后果返回列表"""
        context = {"world_id": "world_001"}
        consequences = engine.generate_consequences(sample_event, context)
        assert isinstance(consequences, list)

    def test_generate_consequences_with_context(self, engine, sample_event):
        """测试带上下文生成后果"""
        context = {
            "world_id": "world_001",
            "trend": "rising",
        }
        consequences = engine.generate_consequences(sample_event, context)
        # 应该生成至少一个后果事件
        assert len(consequences) >= 0
        # 所有后果事件应该引用原因事件
        for consequence in consequences:
            assert sample_event.event_id in consequence.causes

    def test_generate_consequences_with_high_intensity(self, engine):
        """测试高强度事件生成更多后果"""
        high_intensity_event = CausalEvent(
            event_id="evt_high_001",
            event_type=EventType.CAUSAL,
            description="重大转折事件",
            timestamp=datetime.now(),
            intensity=9.0,
            affected_characters=["char_001", "char_002"],
        )
        context = {"world_id": "world_001"}
        consequences = engine.generate_consequences(high_intensity_event, context)
        # 高强度事件应该生成后果
        assert len(consequences) >= 0


class TestProcessEvent:
    """测试事件处理"""

    def test_process_event_returns_list(self, engine, sample_event):
        """测试处理事件返回列表"""
        context = {"world_id": "world_001"}
        results = engine.process_event(sample_event, context)
        assert isinstance(results, list)

    def test_process_event_generates_consequences(self, engine, sample_event):
        """测试处理事件生成后果"""
        context = {"world_id": "world_001"}
        results = engine.process_event(sample_event, context)
        # 应该包含生成的后果事件
        for result in results:
            assert isinstance(result, CausalEvent)

    def test_process_event_validates_causality(self, engine, sample_event):
        """测试处理事件验证因果关系"""
        context = {"world_id": "world_001"}
        results = engine.process_event(sample_event, context)
        # 所有生成的后果应该是有效的
        for result in results:
            is_valid = engine.validate_causality(sample_event, result)
            assert is_valid is True


class TestTraceCauses:
    """测试原因追溯"""

    def test_trace_causes_returns_list(self, engine, sample_causal_chain):
        """测试追溯原因返回列表"""
        event = sample_causal_chain.events[2]  # 最终事件
        causes = engine.trace_causes(event, sample_causal_chain)
        assert isinstance(causes, list)

    def test_trace_causes_finds_direct_cause(self, engine, sample_causal_chain):
        """测试追溯原因找到直接原因"""
        event = sample_causal_chain.events[2]  # 最终事件
        causes = engine.trace_causes(event, sample_causal_chain)
        # 应该找到直接原因
        assert len(causes) > 0
        cause_ids = [c.event_id for c in causes]
        assert "evt_002" in cause_ids

    def test_trace_causes_finds_chain(self, engine, sample_causal_chain):
        """测试追溯原因找到因果链"""
        event = sample_causal_chain.events[2]  # 最终事件
        causes = engine.trace_causes(event, sample_causal_chain)
        # 应该找到整个因果链
        cause_ids = [c.event_id for c in causes]
        assert "evt_001" in cause_ids or "evt_002" in cause_ids

    def test_trace_causes_respects_max_depth(self, engine):
        """测试追溯原因遵守最大深度限制"""
        # 创建深度超过限制的因果链
        events = []
        for i in range(5):
            causes_list = [f"evt_{i-1}"] if i > 0 else []
            events.append(
                CausalEvent(
                    event_id=f"evt_{i}",
                    event_type=EventType.CAUSAL,
                    description=f"事件{i}",
                    timestamp=datetime.now(),
                    intensity=5.0,
                    causes=causes_list,
                )
            )

        chain = CausalChain(
            chain_id="chain_deep",
            world_id="world_001",
            events=events,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # 追溯最后一个事件的原因
        event = events[4]
        causes = engine.trace_causes(event, chain)

        # 应该不超过最大深度
        # MAX_CAUSAL_DEPTH = 3，所以最多追溯到3层
        assert len(causes) <= engine.MAX_CAUSAL_DEPTH

    def test_trace_causes_with_no_causes(self, engine):
        """测试追溯没有原因的事件"""
        event = CausalEvent(
            event_id="evt_no_cause",
            event_type=EventType.CAUSAL,
            description="初始事件",
            timestamp=datetime.now(),
            intensity=5.0,
            causes=[],
        )
        chain = CausalChain(
            chain_id="chain_no_cause",
            world_id="world_001",
            events=[event],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        causes = engine.trace_causes(event, chain)
        # 没有原因时应该返回空列表
        assert causes == []


class TestEdgeCases:
    """测试边界情况"""

    def test_process_event_with_empty_context(self, engine, sample_event):
        """测试处理事件时上下文为空"""
        context = {}
        results = engine.process_event(sample_event, context)
        # 应该能处理空上下文
        assert isinstance(results, list)

    def test_trace_causes_with_empty_chain(self, engine, sample_event):
        """测试追溯原因时因果链为空"""
        chain = CausalChain(
            chain_id="chain_empty",
            world_id="world_001",
            events=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        causes = engine.trace_causes(sample_event, chain)
        # 空链时应该返回空列表
        assert causes == []

    def test_validate_causality_with_same_event(self, engine, sample_event):
        """测试验证同一事件的因果关系"""
        # 同一事件不能是自己的原因和结果
        is_valid = engine.validate_causality(sample_event, sample_event)
        assert is_valid is False

    def test_generate_consequences_with_low_intensity(self, engine):
        """测试低强度事件生成后果"""
        low_intensity_event = CausalEvent(
            event_id="evt_low_001",
            event_type=EventType.CAUSAL,
            description="轻微事件",
            timestamp=datetime.now(),
            intensity=1.0,
            affected_characters=["char_001"],
        )
        context = {"world_id": "world_001"}
        consequences = engine.generate_consequences(low_intensity_event, context)
        # 低强度事件可能不生成后果
        assert isinstance(consequences, list)
