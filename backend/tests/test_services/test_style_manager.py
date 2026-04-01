"""
测试风格管理器服务
"""
import pytest
from app.models.dialogue import DialogueStyle
from app.services.style_manager import StyleManager


class TestStyleManager:
    """测试风格管理器"""

    def test_style_manager_creation(self):
        """测试风格管理器创建"""
        manager = StyleManager()
        assert manager is not None

    def test_get_style_template_formal(self):
        """测试获取正式风格模板"""
        manager = StyleManager()
        template = manager.get_style_template(DialogueStyle.FORMAL)
        assert template["sentence_structure"] == "complex"
        assert template["vocabulary"] == "sophisticated"
        assert template["contractions"] is False
        assert template["filler_words"] is False

    def test_get_style_template_casual(self):
        """测试获取随意风格模板"""
        manager = StyleManager()
        template = manager.get_style_template(DialogueStyle.CASUAL)
        assert template["sentence_structure"] == "simple"
        assert template["vocabulary"] == "everyday"
        assert template["contractions"] is True
        assert template["filler_words"] is True

    def test_get_style_template_emotional(self):
        """测试获取情感风格模板"""
        manager = StyleManager()
        template = manager.get_style_template(DialogueStyle.EMOTIONAL)
        assert template["sentence_structure"] == "varied"
        assert template["vocabulary"] == "expressive"
        assert template["contractions"] is True
        assert template["filler_words"] is False

    def test_get_style_template_humorous(self):
        """测试获取幽默风格模板"""
        manager = StyleManager()
        template = manager.get_style_template(DialogueStyle.HUMOROUS)
        assert template["sentence_structure"] == "punchy"
        assert template["vocabulary"] == "witty"
        assert template["contractions"] is True
        assert template["filler_words"] is True

    def test_get_style_template_serious(self):
        """测试获取严肃风格模板"""
        manager = StyleManager()
        template = manager.get_style_template(DialogueStyle.SERIOUS)
        assert template["sentence_structure"] == "measured"
        assert template["vocabulary"] == "precise"
        assert template["contractions"] is False
        assert template["filler_words"] is False

    def test_blend_styles(self):
        """测试混合风格"""
        manager = StyleManager()
        blended = manager.blend_styles(
            [DialogueStyle.FORMAL, DialogueStyle.CASUAL],
            [0.7, 0.3]
        )
        assert "sentence_structure" in blended
        assert "vocabulary" in blended
        assert blended["contractions"] is False

    def test_blend_styles_equal_weights(self):
        """测试等权重混合风格"""
        manager = StyleManager()
        blended = manager.blend_styles(
            [DialogueStyle.EMOTIONAL, DialogueStyle.HUMOROUS],
            [0.5, 0.5]
        )
        assert blended is not None
        assert isinstance(blended, dict)

    def test_get_all_templates(self):
        """测试获取所有模板"""
        manager = StyleManager()
        templates = manager.get_all_templates()
        assert DialogueStyle.FORMAL in templates
        assert DialogueStyle.CASUAL in templates
        assert DialogueStyle.EMOTIONAL in templates
        assert DialogueStyle.HUMOROUS in templates
        assert DialogueStyle.SERIOUS in templates
