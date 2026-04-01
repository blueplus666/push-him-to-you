import pytest
from app.prompts.world_builder_prompts import (
    WorldBuilderPrompts,
    WORLD_BUILDER_SYSTEM_PROMPT,
    WORLD_BUILDER_USER_PROMPT
)


def test_system_prompt_exists():
    """测试系统提示词存在"""
    assert WORLD_BUILDER_SYSTEM_PROMPT is not None
    assert len(WORLD_BUILDER_SYSTEM_PROMPT) > 100


def test_user_prompt_template():
    """测试用户提示词模板"""
    prompt = WORLD_BUILDER_USER_PROMPT.format(
        era="现代都市",
        location="杭州",
        society_type="平稳发展型",
        special_settings="无"
    )
    assert "现代都市" in prompt
    assert "杭州" in prompt


def test_world_builder_prompts_class():
    """测试WorldBuilderPrompts类"""
    prompts = WorldBuilderPrompts()

    system_prompt = prompts.get_system_prompt()
    assert system_prompt is not None

    user_prompt = prompts.get_user_prompt(
        era="古代",
        location="长安",
        society_type="封建社会",
        special_settings="武侠世界"
    )
    assert "古代" in user_prompt
    assert "长安" in user_prompt


def test_parse_world_response():
    """测试解析世界响应"""
    prompts = WorldBuilderPrompts()

    response_text = """
## 世界概述
这是一个现代都市世界。

## 社会结构
- 上层：企业家、高管
- 中层：白领、技术人员
- 底层：工人、服务业从业者

## 文化特征
- 核心价值观：勤劳、诚信、创新
- 主要习俗：春节团圆、中秋赏月

## 环境特点
- 自然环境：江南水乡，四季分明
- 城市环境：现代化都市

## 潜在冲突源
- 社会矛盾：贫富差距、代际冲突
- 资源争夺：房价、教育资源
"""

    parsed = prompts.parse_response(response_text)
    assert "世界概述" in parsed
    assert "社会结构" in parsed
