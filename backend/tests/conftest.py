import pytest
import asyncio
from pathlib import Path
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    # 清理所有待处理的任务
    try:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        # 等待所有任务完成
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    except Exception:
        pass
    finally:
        loop.close()


@pytest.fixture
def temp_db_path(tmp_path):
    """提供临时数据库路径"""
    return str(tmp_path / "test.db")
