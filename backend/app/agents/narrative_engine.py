"""
叙事引擎Agent
负责管理故事结构、组织章节和场景、协调叙事节奏
"""
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from app.agents.base import BaseAgent, AgentConfig, AgentResponse
from app.services.structure_manager import StructureManager
from app.services.scene_manager import SceneManager
from app.services.pacing_controller import PacingController
from app.prompts.narrative_prompts import NarrativeEnginePrompts
from app.models.narrative import (
    NarrativeStructureType,
    Story,
    Act,
    Scene,
    SceneType,
    NarrativeReport,
)


class NarrativeEngineAgent(BaseAgent):
    """叙事引擎Agent

    负责管理故事结构、组织章节和场景、协调叙事节奏。
    """

    def __init__(self, config: AgentConfig, llm_gateway):
        super().__init__(config, llm_gateway)
        self.structure_manager = StructureManager()
        self.scene_manager = SceneManager()
        self.pacing_controller = PacingController()
        self.prompts = NarrativeEnginePrompts()
        self.stories: Dict[str, Story] = {}

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行Agent任务

        Actions:
        - create_story: 创建故事结构
        - add_scene: 添加场景
        - update_scene: 更新场景
        - get_report: 获取叙事报告
        - analyze_pacing: 分析叙事节奏
        - suggest_next: 建议下一步
        """
        action = input_data.get("action", "create_story")

        action_handlers = {
            "create_story": self._create_story,
            "add_scene": self._add_scene,
            "update_scene": self._update_scene,
            "get_report": self._get_report,
            "analyze_pacing": self._analyze_pacing,
            "suggest_next": self._suggest_next,
        }

        handler = action_handlers.get(action)
        if not handler:
            return AgentResponse(
                success=False,
                error=f"Unknown action: {action}"
            )

        return await handler(input_data)

    async def _create_story(self, input_data: Dict[str, Any]) -> AgentResponse:
        """创建故事结构"""
        world_id = input_data.get("world_id")
        structure_type_str = input_data.get("structure_type", "three_act")
        title = input_data.get("title", "Untitled")
        description = input_data.get("description", "")

        if not world_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: world_id"
            )

        try:
            structure_type = NarrativeStructureType(structure_type_str)
        except ValueError:
            return AgentResponse(
                success=False,
                error=f"Invalid structure type: {structure_type_str}"
            )

        story_config = {
            "world_id": world_id,
            "title": title,
            "description": description,
        }

        story = self.structure_manager.create_structure(structure_type, story_config)
        self.stories[story.story_id] = story

        return AgentResponse(
            success=True,
            data={"story": story.model_dump()},
            metadata={"action": "create_story", "story_id": story.story_id}
        )

    async def _add_scene(self, input_data: Dict[str, Any]) -> AgentResponse:
        """添加场景"""
        story_id = input_data.get("story_id")
        act_number = input_data.get("act_number", 1)
        scene_config = input_data.get("scene_config", {})

        if not story_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: story_id"
            )

        story = self.stories.get(story_id)
        if not story:
            return AgentResponse(
                success=False,
                error=f"Story not found: {story_id}"
            )

        if act_number < 1 or act_number > len(story.acts):
            return AgentResponse(
                success=False,
                error=f"Invalid act number: {act_number}"
            )

        act = story.acts[act_number - 1]

        scene_config["scene_type"] = scene_config.get("scene_type", "exposition")
        scene_config["title"] = scene_config.get("title", "Untitled")
        scene_config["description"] = scene_config.get("description", "")
        scene_config["location"] = scene_config.get("location", "")
        scene_config["tension_level"] = scene_config.get("tension_level", 50.0)
        scene_config["pacing"] = scene_config.get("pacing", "normal")

        scene = self.scene_manager.create_scene(scene_config, act)

        story.updated_at = datetime.now()

        return AgentResponse(
            success=True,
            data={"scene": scene.model_dump()},
            metadata={"action": "add_scene", "story_id": story_id}
        )

    async def _update_scene(self, input_data: Dict[str, Any]) -> AgentResponse:
        """更新场景"""
        story_id = input_data.get("story_id")
        scene_id = input_data.get("scene_id")
        updates = input_data.get("updates", {})

        if not story_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: story_id"
            )

        if not scene_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: scene_id"
            )

        story = self.stories.get(story_id)
        if not story:
            return AgentResponse(
                success=False,
                error=f"Story not found: {story_id}"
            )

        scene = None
        for act in story.acts:
            for s in act.scenes:
                if s.scene_id == scene_id:
                    scene = s
                    break
            if scene:
                break

        if not scene:
            return AgentResponse(
                success=False,
                error=f"Scene not found: {scene_id}"
            )

        updated_scene = self.scene_manager.update_scene(scene, updates)

        story.updated_at = datetime.now()

        return AgentResponse(
            success=True,
            data={"scene": updated_scene.model_dump()},
            metadata={"action": "update_scene", "story_id": story_id}
        )

    async def _get_report(self, input_data: Dict[str, Any]) -> AgentResponse:
        """获取叙事报告"""
        story_id = input_data.get("story_id")

        if not story_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: story_id"
            )

        story = self.stories.get(story_id)
        if not story:
            return AgentResponse(
                success=False,
                error=f"Story not found: {story_id}"
            )

        all_scenes = story.get_all_scenes()

        pacing_analysis = self.pacing_controller.analyze_pacing(story)

        tension_curve = [scene.tension_level for scene in all_scenes]

        completed_scenes = sum(
            1 for scene in all_scenes
            if scene.status == "complete"
        )

        total_word_count = sum(scene.word_count for scene in all_scenes)

        act_summaries = []
        for act in story.acts:
            act_summaries.append({
                "act_number": act.act_number,
                "title": act.title,
                "scene_count": len(act.scenes),
                "act_tension": act.calculate_act_tension(),
            })

        report = NarrativeReport(
            report_id=f"report-{uuid.uuid4().hex[:8]}",
            story_id=story_id,
            structure_analysis={
                "structure_type": story.structure_type.value,
                "act_count": len(story.acts),
                "is_valid": self.structure_manager.validate_structure(story),
            },
            act_summaries=act_summaries,
            tension_analysis={
                "overall_tension": story.overall_tension,
                "tension_range": [min(tension_curve), max(tension_curve)] if tension_curve else [0, 0],
            },
            tension_curve=tension_curve,
            pacing_analysis=pacing_analysis,
            pacing_recommendations=[],
            total_scenes=len(all_scenes),
            completed_scenes=completed_scenes,
            total_word_count=total_word_count,
            narrative_health=story.overall_tension,
            recommendations=[],
            next_actions=[],
        )

        return AgentResponse(
            success=True,
            data={"report": report.model_dump()},
            metadata={"action": "get_report", "story_id": story_id}
        )

    async def _analyze_pacing(self, input_data: Dict[str, Any]) -> AgentResponse:
        """分析叙事节奏"""
        story_id = input_data.get("story_id")

        if not story_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: story_id"
            )

        story = self.stories.get(story_id)
        if not story:
            return AgentResponse(
                success=False,
                error=f"Story not found: {story_id}"
            )

        pacing_analysis = self.pacing_controller.analyze_pacing(story)
        pacing_issues = self.pacing_controller.detect_pacing_issues(story)

        return AgentResponse(
            success=True,
            data={
                "pacing_analysis": pacing_analysis,
                "pacing_issues": pacing_issues,
            },
            metadata={"action": "analyze_pacing", "story_id": story_id}
        )

    async def _suggest_next(self, input_data: Dict[str, Any]) -> AgentResponse:
        """建议下一步叙事方向"""
        story_id = input_data.get("story_id")

        if not story_id:
            return AgentResponse(
                success=False,
                error="Missing required parameter: story_id"
            )

        story = self.stories.get(story_id)
        if not story:
            return AgentResponse(
                success=False,
                error=f"Story not found: {story_id}"
            )

        suggestions = []

        current_act = story.get_current_act()
        if current_act:
            if not current_act.scenes:
                suggestions.append(f"建议在{current_act.title}中添加第一个场景")
            else:
                current_scene = current_act.get_current_scene()
                if current_scene:
                    suggestions.append(f"继续发展场景: {current_scene.title}")
                else:
                    suggestions.append(f"推进到{current_act.title}的下一个场景")
        else:
            suggestions.append("故事尚未开始,建议创建第一个场景")

        pacing_analysis = self.pacing_controller.analyze_pacing(story)
        pacing_type = pacing_analysis.get("pacing_type", "normal")

        if pacing_type == "slow":
            suggestions.append("当前节奏较慢,可以考虑增加冲突或事件")
        elif pacing_type == "fast":
            suggestions.append("当前节奏较快,可以考虑增加描述或角色发展")

        pacing_issues = self.pacing_controller.detect_pacing_issues(story)
        for issue in pacing_issues:
            if issue["issue_type"] == "monotonic_pacing":
                suggestions.append("建议增加节奏变化,避免单调")
            elif issue["issue_type"] == "too_fast_start":
                suggestions.append("开头节奏过快,建议放慢以帮助读者适应")

        return AgentResponse(
            success=True,
            data={"suggestions": suggestions},
            metadata={"action": "suggest_next", "story_id": story_id}
        )
