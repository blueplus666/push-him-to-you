"""
叙事引擎提示词模板
"""
from typing import Dict, Any


NARRATIVE_ENGINE_SYSTEM_PROMPT = """你是一位专业的叙事设计师，精通故事结构、节奏控制和戏剧张力管理。

你的职责是：
1. 设计合理的故事结构
2. 组织章节和场景
3. 协调叙事节奏
4. 维持戏剧张力

你的分析应该:
- 遵循叙事学原理
- 确保结构完整性
- 创造有意义的张力曲线
- 保持节奏变化

请用中文回答，逻辑清晰,结构明确。"""


SCENE_CREATE_PROMPT = """请为以下故事创建一个场景:

## 故事背景
{story_context}

## 当前幕信息
{act_info}

## 场景要求
{scene_requirements}

## 已有场景
{existing_scenes}

请按以下结构输出场景设定:

## 场景编号
场景X: [场景名称]

## 场景描述
(场景的基本设定和氛围)

## 场景目标
(该场景在叙事中的作用和目标)

## 主要人物
(参与该场景的主要人物)

## 关键事件
(场景中发生的关键事件)

## 张力等级
(低/中/高,以及张力来源)

## 节奏类型
(快/中/慢,以及节奏控制方式)

## 伏笔/呼应
(该场景埋下的伏笔或呼应的前文)

请确保场景设计符合整体叙事结构,推进故事发展。"""


PACING_ANALYSIS_PROMPT = """请分析以下故事的叙事节奏:

## 故事概述
{story_summary}

## 场景序列
{scene_sequence}

## 张力曲线
{tension_curve}

请按以下结构输出节奏分析:

## 整体节奏评估
(故事整体节奏的合理性)

## 张力曲线分析
(张力变化的合理性和效果)

## 节奏变化点
(关键的节奏转折点)

## 改进建议
(针对节奏问题的改进建议)

## 优化方案
(具体的节奏调整方案)

请确保分析基于叙事学原理,提供可操作的改进建议."""


class NarrativeEnginePrompts:
    """叙事引擎提示词管理器"""

    def __init__(self):
        self.system_prompt = NARRATIVE_ENGINE_SYSTEM_PROMPT
        self.scene_create_template = SCENE_CREATE_PROMPT
        self.pacing_analysis_template = PACING_ANALYSIS_PROMPT

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.system_prompt

    def get_scene_create_prompt(
        self,
        story_context: Dict[str, Any],
        act_info: Dict[str, Any],
        scene_requirements: Dict[str, Any],
        existing_scenes: str
    ) -> str:
        """获取场景创建提示词"""

        story_context_str = self._format_story_context(story_context)
        act_info_str = self._format_act_info(act_info)
        scene_requirements_str = self._format_scene_requirements(scene_requirements)

        return self.scene_create_template.format(
            story_context=story_context_str,
            act_info=act_info_str,
            scene_requirements=scene_requirements_str,
            existing_scenes=existing_scenes,
        )

    def get_pacing_analysis_prompt(
        self,
        story_summary: str,
        scene_sequence: str,
        tension_curve: str
    ) -> str:
        """获取节奏分析提示词"""
        return self.pacing_analysis_template.format(
            story_summary=story_summary,
            scene_sequence=scene_sequence,
            tension_curve=tension_curve,
        )

    def _format_story_context(self, story_context: Dict[str, Any]) -> str:
        """格式化故事背景"""
        parts = []
        if "title" in story_context:
            parts.append(f"标题: {story_context['title']}")
        if "genre" in story_context:
            parts.append(f"类型: {story_context['genre']}")
        if "theme" in story_context:
            parts.append(f"主题: {story_context['theme']}")
        return "\n".join(parts)

    def _format_act_info(self, act_info: Dict[str, Any]) -> str:
        """格式化幕信息"""
        parts = []
        if "act_number" in act_info:
            parts.append(f"幕数: {act_info['act_number']}")
        if "act_name" in act_info:
            parts.append(f"幕名: {act_info['act_name']}")
        if "description" in act_info:
            parts.append(f"描述: {act_info['description']}")
        return "\n".join(parts)

    def _format_scene_requirements(self, scene_requirements: Dict[str, Any]) -> str:
        """格式化场景要求"""
        parts = []
        if "scene_type" in scene_requirements:
            parts.append(f"场景类型: {scene_requirements['scene_type']}")
        if "location" in scene_requirements:
            parts.append(f"地点: {scene_requirements['location']}")
        if "characters" in scene_requirements:
            parts.append(f"人物: {', '.join(scene_requirements['characters'])}")
        return "\n".join(parts)
