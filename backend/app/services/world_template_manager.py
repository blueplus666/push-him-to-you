from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path


class WorldTemplateManager:
    """世界模板管理器"""

    def __init__(self, config_path: str = "config/world_templates.yaml"):
        self.config_path = Path(config_path)
        self._templates: Dict[str, Any] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """加载模板配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self._templates = config.get("templates", {})
        else:
            self._templates = self._get_default_templates()

    def _get_default_templates(self) -> Dict[str, Any]:
        """获取默认模板"""
        return {
            "modern_urban": {
                "name": "现代都市",
                "era": "现代都市",
                "location": "杭州",
                "society_type": "平稳发展型"
            }
        }

    def list_templates(self) -> List[str]:
        """列出所有模板名称"""
        return list(self._templates.keys())

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取指定模板"""
        return self._templates.get(template_id)

    def get_template_for_builder(self, template_id: str) -> Dict[str, Any]:
        """获取用于WorldBuilder的模板数据"""
        template = self.get_template(template_id)
        if not template:
            return {}

        return {
            "era": template.get("era", ""),
            "location": template.get("location", ""),
            "society_type": template.get("society_type", ""),
            "special_settings": ", ".join(template.get("special_settings", []))
        }
