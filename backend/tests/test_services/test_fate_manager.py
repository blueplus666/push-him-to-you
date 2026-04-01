"""
FateManager 测试
测试命运管理器的所有功能
"""
import pytest
from datetime import datetime, date
from app.services.fate_manager import FateManager
from app.models.fate import (
    FateThread,
    FateNode,
    FateState,
    FateNodeType,
    FateTrend,
    CausalEvent,
    EventType
)
from app.models.character import (
    Character,
    Personality,
    OCEANDimensions,
    Background,
    FamilyBackground,
    CurrentState
)


@pytest.fixture
def sample_character():
    """创建示例人物"""
    return Character(
        character_id="char-001",
        name="张三",
        gender="男",
        birth_date=date(1990, 1, 1),
        personality=Personality(
            ocean=OCEANDimensions(
                openness=70,
                conscientiousness=65,
                extraversion=55,
                agreeableness=60,
                neuroticism=40
            )
        ),
        background=Background(
            family=FamilyBackground(
                father_occupation="教师",
                mother_occupation="医生",
                family_economic_status="middle",
                family_atmosphere="harmonious"
            )
        ),
        current_state=CurrentState(
            age=30,
            occupation="工程师",
            income_level=6,
            relationship_status="single"
        ),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_fate_node():
    """创建示例命运节点"""
    return FateNode(
        node_id="node-001",
        node_type=FateNodeType.TURNING_POINT,
        trigger_event="职业转型",
        consequences=["收入增加", "压力增大"],
        affected_characters=["char-001"],
        narrative_weight=70
    )


@pytest.fixture
def sample_causal_event():
    """创建示例因果事件"""
    return CausalEvent(
        event_id="event-001",
        event_type=EventType.LIFE_STAGE,
        description="成功转型为技术主管",
        timestamp=datetime.now(),
        affected_characters=["char-001"],
        intensity=7
    )


class TestFateManagerInitialization:
    """测试FateManager初始化"""

    def test_init_creates_empty_threads_dict(self):
        """测试初始化创建空的命运线字典"""
        manager = FateManager()

        assert manager.threads == {}
        assert manager.MAX_THREADS == 3

    def test_max_threads_constant(self):
        """测试最大命运线交织数常量"""
        assert FateManager.MAX_THREADS == 3


class TestCreateFateThread:
    """测试创建命运线"""

    def test_create_fate_thread_for_character(self, sample_character):
        """测试为人物创建命运线"""
        manager = FateManager()
        world_id = "world-001"

        thread = manager.create_fate_thread(sample_character, world_id)

        assert thread.character_id == sample_character.character_id
        assert thread.world_id == world_id
        assert thread.thread_id is not None
        assert len(thread.nodes) == 0
        assert thread.current_node_index == 0
        assert thread.current_state is not None
        assert thread.current_state.character_id == sample_character.character_id
        assert len(thread.tension_arc) == 0

    def test_create_fate_thread_adds_to_threads_dict(self, sample_character):
        """测试创建的命运线被添加到字典中"""
        manager = FateManager()
        world_id = "world-001"

        thread = manager.create_fate_thread(sample_character, world_id)

        assert thread.thread_id in manager.threads
        assert manager.threads[thread.thread_id] == thread

    def test_create_fate_thread_initializes_state(self, sample_character):
        """测试创建命运线时初始化状态"""
        manager = FateManager()
        world_id = "world-001"

        thread = manager.create_fate_thread(sample_character, world_id)

        assert thread.current_state.fortune_level == 50.0
        assert thread.current_state.challenge_level == 50.0
        assert thread.current_state.growth_potential == 50.0
        assert thread.current_state.trend == FateTrend.STABLE


class TestAddFateNode:
    """测试添加命运节点"""

    def test_add_fate_node_to_thread(self, sample_character, sample_fate_node):
        """测试向命运线添加节点"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        manager.add_fate_node(thread, sample_fate_node)

        assert len(thread.nodes) == 1
        assert thread.nodes[0] == sample_fate_node

    def test_add_multiple_fate_nodes(self, sample_character, sample_fate_node):
        """测试添加多个命运节点"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        node1 = sample_fate_node
        node2 = FateNode(
            node_id="node-002",
            node_type=FateNodeType.CLIMAX,
            trigger_event="事业高峰",
            consequences=["名声大噪"],
            affected_characters=["char-001"],
            narrative_weight=90
        )

        manager.add_fate_node(thread, node1)
        manager.add_fate_node(thread, node2)

        assert len(thread.nodes) == 2
        assert thread.nodes[0] == node1
        assert thread.nodes[1] == node2

    def test_add_node_updates_thread_timestamp(self, sample_character, sample_fate_node):
        """测试添加节点更新时间戳"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")
        original_time = thread.updated_at

        manager.add_fate_node(thread, sample_fate_node)

        assert thread.updated_at >= original_time


class TestUpdateTensionArc:
    """测试更新张力弧线"""

    def test_update_tension_arc_adds_value(self, sample_character):
        """测试更新张力弧线添加新值"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        manager.update_tension_arc(thread, 60.0)

        assert len(thread.tension_arc) == 1
        assert thread.tension_arc[0] == 60.0

    def test_update_tension_arc_multiple_values(self, sample_character):
        """测试多次更新张力弧线"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        manager.update_tension_arc(thread, 50.0)
        manager.update_tension_arc(thread, 65.0)
        manager.update_tension_arc(thread, 80.0)

        assert len(thread.tension_arc) == 3
        assert thread.tension_arc == [50.0, 65.0, 80.0]

    def test_update_tension_arc_clamps_value(self, sample_character):
        """测试张力值被限制在有效范围内"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        manager.update_tension_arc(thread, 150.0)
        manager.update_tension_arc(thread, -10.0)

        assert thread.tension_arc[0] == 100.0
        assert thread.tension_arc[1] == 0.0

    def test_update_tension_arc_updates_timestamp(self, sample_character):
        """测试更新张力弧线更新时间戳"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")
        original_time = thread.updated_at

        manager.update_tension_arc(thread, 60.0)

        assert thread.updated_at >= original_time


class TestDetectIntersection:
    """测试检测命运线交织"""

    def test_detect_intersection_no_threads(self):
        """测试没有命运线时检测交织"""
        manager = FateManager()

        intersections = manager.detect_intersection([])

        assert intersections == []

    def test_detect_intersection_single_thread(self, sample_character):
        """测试单条命运线时检测交织"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        intersections = manager.detect_intersection([thread])

        assert intersections == []

    def test_detect_intersection_two_threads_same_world(self, sample_character):
        """测试同一世界的两条命运线检测交织"""
        manager = FateManager()

        character2 = Character(
            character_id="char-002",
            name="李四",
            gender="女",
            birth_date=date(1992, 5, 15),
            personality=Personality(
                ocean=OCEANDimensions(
                    openness=65,
                    conscientiousness=70,
                    extraversion=60,
                    agreeableness=55,
                    neuroticism=45
                )
            ),
            background=Background(
                family=FamilyBackground(
                    father_occupation="商人",
                    mother_occupation="教师"
                )
            ),
            current_state=CurrentState(
                age=28,
                occupation="设计师",
                income_level=5
            ),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        thread1 = manager.create_fate_thread(sample_character, "world-001")
        thread2 = manager.create_fate_thread(character2, "world-001")

        # 添加节点
        node1 = FateNode(
            node_id="node-001",
            node_type=FateNodeType.TURNING_POINT,
            trigger_event="职业转型",
            affected_characters=["char-001", "char-002"]
        )
        node2 = FateNode(
            node_id="node-002",
            node_type=FateNodeType.CLIMAX,
            trigger_event="合作项目",
            affected_characters=["char-001", "char-002"]
        )

        manager.add_fate_node(thread1, node1)
        manager.add_fate_node(thread2, node2)

        intersections = manager.detect_intersection([thread1, thread2])

        assert len(intersections) > 0
        assert "thread_ids" in intersections[0]
        assert "intersection_type" in intersections[0]

    def test_detect_intersection_different_worlds(self, sample_character):
        """测试不同世界的命运线不产生交织"""
        manager = FateManager()

        character2 = Character(
            character_id="char-002",
            name="李四",
            gender="女",
            birth_date=date(1992, 5, 15),
            personality=Personality(
                ocean=OCEANDimensions(
                    openness=65,
                    conscientiousness=70,
                    extraversion=60,
                    agreeableness=55,
                    neuroticism=45
                )
            ),
            background=Background(
                family=FamilyBackground()
            ),
            current_state=CurrentState(
                age=28,
                occupation="设计师"
            ),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        thread1 = manager.create_fate_thread(sample_character, "world-001")
        thread2 = manager.create_fate_thread(character2, "world-002")

        intersections = manager.detect_intersection([thread1, thread2])

        assert intersections == []

    def test_detect_intersection_max_threads_exceeded(self, sample_character):
        """测试超过最大交织数的命运线"""
        manager = FateManager()

        threads = []
        for i in range(4):
            char = Character(
                character_id=f"char-{i:03d}",
                name=f"人物{i}",
                gender="男",
                birth_date=date(1990, 1, 1),
                personality=Personality(
                    ocean=OCEANDimensions(
                        openness=50,
                        conscientiousness=50,
                        extraversion=50,
                        agreeableness=50,
                        neuroticism=50
                    )
                ),
                background=Background(family=FamilyBackground()),
                current_state=CurrentState(age=30, occupation="工程师"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            thread = manager.create_fate_thread(char, "world-001")
            threads.append(thread)

        intersections = manager.detect_intersection(threads)

        # 应该只返回最多3条线的交织
        if len(intersections) > 0:
            for intersection in intersections:
                assert len(intersection["thread_ids"]) <= manager.MAX_THREADS


class TestResolveNode:
    """测试解决命运节点"""

    def test_resolve_node_marks_as_resolved(self, sample_character, sample_fate_node, sample_causal_event):
        """测试解决节点标记为已解决"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")
        manager.add_fate_node(thread, sample_fate_node)

        manager.resolve_node(thread, "node-001", sample_causal_event)

        assert thread.nodes[0].is_resolved is True
        assert thread.nodes[0].resolution_event == sample_causal_event.event_id

    def test_resolve_node_updates_state(self, sample_character, sample_fate_node, sample_causal_event):
        """测试解决节点更新命运状态"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")
        manager.add_fate_node(thread, sample_fate_node)

        manager.resolve_node(thread, "node-001", sample_causal_event)

        # 解决节点后应该更新状态
        assert thread.current_state.is_at_turning_point is False

    def test_resolve_node_nonexistent_raises_error(self, sample_character, sample_causal_event):
        """测试解决不存在的节点抛出错误"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        with pytest.raises(ValueError, match="Node .* not found"):
            manager.resolve_node(thread, "nonexistent-node", sample_causal_event)

    def test_resolve_node_already_resolved_raises_error(self, sample_character, sample_causal_event):
        """测试解决已解决的节点抛出错误"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")

        node = FateNode(
            node_id="node-001",
            node_type=FateNodeType.TURNING_POINT,
            trigger_event="职业转型",
            is_resolved=True,
            resolution_event="event-000"
        )
        manager.add_fate_node(thread, node)

        with pytest.raises(ValueError, match="already resolved"):
            manager.resolve_node(thread, "node-001", sample_causal_event)

    def test_resolve_node_updates_timestamp(self, sample_character, sample_fate_node, sample_causal_event):
        """测试解决节点更新时间戳"""
        manager = FateManager()
        thread = manager.create_fate_thread(sample_character, "world-001")
        manager.add_fate_node(thread, sample_fate_node)
        original_time = thread.updated_at

        manager.resolve_node(thread, "node-001", sample_causal_event)

        assert thread.updated_at >= original_time
