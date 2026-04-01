"""
叙事节奏控制器
负责分析调整叙事节奏
"""
from typing import Dict, Any, List
from app.models.narrative import Story, Scene


class PacingController:
    """叙事节奏控制器"""

    PACING_THRESHOLDS = {
        "slow": {"min": 0, "max": 30},
        "normal": {"min": 30, "max": 70},
        "fast": {"min": 70, "max": 100},
    }

    def __init__(self):
        """初始化节奏控制器"""
        pass

    def analyze_pacing(self, story: Story) -> Dict[str, Any]:
        """分析叙事节奏"""
        scenes = story.get_all_scenes()

        if not scenes:
            return {
                "pacing_score": 50.0,
                "pacing_type": "normal",
                "variation": 0.0,
            }

        pacing_score = self.calculate_pacing_score(scenes)
        pacing_type = self._determine_pacing_type(pacing_score)
        variation = self._calculate_variation(scenes)

        return {
            "pacing_score": pacing_score,
            "pacing_type": pacing_type,
            "variation": variation,
        }

    def adjust_pacing(
        self,
        current_pacing: str,
        target_pacing: str
    ) -> List[str]:
        """生成节奏调整建议"""
        if current_pacing == target_pacing:
            return []

        if current_pacing not in self.PACING_THRESHOLDS or target_pacing not in self.PACING_THRESHOLDS:
            return []

        suggestions = []

        if current_pacing == "slow":
            if target_pacing == "normal":
                suggestions = [
                    "增加场景中的事件密度",
                    "加快对话节奏",
                    "提高场景张力",
                    "减少描述性文字",
                ]
            elif target_pacing == "fast":
                suggestions = [
                    "大幅增加事件密度",
                    "使用短句和快速对话",
                    "提高冲突强度",
                    "减少场景转换时间",
                    "增加动作描写",
                ]
        elif current_pacing == "fast":
            if target_pacing == "normal":
                suggestions = [
                    "减少场景中的事件数量",
                    "放慢对话节奏",
                    "增加描述性文字",
                    "给角色更多内心活动",
                ]
            elif target_pacing == "slow":
                suggestions = [
                    "大幅减少事件密度",
                    "增加环境描写",
                    "放慢叙事节奏",
                    "增加角色反思时间",
                    "使用长句和详细描述",
                ]
        elif current_pacing == "normal":
            if target_pacing == "slow":
                suggestions = [
                    "增加描述性段落",
                    "放慢叙事节奏",
                    "增加环境氛围描写",
                ]
            elif target_pacing == "fast":
                suggestions = [
                    "加快事件推进",
                    "提高对话速度",
                    "增加冲突密度",
                ]

        return suggestions

    def calculate_pacing_score(self, scenes: List[Scene]) -> float:
        """计算节奏得分"""
        if not scenes:
            return 50.0

        if len(scenes) == 1:
            return 50.0

        total_score = 0.0

        for scene in scenes:
            scene_score = scene.tension_level

            if scene.pacing == "fast":
                scene_score *= 1.3
            elif scene.pacing == "slow":
                scene_score *= 0.6

            total_score += scene_score

        average_score = total_score / len(scenes)

        return min(100.0, max(0.0, average_score)

    def detect_pacing_issues(self, story: Story) -> List[Dict[str, Any]]:
        """检测节奏问题"""
        issues = []
        scenes = story.get_all_scenes()

        if not scenes:
            return issues

        if self._is_monotonic_pacing(scenes):
            issues.append({
                "issue_type": "monotonic_pacing",
                "description": "故事节奏过于单调，缺乏变化",
                "severity": "medium",
            })

        if self._is_too_fast_start(scenes):
            issues.append({
                "issue_type": "too_fast_start",
                "description": "故事开头节奏过快,可能影响读者适应",
                "severity": "medium",
            })

        if self._is_too_slow_end(scenes):
            issues.append({
                "issue_type": "too_slow_end",
                "description": "故事结尾节奏过慢,可能影响结局冲击力",
                "severity": "low",
            })

        sudden_changes = self._detect_sudden_pacing_changes(scenes)
        for change in sudden_changes:
            issues.append({
                "issue_type": "sudden_pacing_change",
                "description": f"场景 {change['scene_id']} 节奏突变,从 {change['from']} 到 {change['to']}",
                "severity": "low",
            })

        return issues

    def _determine_pacing_type(self, score: float) -> str:
        """根据得分确定节奏类型"""
        for pacing_type, thresholds in self.PACING_THRESHOLDS.items():
            if thresholds["min"] <= score < thresholds["max"]:
                return pacing_type
        return "fast"

    def _calculate_variation(self, scenes: List[Scene]) -> float:
        """计算节奏变化度"""
        if len(scenes) < 2:
            return 0.0

        variations = []
        for i in range(1, len(scenes))
            prev_score = self._get_scene_pacing_score(scenes[i - 1])
            curr_score = self._get_scene_pacing_score(scenes[i])
            variation = abs(curr_score - prev_score)
            variations.append(variation)

        return sum(variations) / len(variations)

    def _get_scene_pacing_score(self, scene: Scene) -> float:
        """获取单个场景的节奏得分"""
        score = scene.tension_level

        if scene.pacing == "fast":
            score *= 1.3
        elif scene.pacing == "slow":
            score *= 0.6

        return min(100.0, max(0.0, score))

    def _is_monotonic_pacing(self, scenes: List[Scene]) -> bool:
        """检测是否单调节奏"""
        if len(scenes) < 3:
            return False

        pacing_types = set()
        for scene in scenes:
            pacing_types.add(scene.pacing)

        return len(pacing_types) == 1

    def _is_too_fast_start(self, scenes: List[Scene]) -> bool:
        """检测开头是否过快"""
        if not scenes:
            return False

        first_scene = scenes[0]
        return first_scene.pacing == "fast" and first_scene.tension_level > 80

    def _is_too_slow_end(self, scenes: List[Scene]) -> bool:
        """检测结尾是否过慢"""
        if len(scenes) < 2:
            return False

        last_scene = scenes[-1]
        return last_scene.pacing == "slow" and last_scene.tension_level < 30

    def _detect_sudden_pacing_changes(self, scenes: List[Scene]) -> List[Dict[str, Any]]:
        """检测节奏突变"""
        changes = []

        for i in range(1, len(scenes))
            prev_pacing = scenes[i - 1].pacing
            curr_pacing = scenes[i].pacing

            if (prev_pacing == "slow" and curr_pacing == "fast") or \
               (prev_pacing == "fast" and curr_pacing == "slow"):
                changes.append({
                    "scene_id": scenes[i].scene_id,
                    "from": prev_pacing,
                    "to": curr_pacing,
                })

        return changes
