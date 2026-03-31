from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import sqlite3
import json
import asyncio
from pathlib import Path
import logging

from app.models.world import WorldState
from app.models.character import CharacterState
from app.models.event import Event
from app.models.simulation import SimulationContext

logger = logging.getLogger(__name__)


def _get_event_loop():
    """安全获取事件循环"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


class StateStore(ABC):
    """状态存储抽象接口"""

    # ========== World State ==========
    @abstractmethod
    async def create_world(self, world_state: WorldState) -> str:
        """创建世界状态"""
        pass

    @abstractmethod
    async def get_world(self, world_id: str) -> Optional[WorldState]:
        """获取世界状态"""
        pass

    @abstractmethod
    async def update_world(self, world_id: str, updates: Dict[str, Any]) -> bool:
        """更新世界状态"""
        pass

    @abstractmethod
    async def delete_world(self, world_id: str) -> bool:
        """删除世界状态"""
        pass

    # ========== Character State ==========
    @abstractmethod
    async def create_character(self, character_state: CharacterState) -> str:
        """创建人物状态"""
        pass

    @abstractmethod
    async def get_character(self, character_id: str) -> Optional[CharacterState]:
        """获取人物状态"""
        pass

    @abstractmethod
    async def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """更新人物状态"""
        pass

    @abstractmethod
    async def delete_character(self, character_id: str) -> bool:
        """删除人物状态"""
        pass

    @abstractmethod
    async def list_characters(self, world_id: str) -> List[CharacterState]:
        """列出世界中的所有人物"""
        pass

    # ========== Event ==========
    @abstractmethod
    async def create_event(self, event: Event) -> str:
        """创建事件"""
        pass

    @abstractmethod
    async def get_event(self, event_id: str) -> Optional[Event]:
        """获取事件"""
        pass

    @abstractmethod
    async def list_events(
        self,
        simulation_id: str,
        character_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Event]:
        """列出事件（支持多种过滤条件）"""
        pass

    # ========== Simulation Context ==========
    @abstractmethod
    async def create_simulation(self, simulation_context: SimulationContext) -> str:
        """创建模拟上下文"""
        pass

    @abstractmethod
    async def get_simulation(self, simulation_id: str) -> Optional[SimulationContext]:
        """获取模拟上下文"""
        pass

    @abstractmethod
    async def update_simulation(self, simulation_id: str, updates: Dict[str, Any]) -> bool:
        """更新模拟上下文"""
        pass

    @abstractmethod
    async def delete_simulation(self, simulation_id: str) -> bool:
        """删除模拟上下文"""
        pass


class SQLiteStateStore(StateStore):
    """基于SQLite的状态存储实现"""

    def __init__(self, db_path: str = "data/db/push_him_to_you.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # 对于内存数据库，保持持久连接
        self._memory_conn = None
        if str(self.db_path) == ":memory:":
            self._memory_conn = sqlite3.connect(":memory:", check_same_thread=False)

        self._init_db()

    def _get_connection(self):
        """获取数据库连接"""
        if self._memory_conn:
            return self._memory_conn
        return sqlite3.connect(self.db_path)

    def _close_connection(self, conn):
        """关闭数据库连接（如果不是内存数据库）"""
        if not self._memory_conn:
            conn.close()

    def _init_db(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 创建世界状态表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS world_states (
                world_id TEXT PRIMARY KEY,
                era TEXT NOT NULL,
                location TEXT NOT NULL,
                time_span TEXT NOT NULL,
                society_type TEXT NOT NULL,
                special_settings TEXT NOT NULL,
                current_time TEXT NOT NULL,
                environment_state TEXT NOT NULL,
                social_events TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        # 创建人物状态表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS character_states (
                character_id TEXT PRIMARY KEY,
                world_id TEXT NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                age REAL NOT NULL,
                personality TEXT NOT NULL,
                current_state TEXT NOT NULL,
                needs TEXT NOT NULL,
                skills TEXT NOT NULL,
                "values" TEXT NOT NULL,
                relationship_graph_id TEXT,
                event_timeline_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (world_id) REFERENCES world_states(world_id)
            )
        """
        )

        # 创建事件表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                simulation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                age_at_event REAL NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                intensity INTEGER NOT NULL,
                participants TEXT NOT NULL,
                causes TEXT NOT NULL,
                effects TEXT NOT NULL,
                impact TEXT NOT NULL,
                is_spark_moment INTEGER NOT NULL DEFAULT 0,
                spark_score REAL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """
        )

        # 创建模拟上下文表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS simulation_contexts (
                simulation_id TEXT PRIMARY KEY,
                world_id TEXT NOT NULL,
                character_ids TEXT NOT NULL,
                status TEXT NOT NULL,
                current_time TEXT NOT NULL,
                current_age REAL NOT NULL,
                total_events INTEGER NOT NULL DEFAULT 0,
                spark_moments_count INTEGER NOT NULL DEFAULT 0,
                speed REAL NOT NULL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (world_id) REFERENCES world_states(world_id)
            )
        """
        )

        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_simulation ON events(simulation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_characters_world ON character_states(world_id)"
        )

        conn.commit()

        # 如果不是内存数据库，关闭连接
        if not self._memory_conn:
            conn.close()

        logger.info(f"Database initialized at {self.db_path}")

    # ========== World State Implementation ==========
    async def create_world(self, world_state: WorldState) -> str:
        """创建世界状态"""

        def _create():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO world_states VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    world_state.world_id,
                    world_state.era,
                    json.dumps(world_state.location, ensure_ascii=False),
                    json.dumps(world_state.time_span),
                    world_state.society_type,
                    json.dumps(world_state.special_settings, ensure_ascii=False),
                    world_state.current_time.isoformat(),
                    json.dumps(world_state.environment_state, ensure_ascii=False),
                    json.dumps(world_state.social_events, ensure_ascii=False),
                    world_state.created_at.isoformat(),
                    world_state.updated_at.isoformat(),
                ),
            )
            conn.commit()
            if not self._memory_conn:
                conn.close()
            return world_state.world_id

        return await _get_event_loop().run_in_executor(None, _create)

    async def get_world(self, world_id: str) -> Optional[WorldState]:
        """获取世界状态"""

        def _get():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM world_states WHERE world_id = ?", (world_id,))
            row = cursor.fetchone()
            result = None
            if row:
                result = WorldState(
                    world_id=row[0],
                    era=row[1],
                    location=json.loads(row[2]),
                    time_span=json.loads(row[3]),
                    society_type=row[4],
                    special_settings=json.loads(row[5]),
                    current_time=datetime.fromisoformat(row[6]),
                    environment_state=json.loads(row[7]),
                    social_events=json.loads(row[8]),
                    created_at=datetime.fromisoformat(row[9]),
                    updated_at=datetime.fromisoformat(row[10]),
                )
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _get)

    async def update_world(self, world_id: str, updates: Dict[str, Any]) -> bool:
        """更新世界状态"""

        def _update():
            conn = self._get_connection()
            cursor = conn.cursor()

            # 构建UPDATE语句
            set_clauses = []
            values = []
            for key, value in updates.items():
                if key in [
                    "location",
                    "time_span",
                    "special_settings",
                    "environment_state",
                    "social_events",
                ]:
                    set_clauses.append(f"{key} = ?")
                    values.append(json.dumps(value, ensure_ascii=False))
                elif key == "current_time":
                    set_clauses.append(f"{key} = ?")
                    values.append(value.isoformat())
                else:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)

            # 添加updated_at
            set_clauses.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(world_id)

            query = f"UPDATE world_states SET {', '.join(set_clauses)} WHERE world_id = ?"
            cursor.execute(query, values)
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _update)

    async def delete_world(self, world_id: str) -> bool:
        """删除世界状态"""

        def _delete():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM world_states WHERE world_id = ?", (world_id,))
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _delete)

    # ========== Character State Implementation ==========
    async def create_character(self, character_state: CharacterState) -> str:
        """创建人物状态"""

        def _create():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO character_states VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    character_state.character_id,
                    character_state.world_id,
                    character_state.name,
                    character_state.gender,
                    character_state.birth_date.isoformat(),
                    character_state.age,
                    json.dumps(character_state.personality, ensure_ascii=False),
                    json.dumps(character_state.current_state, ensure_ascii=False),
                    json.dumps(character_state.needs, ensure_ascii=False),
                    json.dumps(character_state.skills, ensure_ascii=False),
                    json.dumps(character_state.values, ensure_ascii=False),
                    character_state.relationship_graph_id,
                    character_state.event_timeline_id,
                    character_state.created_at.isoformat(),
                    character_state.updated_at.isoformat(),
                ),
            )
            conn.commit()
            self._close_connection(conn)
            return character_state.character_id

        return await _get_event_loop().run_in_executor(None, _create)

    async def get_character(self, character_id: str) -> Optional[CharacterState]:
        """获取人物状态"""

        def _get():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM character_states WHERE character_id = ?", (character_id,))
            row = cursor.fetchone()
            result = None
            if row:
                result = CharacterState(
                    character_id=row[0],
                    world_id=row[1],
                    name=row[2],
                    gender=row[3],
                    birth_date=datetime.fromisoformat(row[4]),
                    age=row[5],
                    personality=json.loads(row[6]),
                    current_state=json.loads(row[7]),
                    needs=json.loads(row[8]),
                    skills=json.loads(row[9]),
                    values=json.loads(row[10]),
                    relationship_graph_id=row[11],
                    event_timeline_id=row[12],
                    created_at=datetime.fromisoformat(row[13]),
                    updated_at=datetime.fromisoformat(row[14]),
                )
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _get)

    async def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """更新人物状态"""

        def _update():
            conn = self._get_connection()
            cursor = conn.cursor()

            set_clauses = []
            values = []
            for key, value in updates.items():
                if key in ["personality", "current_state", "needs", "skills", "values"]:
                    set_clauses.append(f"{key} = ?")
                    values.append(json.dumps(value, ensure_ascii=False))
                elif key in ["birth_date"]:
                    set_clauses.append(f"{key} = ?")
                    values.append(value.isoformat())
                else:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)

            set_clauses.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(character_id)

            query = f"UPDATE character_states SET {', '.join(set_clauses)} WHERE character_id = ?"
            cursor.execute(query, values)
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _update)

    async def delete_character(self, character_id: str) -> bool:
        """删除人物状态"""

        def _delete():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM character_states WHERE character_id = ?", (character_id,))
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _delete)

    async def list_characters(self, world_id: str) -> List[CharacterState]:
        """列出世界中的所有人物"""

        def _list():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM character_states WHERE world_id = ?", (world_id,))
            rows = cursor.fetchall()

            characters = []
            for row in rows:
                characters.append(
                    CharacterState(
                        character_id=row[0],
                        world_id=row[1],
                        name=row[2],
                        gender=row[3],
                        birth_date=datetime.fromisoformat(row[4]),
                        age=row[5],
                        personality=json.loads(row[6]),
                        current_state=json.loads(row[7]),
                        needs=json.loads(row[8]),
                        skills=json.loads(row[9]),
                        values=json.loads(row[10]),
                        relationship_graph_id=row[11],
                        event_timeline_id=row[12],
                        created_at=datetime.fromisoformat(row[13]),
                        updated_at=datetime.fromisoformat(row[14]),
                    )
                )
            self._close_connection(conn)
            return characters

        return await _get_event_loop().run_in_executor(None, _list)

    # ========== Event Implementation ==========
    async def create_event(self, event: Event) -> str:
        """创建事件"""

        def _create():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    event.event_id,
                    event.simulation_id,
                    event.event_type,
                    event.timestamp.isoformat(),
                    event.age_at_event,
                    event.title,
                    event.description,
                    event.intensity,
                    json.dumps(event.participants, ensure_ascii=False),
                    json.dumps(event.causes, ensure_ascii=False),
                    json.dumps(event.effects, ensure_ascii=False),
                    json.dumps(event.impact, ensure_ascii=False),
                    1 if event.is_spark_moment else 0,
                    event.spark_score,
                    json.dumps(event.metadata, ensure_ascii=False),
                    event.created_at.isoformat(),
                ),
            )
            conn.commit()
            self._close_connection(conn)
            return event.event_id

        return await _get_event_loop().run_in_executor(None, _create)

    async def get_event(self, event_id: str) -> Optional[Event]:
        """获取事件"""

        def _get():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
            row = cursor.fetchone()
            result = None
            if row:
                result = Event(
                    event_id=row[0],
                    simulation_id=row[1],
                    event_type=row[2],
                    timestamp=datetime.fromisoformat(row[3]),
                    age_at_event=row[4],
                    title=row[5],
                    description=row[6],
                    intensity=row[7],
                    participants=json.loads(row[8]),
                    causes=json.loads(row[9]),
                    effects=json.loads(row[10]),
                    impact=json.loads(row[11]),
                    is_spark_moment=bool(row[12]),
                    spark_score=row[13],
                    metadata=json.loads(row[14]),
                    created_at=datetime.fromisoformat(row[15]),
                )
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _get)

    async def list_events(
        self,
        simulation_id: str,
        character_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Event]:
        """列出事件"""

        def _list():
            conn = self._get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM events WHERE simulation_id = ?"
            params = [simulation_id]

            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time.isoformat())

            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time.isoformat())

            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            events = []
            for row in rows:
                events.append(
                    Event(
                        event_id=row[0],
                        simulation_id=row[1],
                        event_type=row[2],
                        timestamp=datetime.fromisoformat(row[3]),
                        age_at_event=row[4],
                        title=row[5],
                        description=row[6],
                        intensity=row[7],
                        participants=json.loads(row[8]),
                        causes=json.loads(row[9]),
                        effects=json.loads(row[10]),
                        impact=json.loads(row[11]),
                        is_spark_moment=bool(row[12]),
                        spark_score=row[13],
                        metadata=json.loads(row[14]),
                        created_at=datetime.fromisoformat(row[15]),
                    )
                )
            self._close_connection(conn)
            return events

        return await _get_event_loop().run_in_executor(None, _list)

    # ========== Simulation Context Implementation ==========
    async def create_simulation(self, simulation_context: SimulationContext) -> str:
        """创建模拟上下文"""

        def _create():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO simulation_contexts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    simulation_context.simulation_id,
                    simulation_context.world_id,
                    json.dumps(simulation_context.character_ids, ensure_ascii=False),
                    simulation_context.status,
                    simulation_context.current_time.isoformat(),
                    simulation_context.current_age,
                    simulation_context.total_events,
                    simulation_context.spark_moments_count,
                    simulation_context.speed,
                    simulation_context.created_at.isoformat(),
                    simulation_context.updated_at.isoformat(),
                ),
            )
            conn.commit()
            self._close_connection(conn)
            return simulation_context.simulation_id

        return await _get_event_loop().run_in_executor(None, _create)

    async def get_simulation(self, simulation_id: str) -> Optional[SimulationContext]:
        """获取模拟上下文"""

        def _get():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM simulation_contexts WHERE simulation_id = ?", (simulation_id,)
            )
            row = cursor.fetchone()
            result = None
            if row:
                result = SimulationContext(
                    simulation_id=row[0],
                    world_id=row[1],
                    character_ids=json.loads(row[2]),
                    status=row[3],
                    current_time=datetime.fromisoformat(row[4]),
                    current_age=row[5],
                    total_events=row[6],
                    spark_moments_count=row[7],
                    speed=row[8],
                    created_at=datetime.fromisoformat(row[9]),
                    updated_at=datetime.fromisoformat(row[10]),
                )
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _get)

    async def update_simulation(self, simulation_id: str, updates: Dict[str, Any]) -> bool:
        """更新模拟上下文"""

        def _update():
            conn = self._get_connection()
            cursor = conn.cursor()

            set_clauses = []
            values = []
            for key, value in updates.items():
                if key in ["character_ids"]:
                    set_clauses.append(f"{key} = ?")
                    values.append(json.dumps(value, ensure_ascii=False))
                elif key in ["current_time"]:
                    set_clauses.append(f"{key} = ?")
                    values.append(value.isoformat())
                else:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)

            set_clauses.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(simulation_id)

            query = (
                f"UPDATE simulation_contexts SET {', '.join(set_clauses)} WHERE simulation_id = ?"
            )
            cursor.execute(query, values)
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _update)

    async def delete_simulation(self, simulation_id: str) -> bool:
        """删除模拟上下文"""

        def _delete():
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM simulation_contexts WHERE simulation_id = ?", (simulation_id,)
            )
            conn.commit()
            result = cursor.rowcount > 0
            self._close_connection(conn)
            return result

        return await _get_event_loop().run_in_executor(None, _delete)
