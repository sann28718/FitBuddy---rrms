from typing import Literal

from pydantic import BaseModel, Field


GoalType = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility",
    "strength"
]

IntensityType = Literal[
    "low",
    "medium",
    "high"
]


class UserInput(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=100
    )

    user_id: str = Field(
        min_length=1,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        le=300
    )

    goal: GoalType

    intensity: IntensityType


class FeedbackRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=100
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000
    )
