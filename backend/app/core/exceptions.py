class PushHimToYouError(Exception):
    """基础异常类"""

    pass


class StateStoreError(PushHimToYouError):
    """状态存储异常"""

    pass


class WorldNotFoundError(StateStoreError):
    """世界未找到"""

    pass


class CharacterNotFoundError(StateStoreError):
    """人物未找到"""

    pass


class EventNotFoundError(StateStoreError):
    """事件未找到"""

    pass


class SimulationNotFoundError(StateStoreError):
    """模拟未找到"""

    pass
