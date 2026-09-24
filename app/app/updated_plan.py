import os

from dotenv import load_dotenv

load_dotenv()


def _demo_updated_plan(
    original_plan: str,
    feedback: str
) -> str:
    """
    Demonstration fallback for feedback-based updates.
    """

    return f"""
UPDATED FITBUDDY WORKOUT PLAN

The following changes were requested:

"{feedback}"

The existing plan has been adjusted while preserving
the original fitness goal and general structure.

DAY 1 - FULL BODY
- 5-10 minute warm-up
- Squats: 3 x 12
- Push-ups: 3 x 8-12
- Glute Bridges: 3 x 15
- Plank: 3 x 30 seconds
- 5 minute cooldown

DAY 2 - CARDIO
- 5 minute warm-up
- Brisk walking/light jogging: 20-30 minutes
- Core movement: 3 sets
- Stretching

DAY 3 - UPPER BODY
- Push-ups or incline push-ups: 3 x 10
- Rows: 3 x 12
- Shoulder press: 3 x 10
- Light mobility work

DAY 4 - ACTIVE RECOVERY
- Easy walking
- Mobility exercises
- Gentle stretching

DAY 5 - LOWER BODY
- Squats: 3 x 12
- Lunges: 3 x 10 each leg
- Glute bridges: 3 x 15
- Calf raises: 3 x 15

DAY 6 - CARDIO + CORE
- 20 minutes moderate cardio
- Plank: 3 x 30 seconds
- Bicycle crunches: 3 x 15
- Cooldown

DAY 7 - REST
- Full recovery
- Optional easy walk
- Hydration and sleep

FEEDBACK APPLIED:
{feedback}

Original plan was retained in the database for comparison.

SAFETY NOTE:
Adjust or stop exercises that cause pain and seek professional guidance when needed.
""".strip()


def update_workout_plan(
    original_plan: str,
    feedback: str
) -> str:
    """
    Update an existing workout plan based on user feedback.
    """

    demo_mode = os.getenv(
        "DEMO_MODE",
        "true"
    ).lower() == "true"

    api_key = os.getenv("GEMINI_API_KEY")

    if demo_mode or not api_key:
        return _demo_updated_plan(
            original_plan,
            feedback
        )

    try:
        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        model_name = os.getenv(
            "GEMINI_WORKOUT_MODEL",
            "gemini-2.0-flash"
        )

        prompt = f"""
You are FitBuddy.

Update the existing workout plan using the user's feedback.

ORIGINAL PLAN
----------------
{original_plan}
----------------

USER FEEDBACK
----------------
{feedback}
----------------

Instructions:

1. Preserve useful parts of the original plan.
2. Apply the requested changes.
3. Keep a 7-day structure.
4. Include warm-up, workout, rest/recovery and cooldown guidance.
5. Make the requested modifications clear.
6. Do not provide medical treatment.
7. Do not claim the plan replaces a qualified professional.
8. Return only the updated workout plan.
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

        return _demo_updated_plan(
            original_plan,
            feedback
        )

    except Exception:
        return _demo_updated_plan(
            original_plan,
            feedback
        )
