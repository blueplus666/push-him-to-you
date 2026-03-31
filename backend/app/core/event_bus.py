import asyncio
import inspect
from typing import Dict, List, Callable, Any, Optional
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
import logging
import uuid

logger = logging.getLogger(__name__)


def _get_event_loop():
    """安全获取事件循环"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


class EventType(str, Enum):
    """系统事件类型枚举"""

    # 系统级事件
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"

    # 模拟生命周期事件
    SIMULATION_CREATED = "simulation.created"
    SIMULATION_STARTED = "simulation.started"
    SIMULATION_PAUSED = "simulation.paused"
    SIMULATION_RESUMED = "simulation.resumed"
    SIMULATION_STOPPED = "simulation.stopped"
    SIMULATION_COMPLETED = "simulation.completed"

    # 世界事件
    WORLD_CREATED = "world.created"
    WORLD_UPDATED = "world.updated"
    ENVIRONMENT_CHANGED = "environment.changed"
    SOCIAL_EVENT_OCCURRED = "social_event.occurred"

    # 人物事件
    CHARACTER_CREATED = "character.created"
    CHARACTER_UPDATED = "character.updated"
    CHARACTER_REACTION_COMPUTED = "character.reaction_computed"

    # 命运引擎事件
    EVENTS_GENERATED = "fate.events_generated"
    EVENT_SELECTED = "fate.event_selected"
    CAUSAL_CHAIN_UPDATED = "fate.causal_chain_updated"

    # 关系事件
    RELATIONSHIP_ESTABLISHED = "relationship.established"
    RELATIONSHIP_UPDATED = "relationship.updated"
    RELATIONSHIP_ENDED = "relationship.ended"

    # 闪光时刻事件
    SPARK_DETECTED = "spark.detected"
    SPARK_RECORDED = "spark.recorded"

    # 叙事事件
    NARRATIVE_GENERATED = "narrative.generated"
    NARRATIVE_EXPORTED = "narrative.exported"

    # 状态变更事件
    STATE_CHANGED = "state.changed"
    ERROR_OCCURRED = "error.occurred"


class Event(BaseModel):
    """事件基类"""

    model_config = ConfigDict(use_enum_values=True)

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str  # 事件来源（Agent ID或系统组件）
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EventBus:
    """事件总线 - 实现发布/订阅模式"""

    def __init__(self, persist_events: bool = True, log_file: str = "logs/events.log"):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: List[Event] = []
        self.persist_events = persist_events
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # 事件队列（用于异步处理）
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False

    async def start(self):
        """启动事件总线"""
        self._running = True
        asyncio.create_task(self._process_events())
        logger.info("Event Bus started")

    async def stop(self):
        """停止事件总线"""
        self._running = False
        logger.info("Event Bus stopped")

    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event: {event_type}")

    async def publish(self, event: Event):
        """发布事件（异步）"""
        await self.event_queue.put(event)

    async def _process_events(self):
        """处理事件队列"""
        while self._running:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self._dispatch_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}", exc_info=True)

    async def _dispatch_event(self, event: Event):
        """分发事件到订阅者"""
        logger.debug(f"Dispatching event: {event.event_type}")

        # 记录事件历史
        self.event_history.append(event)
        if self.persist_events:
            self._persist_event(event)

        # 获取订阅者
        callbacks = self.subscribers.get(event.event_type, [])

        # 并行调用所有订阅者
        tasks = []
        for callback in callbacks:
            try:
                if inspect.iscoroutinefunction(callback):
                    tasks.append(callback(event))
                else:
                    # 如果是同步函数，在线程池中执行
                    tasks.append(_get_event_loop().run_in_executor(None, callback, event))
            except Exception as e:
                logger.error(f"Error creating task for callback: {e}", exc_info=True)

        # 等待所有订阅者处理完成
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _persist_event(self, event: Event):
        """持久化事件到日志文件"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.model_dump(), default=str, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")

    def get_event_history(
        self,
        event_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Event]:
        """获取事件历史"""
        events = self.event_history

        # 过滤
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]

        # 限制数量
        return events[-limit:]
