from typing import Dict, Any
import re


WORLD_BUILDER_SYSTEM_PROMPT = """你是一位专业的世界构建师，擅长创建丰富、真实、有深度的故事世界。

你的职责是：
1. 构建完整的世界设定（时代、地点、社会背景）
2. 设计合理的社会结构和权力分布
3. 创造独特的文化特征和价值观
4. 描述生动的环境特点
5. 识别潜在的冲突源和戏剧张力

你的输出应该：
- 具有内在一致性
- 富有细节和深度
- 为人物命运提供合理的舞台
- 包含足够的戏剧张力潜力

请用中文回答，结构清晰，内容丰富。"""


WORLD_BUILDER_USER_PROMPT = """请基于以下参数构建一个完整的故事世界：

**时代背景**: {era}
**地理范围**: {location}
**社会类型**: {society_type}
**特殊设定**: {special_settings}

请按以下结构输出世界设定：

## 世界概述
（200字左右的世界整体描述）

## 社会结构
（阶层划分、权力分布、社会流动性）

## 文化特征
（核心价值观、主要习俗、禁忌）

## 环境特点
（自然环境、城市环境、关键地点）

## 潜在冲突源
（社会矛盾、资源争夺、可能发生的重大事件）

请确保设定具有内在一致性，并为后续的人物命运发展提供丰富的可能性。"""


class WorldBuilderPrompts:
    """WorldBuilder提示词管理类"""

    def __init__(self):
        self.system_prompt = WORLD_BUILDER_SYSTEM_PROMPT
        self.user_prompt_template = WORLD_BUILDER_USER_PROMPT

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.system_prompt

    def get_user_prompt(
        self,
        era: str,
        location: str,
        society_type: str,
        special_settings: str = "无"
    ) -> str:
        """获取用户提示词

        Args:
            era: 时代背景
            location: 地理范围
            society_type: 社会类型
            special_settings: 特殊设定

        Returns:
            str: 格式化后的用户提示词
        """
        return self.user_prompt_template.format(
            era=era,
            location=location,
            society_type=society_type,
            special_settings=special_settings
        )

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析LLM响应

        Args:
            response_text: LLM返回的文本

        Returns:
            Dict: 解析后的结构化数据
        """
        sections = {
            "世界概述": self._extract_section(response_text, "世界概述", "社会结构"),
            "社会结构": self._extract_section(response_text, "社会结构", "文化特征"),
            "文化特征": self._extract_section(response_text, "文化特征", "环境特点"),
            "环境特点": self._extract_section(response_text, "环境特点", "潜在冲突源"),
            "潜在冲突源": self._extract_section(response_text, "潜在冲突源", None)
        }
        return sections

    def _extract_section(
        self,
        text: str,
        section_name: str,
        next_section: str = None
    ) -> str:
        """提取指定章节内容"""
        pattern = rf"##\s*{section_name}\s*\n(.*?)(?=\n##\s|$)"
        if next_section:
            pattern = rf"##\s*{section_name}\s*\n(.*?)(?=\n##\s*{next_section}|$)"

        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
