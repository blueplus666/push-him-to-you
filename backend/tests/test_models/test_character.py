import pytest
from datetime import datetime
from pydantic import ValidationError


def test_character_state_creation():
    from app.models.character import CharacterState

    character = CharacterState(
        character_id="char-001",
        world_id="world-001",
        name="李明",
        gender="male",
        birth_date=datetime(1990, 3, 15),
        age=25.0,
        personality={
            "openness": 75,
            "conscientiousness": 68,
            "extraversion": 45,
            "agreeableness": 82,
            "neuroticism": 35,
        },
        current_state={
            "occupation": "软件工程师",
            "income_level": 4,
            "relationship_status": "single",
        },
        needs={"physiological": 85, "safety": 78, "belonging": 65},
        skills={"technical": ["编程", "数据分析"], "social": ["沟通", "团队协作"]},
        values={"core_values": ["家庭", "自由", "成长"], "life_goal": "成为一名技术专家"},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert character.character_id == "char-001"
    assert character.name == "李明"
    assert character.personality["openness"] == 75


def test_character_personality_validation():
    from app.models.character import CharacterState

    # 测试人格值范围验证
    with pytest.raises(ValidationError):
        CharacterState(
            character_id="char-001",
            world_id="world-001",
            name="李明",
            gender="male",
            birth_date=datetime(1990, 3, 15),
            age=25.0,
            personality={
                "openness": 150,  # 超出范围
                "conscientiousness": 68,
                "extraversion": 45,
                "agreeableness": 82,
                "neuroticism": 35,
            },
            current_state={},
            needs={},
            skills={},
            values={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
