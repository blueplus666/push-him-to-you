"""
Fate Engine Agent
命运引擎Agent主类，整合所有组件
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.models.fate import (
    FateThread,
    FateState,
    FateNode,
    FateNodeType,
    CausalEvent,
    EventType,
    CausalChain,
    FateReport,
    PredictedEvent,
    FateTrend,
)
from app.models.character import Character
from app.services.causal_engine import CausalEngine
from app.services.fate_manager import FateManager
from app.services.tension_calculator import TensionCalculator
from app.prompts.fate_prompts import FateEnginePrompts


# 常量定义
DEFAULT_WORLD_ID = "default-world"
DEFAULT_CHAIN_ID = "default-chain"
DEFAULT_TENSION = 50.0
TENSION_IMPACT_FACTOR = 0.1


class FateEngineAgent(BaseAgent):
    """Fate Engine Agent

    命运引擎Agent，负责管理命运线、因果链和戏剧张力。

    Attributes:
        causal_engine: 因果引擎
        fate_manager: 命运管理器
        tension_calculator: 张力计算器
        prompts: 提示词管理器
        chains: 因果链字典
    """

    def __init__(self, config: AgentConfig, llm_gateway):
        """初始化Fate Engine Agent

        Args:
            config: Agent配置
            llm_gateway: LLM网关
        """
        super().__init__(config, llm_gateway)
        self.causal_engine = CausalEngine()
        self.fate_manager = FateManager()
        self.tension_calculator = TensionCalculator()
        self.prompts = FateEnginePrompts()
        self.chains: Dict[str, CausalChain] = {}

    def _get_world_threads(self, world_id: str) -> List[FateThread]:
        """获取指定世界的命运线列表

        Args:
            world_id: 世界ID

        Returns:
            List[FateThread]: 命运线列表
        """
        return [
            thread
            for thread in self.fate_manager.threads.values()
            if thread.world_id == world_id
        ]

    def _find_thread_by_character(self, character_id: str) -> Optional[FateThread]:
        """根据角色ID查找命运线

        Args:
            character_id: 角色ID

        Returns:
            Optional[FateThread]: 命运线，如果未找到则返回None
        """
        for thread in self.fate_manager.threads.values():
            if thread.character_id == character_id:
                return thread
        return None

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Execute agent task

        Args:
            input_data: 输入数据，必须包含action字段

        Actions:
        - advance: 推进命运
        - add_event: 添加事件到因果链
        - get_report: 获取命运报告
        - create_thread: 创建命运线
        - detect_intersection: 检测命运交织
        - predict: 预测命运走向

        Returns:
            AgentResponse: Agent响应
        """
        # 检查action字段
        action = input_data.get("action")
        if not action:
            return AgentResponse(success=False, error="Missing required field: action")

        # 路由到不同的处理方法
        action_handlers = {
            "advance": self._advance_fate,
            "add_event": self._add_event,
            "get_report": self._get_report,
            "create_thread": self._create_thread,
            "detect_intersection": self._detect_intersection,
            "predict": self._predict_fate,
        }

        handler = action_handlers.get(action)
        if not handler:
            return AgentResponse(success=False, error=f"Unknown action: {action}")

        return await handler(input_data)

    async def _advance_fate(self, input_data: Dict[str, Any]) -> AgentResponse:
        """推进命运

        Args:
            input_data: 包含event、world_id和context的输入数据

        Returns:
            AgentResponse: 包含consequences、tension_change和analysis的响应
        """
        # 检查必需字段
        event_data = input_data.get("event")
        if not event_data:
            return AgentResponse(success=False, error="Missing required field: event")

        world_id = input_data.get("world_id", DEFAULT_WORLD_ID)
        context = input_data.get("context", {})

        # 创建事件对象
        try:
            event = CausalEvent(**event_data)
        except Exception as e:
            return AgentResponse(success=False, error=f"Invalid event data: {str(e)}")

        # 处理事件，生成后果
        consequences = self.causal_engine.process_event(event, context)

        # 计算张力变化
        current_tension = context.get("current_tension", DEFAULT_TENSION)
        event_tension = self.tension_calculator.calculate_event_tension(event, context)
        tension_change = event_tension - current_tension * TENSION_IMPACT_FACTOR

        # 生成分析（使用LLM）
        try:
            analysis = await self.generate(
                self.prompts.get_advance_prompt(
                    fate_state={"world_id": world_id},
                    trigger_event=event_data,
                    world_context={"world_id": world_id},
                    event_history="",
                    current_tension=current_tension,
                )
            )
        except Exception:
            analysis = "命运推进分析完成"

        return AgentResponse(
            success=True,
            data={
                "consequences": [c.model_dump() for c in consequences],
                "tension_change": abs(tension_change),
                "analysis": analysis,
            },
        )

    async def _add_event(self, input_data: Dict[str, Any]) -> AgentResponse:
        """添加事件到因果链

        Args:
            input_data: 包含event、chain_id和world_id的输入数据

        Returns:
            AgentResponse: 包含chain_id、event_id和current_tension的响应
        """
        # 检查必需字段
        event_data = input_data.get("event")
        if not event_data:
            return AgentResponse(success=False, error="Missing required field: event")

        chain_id = input_data.get("chain_id", DEFAULT_CHAIN_ID)
        world_id = input_data.get("world_id", DEFAULT_WORLD_ID)

        # 创建事件对象
        try:
            event = CausalEvent(**event_data)
        except Exception as e:
            return AgentResponse(success=False, error=f"Invalid event data: {str(e)}")

        # 获取或创建因果链
        if chain_id not in self.chains:
            self.chains[chain_id] = CausalChain(
                chain_id=chain_id,
                world_id=world_id,
                events=[],
                current_tension=DEFAULT_TENSION,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

        chain = self.chains[chain_id]

        # 添加事件到链
        chain.events.append(event)
        chain.updated_at = datetime.now()

        # 计算张力
        event_tension = self.tension_calculator.calculate_event_tension(event)
        chain.current_tension = min(
            100, chain.current_tension + event_tension * TENSION_IMPACT_FACTOR
        )
        chain.tension_history.append(chain.current_tension)

        return AgentResponse(
            success=True,
            data={
                "chain_id": chain_id,
                "event_id": event.event_id,
                "current_tension": chain.current_tension,
            },
        )

    async def _get_report(self, input_data: Dict[str, Any]) -> AgentResponse:
        """生成命运报告

        Args:
            input_data: 包含world_id的输入数据

        Returns:
            AgentResponse: 包含report的响应
        """
        world_id = input_data.get("world_id", DEFAULT_WORLD_ID)

        # 获取该世界的命运线
        threads = self._get_world_threads(world_id)

        # 计算整体张力
        overall_tension = self.tension_calculator.calculate_overall_tension(
            threads=threads
        )

        # 统计待解决节点
        pending_nodes = sum(
            len([n for n in thread.nodes if not n.is_resolved]) for thread in threads
        )

        # 创建报告
        report = FateReport(
            report_id=f"report-{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            world_id=world_id,
            overall_tension=overall_tension,
            active_threads=len(threads),
            pending_nodes=pending_nodes,
            character_states={
                thread.character_id: thread.current_state for thread in threads
            },
            active_chains=list(self.chains.keys()),
            upcoming_events=[],
            recommended_actions=[],
        )

        return AgentResponse(success=True, data={"report": report.model_dump()})

    async def _create_thread(self, input_data: Dict[str, Any]) -> AgentResponse:
        """创建命运线

        Args:
            input_data: 包含character和world_id的输入数据

        Returns:
            AgentResponse: 包含thread_id、character_id和initial_state的响应
        """
        # 检查必需字段
        character_data = input_data.get("character")
        if not character_data:
            return AgentResponse(
                success=False, error="Missing required field: character"
            )

        world_id = input_data.get("world_id", DEFAULT_WORLD_ID)

        # 创建人物对象
        try:
            character = Character(**character_data)
        except Exception as e:
            return AgentResponse(
                success=False, error=f"Invalid character data: {str(e)}"
            )

        # 创建命运线
        thread = self.fate_manager.create_fate_thread(character, world_id)

        return AgentResponse(
            success=True,
            data={
                "thread_id": thread.thread_id,
                "character_id": thread.character_id,
                "initial_state": thread.current_state.model_dump(),
            },
        )

    async def _detect_intersection(self, input_data: Dict[str, Any]) -> AgentResponse:
        """检测命运线交织

        Args:
            input_data: 包含world_id的输入数据

        Returns:
            AgentResponse: 包含intersections的响应
        """
        world_id = input_data.get("world_id", DEFAULT_WORLD_ID)

        # 获取该世界的命运线
        threads = self._get_world_threads(world_id)

        # 检测交织
        intersections = self.fate_manager.detect_intersection(threads)

        return AgentResponse(success=True, data={"intersections": intersections})

    async def _predict_fate(self, input_data: Dict[str, Any]) -> AgentResponse:
        """预测命运走向

        Args:
            input_data: 包含character_id和world_context的输入数据

        Returns:
            AgentResponse: 包含predictions的响应
        """
        character_id = input_data.get("character_id")
        world_context = input_data.get("world_context", {})

        # 查找该角色的命运线
        thread = self._find_thread_by_character(character_id)

        if not thread:
            return AgentResponse(
                success=False,
                error=f"Fate thread not found for character: {character_id}",
            )

        # 预测张力弧线
        tension_predictions = self.tension_calculator.predict_tension_arc(
            thread, steps=5
        )

        # 使用LLM生成预测
        try:
            prediction_text = await self.generate(
                self.prompts.get_prediction_prompt(
                    character_state=thread.current_state.model_dump(),
                    fate_history=str(thread.tension_arc),
                    world_context=world_context,
                )
            )
        except Exception:
            prediction_text = "命运预测分析完成"

        return AgentResponse(
            success=True,
            data={
                "predictions": {
                    "short_term": tension_predictions[:2],
                    "long_term": tension_predictions[2:],
                    "analysis": prediction_text,
                }
            },
        )
