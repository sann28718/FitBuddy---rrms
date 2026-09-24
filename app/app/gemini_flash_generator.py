import os

from dotenv import load_dotenv

load_dotenv()


def _demo_nutrition_tip(goal: str) -> str:
    tips = {
        "weight loss": (
            "Prioritize vegetables, lean protein, whole foods and "
            "adequate hydration. Focus on sustainable portions rather "
            "than extreme calorie restriction."
        ),
        "muscle gain": (
            "Include a protein-rich food in each main meal, such as "
            "eggs, chicken, fish, beans, lentils, paneer or Greek yogurt. "
            "Combine this with adequate overall calories and recovery."
        ),
        "general wellness": (
            "Build balanced meals around vegetables or fruit, protein, "
            "whole grains and healthy fats. Stay hydrated throughout "
            "the day."
        ),
        "flexibility": (
            "Stay hydrated and include protein-rich foods and "
            "fruit and vegetables. Adequate recovery supports "
            "consistent mobility training."
        ),
        "strength": (
            "Include adequate protein and nutrient-dense carbohydrates "
            "around training while maintaining good hydration."
        ),
    }

    return tips.get(
        goal.lower(),
        "Stay hydrated and prioritize balanced meals containing protein, vegetables, fruit and whole grains."
    )


def generate_nutrition_tip_with_flash(
    goal: str
) -> str:
    """
    Generate a concise nutrition/recovery tip.
    """

    demo_mode = os.getenv(
        "DEMO_MODE",
        "true"
    ).lower() == "true"

    api_key = os.getenv("GEMINI_API_KEY")

    if demo_mode or not api_key:
        return _demo_nutrition_tip(goal)

    try:
        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        model_name = os.getenv(
            "GEMINI_TIP_MODEL",
            "gemini-2.0-flash"
        )

        prompt = f"""
You are FitBuddy.

Give one concise and practical nutrition or recovery tip
for a person whose fitness goal is:

{goal}

The answer should be 2-4 sentences.

Prefer practical guidance involving:
- hydration
- balanced meals
- protein
- recovery
- fruits and vegetables
- whole foods

Do not provide medical treatment.
Do not recommend extreme diets.

Return only the tip.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        text = getattr(
            response,
            "text",
            None
        )

        if text:
            return text.strip()

        return _demo_nutrition_tip(goal)

    except Exception:
        return _demo_nutrition_tip(goal)
