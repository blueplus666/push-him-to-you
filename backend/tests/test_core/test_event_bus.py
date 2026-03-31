import pytest
import asyncio
from app.core.event_bus import EventBus, Event, EventType

@pytest.mark.asyncio
async def test_event_bus_publish_subscribe():
    """测试事件发布订阅"""
    bus = EventBus(persist_events=False)
    await bus.start()
    
    received_events = []
    
    async def handler(event: Event):
        received_events.append(event)
    
    bus.subscribe(EventType.SIMULATION_STARTED, handler)
    
    event = Event(
        event_type=EventType.SIMULATION_STARTED,
        source="test",
        data={"simulation_id": "test-001"}
    )
    
    await bus.publish(event)
    await asyncio.sleep(0.1)  # 等待事件处理
    
    assert len(received_events) == 1
    assert received_events[0].data["simulation_id"] == "test-001"
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_multiple_subscribers():
    """测试多个订阅者"""
    bus = EventBus(persist_events=False)
    await bus.start()
    
    results = []
    
    async def handler1(event: Event):
        results.append("handler1")
    
    async def handler2(event: Event):
        results.append("handler2")
    
    bus.subscribe(EventType.WORLD_CREATED, handler1)
    bus.subscribe(EventType.WORLD_CREATED, handler2)
    
    event = Event(
        event_type=EventType.WORLD_CREATED,
        source="test",
        data={"world_id": "world-001"}
    )
    
    await bus.publish(event)
    await asyncio.sleep(0.1)
    
    assert len(results) == 2
    assert "handler1" in results
    assert "handler2" in results
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_unsubscribe():
    """测试取消订阅"""
    bus = EventBus(persist_events=False)
    await bus.start()
    
    received_events = []
    
    async def handler(event: Event):
        received_events.append(event)
    
    bus.subscribe(EventType.CHARACTER_CREATED, handler)
    
    event1 = Event(
        event_type=EventType.CHARACTER_CREATED,
        source="test",
        data={"character_id": "char-001"}
    )
    
    await bus.publish(event1)
    await asyncio.sleep(0.1)
    
    assert len(received_events) == 1
    
    # 取消订阅
    bus.unsubscribe(EventType.CHARACTER_CREATED, handler)
    
    event2 = Event(
        event_type=EventType.CHARACTER_CREATED,
        source="test",
        data={"character_id": "char-002"}
    )
    
    await bus.publish(event2)
    await asyncio.sleep(0.1)
    
    # 应该还是1，因为已经取消订阅
    assert len(received_events) == 1
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_history():
    """测试事件历史记录"""
    bus = EventBus(persist_events=False)
    await bus.start()
    
    # 发布多个事件
    for i in range(5):
        event = Event(
            event_type=EventType.SIMULATION_STARTED,
            source="test",
            data={"index": i}
        )
        await bus.publish(event)
    
    await asyncio.sleep(0.1)
    
    # 获取事件历史
    history = bus.get_event_history(limit=10)
    assert len(history) == 5
    
    await bus.stop()
