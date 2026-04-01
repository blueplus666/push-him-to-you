from typing import Dict, Any, Optional
from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.models.world import (
    WorldState,
    WorldSetting,
    SocialStructure,
    CulturalFeature,
    EnvironmentDescription,
    ConflictSource
)
from app.prompts.world_builder_prompts import WorldBuilderPrompts
import uuid
from datetime import datetime


class WorldBuilderAgent(BaseAgent):
    """世界构建Agent

    负责创建和维护故事世界的基础设定。
    """

    def __init__(self, config: AgentConfig, llm_gateway):
        super().__init__(config, llm_gateway)
        self.prompts = WorldBuilderPrompts()

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行世界构建任务

        Args:
            input_data: 输入数据，包含：
                - action: "create" 或 "update"
                - era: 时代背景
                - location: 地理范围
                - society_type: 社会类型
                - special_settings: 特殊设定（可选）

        Returns:
            AgentResponse: 包含world_state的响应
        """
        try:
            action = input_data.get("action", "create")

            if action == "create":
                return await self._create_world(input_data)
            elif action == "update":
                return await self._update_world(input_data)
            else:
                return AgentResponse(
                    success=False,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )

    async def _create_world(self, input_data: Dict[str, Any]) -> AgentResponse:
        """创建新世界"""
        era = input_data.get("era")
        location = input_data.get("location")
        society_type = input_data.get("society_type")
        special_settings = input_data.get("special_settings", "无")

        if not all([era, location, society_type]):
            return AgentResponse(
                success=False,
                error="Missing required fields: era, location, society_type"
            )

        user_prompt = self.prompts.get_user_prompt(
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )

        response_text = await self.generate(
            prompt=user_prompt,
            system_prompt=self.prompts.get_system_prompt()
        )

        world_state = self._parse_to_world_state(
            response_text,
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )

        return AgentResponse(
            success=True,
            data={
                "world_state": world_state.model_dump(),
                "raw_response": response_text
            },
            metadata={
                "agent": "world_builder",
                "action": "create"
            }
        )

    async def _update_world(self, input_data: Dict[str, Any]) -> AgentResponse:
        """更新现有世界"""
        world_data = input_data.get("world")
        update_request = input_data.get("update_request", "")

        if not world_data:
            return AgentResponse(
                success=False,
                error="Missing world data for update"
            )

        update_prompt = f"""
当前世界设定：
{world_data}

更新请求：{update_request}

请根据更新请求，提供更新后的相关部分内容。
"""

        response_text = await self.generate(
            prompt=update_prompt,
            system_prompt=self.prompts.get_system_prompt()
        )

        return AgentResponse(
            success=True,
            data={
                "update_response": response_text
            },
            metadata={
                "agent": "world_builder",
                "action": "update"
            }
        )

    def _parse_to_world_state(
        self,
        response_text: str,
        era: str,
        location: str,
        society_type: str,
        special_settings: str = "无"
    ) -> WorldState:
        """将LLM响应解析为WorldState对象"""
        parsed = self.prompts.parse_response(response_text)

        world_id = f"world-{uuid.uuid4().hex[:8]}"

        setting = WorldSetting(
            era=era,
            location={"description": location},
            society_type=society_type,
            special_settings=[special_settings] if special_settings != "无" else []
        )

        social_structure = self._parse_social_structure(parsed.get("社会结构", ""))
        cultural_features = self._parse_cultural_features(parsed.get("文化特征", ""))
        environment = self._parse_environment(parsed.get("环境特点", ""))
        conflict_sources = self._parse_conflicts(parsed.get("潜在冲突源", ""))

        return WorldState(
            world_id=world_id,
            setting=setting,
            social_structure=social_structure,
            cultural_features=cultural_features,
            environment=environment,
            conflict_sources=conflict_sources
        )

    def _parse_social_structure(self, text: str) -> Optional[SocialStructure]:
        """解析社会结构"""
        if not text:
            return None

        classes = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                class_name = line.lstrip("-• ").split("：")[0].split(":")[0].strip()
                if class_name:
                    classes.append(class_name)

        return SocialStructure(classes=classes) if classes else None

    def _parse_cultural_features(self, text: str) -> Optional[CulturalFeature]:
        """解析文化特征"""
        if not text:
            return None

        core_values = []
        customs = []

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if "核心价值观" in line or "价值观" in line:
                values_str = line.split("：")[-1].split(":")[-1].strip()
                core_values = [v.strip() for v in values_str.split("、") if v.strip()]
            elif "习俗" in line:
                customs_str = line.split("：")[-1].split(":")[-1].strip()
                customs = [c.strip() for c in customs_str.split("、") if c.strip()]

        return CulturalFeature(
            core_values=core_values,
            customs=customs
        ) if core_values or customs else None

    def _parse_environment(self, text: str) -> Optional[EnvironmentDescription]:
        """解析环境描述"""
        if not text:
            return None

        natural_env = ""
        urban_env = ""

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if "自然" in line:
                natural_env = line.split("：")[-1].split(":")[-1].strip()
            elif "城市" in line:
                urban_env = line.split("：")[-1].split(":")[-1].strip()

        return EnvironmentDescription(
            natural_environment=natural_env,
            urban_environment=urban_env
        )

    def _parse_conflicts(self, text: str) -> list:
        """解析冲突源"""
        if not text:
            return []

        social_contradictions = []

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                conflict = line.lstrip("-• ").strip()
                if conflict:
                    social_contradictions.append(conflict)

        if social_contradictions:
            return [ConflictSource(social_contradictions=social_contradictions)]
        return []
