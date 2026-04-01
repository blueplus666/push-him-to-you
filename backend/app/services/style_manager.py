"""
对话风格管理器
管理对话风格的模板和混合
"""
from typing import Dict, Any, List

from app.models.dialogue import DialogueStyle


class StyleManager:
    """对话风格管理器"""

    STYLE_TEMPLATES = {
        DialogueStyle.FORMAL: {
            "sentence_structure": "complex",
            "vocabulary": "sophisticated",
            "contractions": False,
            "filler_words": False,
        },
        DialogueStyle.CASUAL: {
            "sentence_structure": "simple",
            "vocabulary": "everyday",
            "contractions": True,
            "filler_words": True,
        },
        DialogueStyle.EMOTIONAL: {
            "sentence_structure": "varied",
            "vocabulary": "expressive",
            "contractions": True,
            "filler_words": False,
        },
        DialogueStyle.HUMOROUS: {
            "sentence_structure": "punchy",
            "vocabulary": "witty",
            "contractions": True,
            "filler_words": True,
        },
        DialogueStyle.SERIOUS: {
            "sentence_structure": "measured",
            "vocabulary": "precise",
            "contractions": False,
            "filler_words": False,
        },
    }

    def get_style_template(self, style: DialogueStyle) -> Dict[str, Any]:
        """获取风格模板"""
        return self.STYLE_TEMPLATES[style]

    def blend_styles(
        self, styles: List[DialogueStyle], weights: List[float]
    ) -> Dict[str, Any]:
        """混合多种风格"""
        blended = {}

        max_weight_idx = weights.index(max(weights))
        dominant_style = styles[max_weight_idx]
        dominant_template = self.STYLE_TEMPLATES[dominant_style]

        for key in ["sentence_structure", "vocabulary"]:
            blended[key] = dominant_template[key]

        for key in ["contractions", "filler_words"]:
            total = sum(
                self.STYLE_TEMPLATES[style].get(key, False) * weight
                for style, weight in zip(styles, weights)
            )
            blended[key] = total / sum(weights)

        return blended

    def get_all_templates(self) -> Dict[DialogueStyle, Dict[str, Any]]:
        """获取所有风格模板"""
        return self.STYLE_TEMPLATES.copy()
