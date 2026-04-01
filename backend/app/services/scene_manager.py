"""
场景管理器服务
负责场景的创建、更新、张力计算和顺序验证
"""
from typing import Dict, Any, List
from app.models.narrative import Scene, Act, SceneType, SceneCharacter


class SceneManager:
    """场景管理器"""

    def __init__(self):
        """初始化场景管理器"""
        pass

    def create_scene(
        self,
        scene_config: Dict[str, Any],
        act: Act
    ) -> Scene:
        """创建场景并添加到幕中"""
        import uuid

        scene_id = f"scene-{uuid.uuid4().hex[:8]}"\n        characters = []
        for char_config in scene_config.get("characters", []):
            characters.append(SceneCharacter(**char_config))

        scene = Scene(
            scene_id=scene_id,
            scene_type=scene_config.get("scene_type", SceneType.EXPOSITION),
            title=scene_config.get("title", "Untitled"),
            description=scene_config.get("description", ""),
            location=scene_config.get("location", ""),
            characters=characters,
            tension_level=scene_config.get("tension_level", 50.0),
            pacing=scene_config.get("pacing", "normal"),
        )

        act.scenes.append(scene)
        act.updated_at = datetime.now()

        return scene

    def update_scene(
        self,
        scene: Scene,
        updates: Dict[str, Any]
    ) -> Scene:
        """更新场景属性"""
        for key, value in updates.items():
            if hasattr(scene, key):
                setattr(scene, key, value)
        return scene

    def calculate_scene_tension(
        self,
        scene: Scene,
        context: Dict[str, Any]
    ) -> float:
        """计算场景张力（基于事件强度和场景类型)"""
        base_tension = 50.0

        type_tension_map = {
            SceneType.EXPOSITION: 20.0,
            SceneType.RISING_ACTION: 50.0,
            SceneType.CLIMAX: 80.0,
            SceneType.FALLING_ACTION: 40.0,
            SceneType.RESOLUTION: 15.0,
        }

        base_tension = type_tension_map.get(scene.scene_type, 50.0)

        if scene.events:
            avg_event_intensity = sum(event.intensity for event in scene.events) / len(scene.events)
            event_tension = (avg_event_intensity / 10.0) * 30.0
        else:
            event_tension = 0.0

        previous_tension = context.get("previous_tension", 50.0)
        story_progress = context.get("story_progress", 0.5)

        tension = (
            base_tension * 0.4 +
            event_tension * 0.3 +
            previous_tension * 0.2 +
            (story_progress * 100) * 0.1
        )

        return max(0.0, min(100.0, tension)

    def validate_scene_order(
        self,
        scenes: List[Scene]
    ) -> bool:
        """验证场景顺序合理性(exposition -> rising_action -> climax -> falling_action -> resolution)"""
        if not scenes:
            return True

        type_order = {
            SceneType.EXPOSITION: 1,
            SceneType.RISING_ACTION: 2,
            SceneType.CLIMAX: 3,
            SceneType.FALLING_ACTION: 4,
            SceneType.RESOLUTION: 5,
        }

        for i in range(len(scenes) - 1):
            current_order = type_order.get(scenes[i].scene_type, 0)
            next_order = type_order.get(scenes[i + 1].scene_type, 0)

            if next_order < current_order:
                return False

        return True
