import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from enum import Enum

from app.core.state_store import StateStore
from app.core.event_bus import EventBus, Event, EventType
from app.models.world import WorldState
from app.models.character import CharacterState
from app.models.simulation import SimulationContext, SimulationStatus

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    """主协调器 - 管理整个模拟流程"""

    def __init__(self, state_store: StateStore, event_bus: EventBus):
        self.state_store = state_store
        self.event_bus = event_bus

        # 模拟状态
        self.current_simulation_id: Optional[str] = None
        self.simulation_status: SimulationStatus = SimulationStatus.IDLE

        # 任务队列
        self.task_queue: asyncio.Queue = asyncio.Queue()

        # 性能监控
        self.metrics = {
            'events_processed': 0,
            'agents_invoked': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

    async def create_simulation(
        self,
        world_config: Dict[str, Any],
        character_configs: List[Dict[str, Any]]
    ) -> str:
        """创建新的模拟"""
        simulation_id = str(uuid.uuid4())

        # 创建世界状态
        world_id = str(uuid.uuid4())
        world_state = WorldState(
            world_id=world_id,
            era=world_config.get("era", "现代都市"),
            location=world_config.get("location", {"province": "浙江", "city": "杭州"}),
            time_span=world_config.get("time_span", {"start": 1990, "end": 2025}),
            society_type=world_config.get("society_type", "平稳发展型"),
            special_settings=world_config.get("special_settings", []),
            current_time=datetime.now(),
            environment_state={},
            social_events=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await self.state_store.create_world(world_state)

        # 创建人物状态
        character_ids = []
        for char_config in character_configs:
            character_id = str(uuid.uuid4())
            character_state = CharacterState(
                character_id=character_id,
                world_id=world_id,
                name=char_config.get("name", "未命名"),
                gender=char_config.get("gender", "male"),
                birth_date=char_config.get("birth_date", datetime.now()),
                age=char_config.get("age", 0.0),
                personality=char_config.get("personality", {}),
                current_state=char_config.get("current_state", {}),
                needs=char_config.get("needs", {}),
                skills=char_config.get("skills", {}),
                values=char_config.get("values", {}),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            await self.state_store.create_character(character_state)
            character_ids.append(character_id)

        # 创建模拟上下文
        simulation_context = SimulationContext(
            simulation_id=simulation_id,
            world_id=world_id,
            character_ids=character_ids,
            status=SimulationStatus.IDLE.value,
            current_time=datetime.now(),
            current_age=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await self.state_store.create_simulation(simulation_context)

        # 发布事件
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_CREATED,
            source="orchestrator",
            data={
                "simulation_id": simulation_id,
                "world_id": world_id,
                "character_ids": character_ids
            }
        ))

        logger.info(f"Simulation created: {simulation_id}")
        return simulation_id

    async def start_simulation(self, simulation_id: str):
        """启动模拟"""
        # 获取模拟上下文
        simulation = await self.state_store.get_simulation(simulation_id)
        if not simulation:
            raise ValueError(f"Simulation not found: {simulation_id}")

        # 更新状态
        self.current_simulation_id = simulation_id
        self.simulation_status = SimulationStatus.RUNNING
        self.metrics['start_time'] = datetime.now()

        # 更新数据库
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.RUNNING.value}
        )

        # 发布启动事件
        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_STARTED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))

        logger.info(f"Simulation started: {simulation_id}")

    async def pause_simulation(self, simulation_id: str):
        """暂停模拟"""
        self.simulation_status = SimulationStatus.PAUSED
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.PAUSED.value}
        )

        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_PAUSED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))

        logger.info(f"Simulation paused: {simulation_id}")

    async def resume_simulation(self, simulation_id: str):
        """恢复模拟"""
        self.simulation_status = SimulationStatus.RUNNING
        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.RUNNING.value}
        )

        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_RESUMED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))

        logger.info(f"Simulation resumed: {simulation_id}")

    async def stop_simulation(self, simulation_id: str):
        """停止模拟"""
        self.simulation_status = SimulationStatus.STOPPED
        self.metrics['end_time'] = datetime.now()

        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.STOPPED.value}
        )

        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_STOPPED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))

        logger.info(f"Simulation stopped: {simulation_id}")

    async def complete_simulation(self, simulation_id: str):
        """完成模拟"""
        self.simulation_status = SimulationStatus.COMPLETED
        self.metrics['end_time'] = datetime.now()

        await self.state_store.update_simulation(
            simulation_id,
            {"status": SimulationStatus.COMPLETED.value}
        )

        await self.event_bus.publish(Event(
            event_type=EventType.SIMULATION_COMPLETED,
            source="orchestrator",
            data={"simulation_id": simulation_id}
        ))

        logger.info(f"Simulation completed: {simulation_id}")
