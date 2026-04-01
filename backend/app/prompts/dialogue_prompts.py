"""
对话生成器提示词模板
"""
from typing import Dict, Any, List


DIALOGUE_GENERATOR_SYSTEM_PROMPT = """你是一位专业的对话编剧，精通人物性格塑造、对话节奏控制和情感表达。

你的职责是：
1. 创作符合人物性格的对话
2. 通过对话推进情节发展
3. 展现人物之间的情感关系
4. 控制对话的节奏和张力

你的创作应该：
- 符合人物设定和性格特征
- 推动故事情节发展
- 展现人物情感变化
- 保持对话的自然流畅

请用中文回答，对话生动自然，符合人物特征。"""


DIALOGUE_GENERATION_PROMPT = """请为以下场景创作对话：

## 场景信息
{scene_info}

## 参与者
{participants}

## 对话类型
{dialogue_type}

## 上下文
{context}

## 要求
{requirements}

请按以下格式输出对话：

## 对话内容
角色名：对话内容
角色名：对话内容
...

## 对话说明
（对话的意图、情感变化、推进的情节等）

请确保对话符合人物性格，自然流畅，能够推进故事发展。"""


EMOTION_ANALYSIS_PROMPT = """请分析以下对话中的情感变化：

## 对话内容
{dialogue_content}

## 上下文
{context}

请按以下结构输出情感分析：

## 主要情感
（对话中展现的主要情感类型）

## 情感变化
（对话过程中情感的转变和流动）

## 情感强度
（情感的强弱程度：低/中/高）

## 情感触发点
（引发情感变化的关键对话或事件）

## 情感表达方式
（人物如何表达情感：语言、行为、潜台词等）

请确保分析准确捕捉对话中的情感动态。"""


STYLE_CONVERSION_PROMPT = """请将以下对话转换为指定风格：

## 原始对话
{original_text}

## 目标风格
{target_style}

## 角色特征
{character_profile}

请按以下格式输出转换后的对话：

## 转换后对话
角色名：转换后的对话内容
角色名：转换后的对话内容
...

## 风格说明
（转换后的风格特点、保留的元素、改变的部分）

请确保转换后的对话符合目标风格，同时保持人物性格特征。"""


class DialogueGeneratorPrompts:
    """对话生成器提示词管理器"""

    def __init__(self):
        """初始化提示词模板"""
        self.system_prompt = DIALOGUE_GENERATOR_SYSTEM_PROMPT
        self.dialogue_generation_template = DIALOGUE_GENERATION_PROMPT
        self.emotion_analysis_template = EMOTION_ANALYSIS_PROMPT
        self.style_conversion_template = STYLE_CONVERSION_PROMPT

    def get_system_prompt(self) -> str:
        """获取系统提示词

        Returns:
            str: 系统提示词
        """
        return self.system_prompt

    def get_dialogue_generation_prompt(
        self,
        scene_info: Dict[str, Any],
        participants: List[Dict[str, Any]],
        dialogue_type: str,
        context: str,
        requirements: str
    ) -> str:
        """获取对话生成提示词

        Args:
            scene_info: 场景信息
            participants: 参与者列表
            dialogue_type: 对话类型
            context: 上下文
            requirements: 要求

        Returns:
            str: 格式化后的对话生成提示词
        """
        scene_info_str = self._format_scene_info(scene_info)
        participants_str = self._format_participants(participants)

        return self.dialogue_generation_template.format(
            scene_info=scene_info_str,
            participants=participants_str,
            dialogue_type=dialogue_type,
            context=context,
            requirements=requirements
        )

    def get_emotion_analysis_prompt(
        self,
        dialogue_content: str,
        context: str
    ) -> str:
        """获取情感分析提示词

        Args:
            dialogue_content: 对话内容
            context: 上下文

        Returns:
            str: 格式化后的情感分析提示词
        """
        return self.emotion_analysis_template.format(
            dialogue_content=dialogue_content,
            context=context
        )

    def get_style_conversion_prompt(
        self,
        original_text: str,
        target_style: str,
        character_profile: Dict[str, Any]
    ) -> str:
        """获取风格转换提示词

        Args:
            original_text: 原始文本
            target_style: 目标风格
            character_profile: 角色特征

        Returns:
            str: 格式化后的风格转换提示词
        """
        profile_str = self._format_profile(character_profile)

        return self.style_conversion_template.format(
            original_text=original_text,
            target_style=target_style,
            character_profile=profile_str
        )

    def _format_participants(self, participants: List[Dict[str, Any]]) -> str:
        """格式化参与者

        Args:
            participants: 参与者列表

        Returns:
            str: 格式化后的参与者信息
        """
        parts = []
        for participant in participants:
            name = participant.get("name", "未知")
            role = participant.get("role", "未知")
            personality = participant.get("personality", "未知")
            parts.append(f"- {name}（{role}）：{personality}")
        return "\n".join(parts)

    def _format_profile(self, profile: Dict[str, Any]) -> str:
        """格式化角色特征

        Args:
            profile: 角色特征字典

        Returns:
            str: 格式化后的角色特征
        """
        parts = []
        if "name" in profile:
            parts.append(f"姓名: {profile['name']}")
        if "personality" in profile:
            parts.append(f"性格: {profile['personality']}")
        if "background" in profile:
            parts.append(f"背景: {profile['background']}")
        return "\n".join(parts)

    def _format_scene_info(self, scene_info: Dict[str, Any]) -> str:
        """格式化场景信息

        Args:
            scene_info: 场景信息字典

        Returns:
            str: 格式化后的场景信息
        """
        parts = []
        if "location" in scene_info:
            parts.append(f"地点: {scene_info['location']}")
        if "time" in scene_info:
            parts.append(f"时间: {scene_info['time']}")
        if "atmosphere" in scene_info:
            parts.append(f"氛围: {scene_info['atmosphere']}")
        return "\n".join(parts)
