"""
Fate Manager - 命运管理器
管理命运线和节点
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.models.fate import (
    FateThread,
    FateNode,
    FateState,
    FateTrend,
    CausalEvent
)
from app.models.character import Character


class FateManager:
    """命运管理器"""

    MAX_THREADS = 3  # 最大命运线交织数

    def __init__(self):
        """初始化命运管理器"""
        self.threads: Dict[str, FateThread] = {}

    def create_fate_thread(
        self,
        character: Character,
        world_id: str
    ) -> FateThread:
        """
        为人物创建命运线

        Args:
            character: 人物对象
            world_id: 世界ID

        Returns:
            创建的命运线
        """
        # 生成命运线ID
        thread_id = f"thread-{character.character_id}-{datetime.now().timestamp()}"

        # 创建初始命运状态
        initial_state = FateState(
            state_id=f"state-{character.character_id}",
            character_id=character.character_id,
            fortune_level=50.0,
            challenge_level=50.0,
            growth_potential=50.0,
            trend=FateTrend.STABLE,
            momentum=0.0,
            is_at_turning_point=False
        )

        # 创建命运线
        thread = FateThread(
            thread_id=thread_id,
            character_id=character.character_id,
            world_id=world_id,
            nodes=[],
            current_node_index=0,
            current_state=initial_state,
            tension_arc=[],
            fate_endpoint=None,
            endpoint_type="dynamic",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # 添加到管理器
        self.threads[thread_id] = thread

        return thread

    def add_fate_node(
        self,
        thread: FateThread,
        node: FateNode
    ) -> None:
        """
        添加命运节点

        Args:
            thread: 命运线
            node: 命运节点
        """
        thread.nodes.append(node)
        thread.updated_at = datetime.now()

    def update_tension_arc(
        self,
        thread: FateThread,
        tension: float
    ) -> None:
        """
        更新张力弧线

        Args:
            thread: 命运线
            tension: 张力值（会被限制在0-100范围内）
        """
        # 限制张力值在有效范围内
        clamped_tension = max(0.0, min(100.0, tension))
        thread.tension_arc.append(clamped_tension)
        thread.updated_at = datetime.now()

    def detect_intersection(
        self,
        threads: List[FateThread]
    ) -> List[Dict[str, Any]]:
        """
        检测命运线交织点

        Args:
            threads: 命运线列表

        Returns:
            交织点列表，每个交织点包含thread_ids和intersection_type
        """
        if len(threads) < 2:
            return []

        intersections = []

        # 按世界分组
        world_threads: Dict[str, List[FateThread]] = {}
        for thread in threads:
            if thread.world_id not in world_threads:
                world_threads[thread.world_id] = []
            world_threads[thread.world_id].append(thread)

        # 检测每个世界内的交织
        for world_id, world_thread_list in world_threads.items():
            if len(world_thread_list) < 2:
                continue

            # 检查节点中是否有共同影响的人物
            for i in range(len(world_thread_list)):
                for j in range(i + 1, len(world_thread_list)):
                    thread1 = world_thread_list[i]
                    thread2 = world_thread_list[j]

                    # 检查是否有共同的受影响人物
                    common_characters = set()
                    for node in thread1.nodes:
                        for char_id in node.affected_characters:
                            for node2 in thread2.nodes:
                                if char_id in node2.affected_characters:
                                    common_characters.add(char_id)

                    if common_characters:
                        intersections.append({
                            "thread_ids": [thread1.thread_id, thread2.thread_id],
                            "intersection_type": "character_overlap",
                            "common_characters": list(common_characters),
                            "world_id": world_id
                        })

        # 限制交织数不超过MAX_THREADS
        if len(intersections) > 0:
            # 只保留涉及最多MAX_THREADS条线的交织
            filtered_intersections = []
            for intersection in intersections:
                if len(intersection["thread_ids"]) <= self.MAX_THREADS:
                    filtered_intersections.append(intersection)
            return filtered_intersections

        return intersections

    def resolve_node(
        self,
        thread: FateThread,
        node_id: str,
        resolution_event: CausalEvent
    ) -> None:
        """
        解决命运节点

        Args:
            thread: 命运线
            node_id: 节点ID
            resolution_event: 解决事件

        Raises:
            ValueError: 如果节点不存在或已解决
        """
        # 查找节点
        node = None
        for n in thread.nodes:
            if n.node_id == node_id:
                node = n
                break

        if node is None:
            raise ValueError(f"Node {node_id} not found in thread {thread.thread_id}")

        if node.is_resolved:
            raise ValueError(f"Node {node_id} is already resolved")

        # 标记为已解决
        node.is_resolved = True
        node.resolution_event = resolution_event.event_id

        # 更新命运状态
        thread.current_state.is_at_turning_point = False
        thread.updated_at = datetime.now()
