import pytest
from app.services.world_template_manager import WorldTemplateManager


@pytest.fixture
def template_manager():
    return WorldTemplateManager()


def test_template_manager_creation(template_manager):
    """测试模板管理器创建"""
    assert template_manager is not None


def test_list_templates(template_manager):
    """测试列出模板"""
    templates = template_manager.list_templates()
    assert isinstance(templates, list)
    assert len(templates) > 0


def test_get_template(template_manager):
    """测试获取模板"""
    template = template_manager.get_template("modern_urban")
    assert template is not None
    assert template.get("era") is not None


def test_get_nonexistent_template(template_manager):
    """测试获取不存在的模板"""
    template = template_manager.get_template("nonexistent")
    assert template is None


def test_get_template_for_builder(template_manager):
    """测试获取用于WorldBuilder的模板数据"""
    builder_data = template_manager.get_template_for_builder("modern_urban")
    assert "era" in builder_data
    assert "location" in builder_data
