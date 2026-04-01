import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.agents.world_builder import WorldBuilderAgent
from app.agents.base import AgentConfig
from app.services.llm_gateway import LLMGateway
from app.config.llm_config import LLMConfigManager
from app.services.world_template_manager import WorldTemplateManager


@pytest.fixture
def config_manager():
    manager = LLMConfigManager()
    manager.load_config()
    return manager


@pytest.fixture
def llm_gateway(config_manager):
    return LLMGateway(config_manager)


@pytest.fixture
def template_manager():
    return WorldTemplateManager()


@pytest.fixture
def world_builder(llm_gateway):
    config = AgentConfig(
        name="world_builder",
        model="qwen-max",
        temperature=0.8
    )
    return WorldBuilderAgent(config, llm_gateway)


class TestWorldBuilderIntegration:
    """WorldBuilder集成测试"""
    
    def test_template_manager_integration(self, template_manager):
        """测试模板管理器集成"""
        templates = template_manager.list_templates()
        assert len(templates) > 0
        
        template = template_manager.get_template("modern_urban")
        assert template is not None
    
    @pytest.mark.asyncio
    async def test_world_builder_with_template(self, world_builder, template_manager):
        """测试使用模板创建世界"""
        template_data = template_manager.get_template_for_builder("modern_urban")
        
        mock_response = MagicMock()
        mock_response.content = """
## 世界概述
现代都市杭州，江南水乡。

## 社会结构
- 上层：企业家
- 中层：白领
- 底层：工人

## 文化特征
- 核心价值观：勤劳、诚信

## 环境特点
- 自然环境：江南水乡

## 潜在冲突源
- 社会矛盾：贫富差距
"""
        
        with patch.object(world_builder.llm_gateway, 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = mock_response
            
            response = await world_builder.execute(template_data)
            
            assert response.success is True
            assert "world_state" in response.data
    
    def test_full_workflow(self, template_manager):
        """测试完整工作流"""
        # 1. 获取模板
        template = template_manager.get_template("modern_urban")
        assert template is not None
        
        # 2. 转换为Builder输入
        builder_input = template_manager.get_template_for_builder("modern_urban")
        assert builder_input["era"] == "现代都市"
        
        # 3. 验证模板包含必要字段
        assert "era" in builder_input
        assert "location" in builder_input
        assert "society_type" in builder_input
    
    def test_all_templates_valid(self, template_manager):
        """测试所有模板都是有效的"""
        templates = template_manager.list_templates()
        
        for template_id in templates:
            builder_data = template_manager.get_template_for_builder(template_id)
            assert builder_data.get("era"), f"Template {template_id} missing era"
            assert builder_data.get("location"), f"Template {template_id} missing location"
            assert builder_data.get("society_type"), f"Template {template_id} missing society_type"
