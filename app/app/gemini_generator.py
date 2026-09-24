import os

from dotenv import load_dotenv

load_dotenv()


def _demo_workout(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:
    """
    Offline demonstration workout plan.

    This allows the application to work even when no
    Gemini API key has been configured.
    """

    intensity_text = intensity.capitalize()

    return f"""
FITBUDDY - PERSONALIZED 7-DAY WORKOUT PLAN

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal.title()}
Intensity: {intensity_text}

DAY 1 - FULL BODY
Warm-up:
- 5-10 minutes brisk walking
- Arm circles
- Hip rotations

Main Workout:
- Bodyweight Squats: 3 sets x 12 reps
- Push-ups: 3 sets x 8-12 reps
- Glute Bridges: 3 sets x 15 reps
- Plank: 3 x 30 seconds

Cooldown:
- 5 minutes of gentle stretching

DAY 2 - CARDIO
Warm-up:
- 5 minutes easy walking

Main Workout:
- Brisk walking or light jogging: 25 minutes
- Mountain Climbers: 3 x 20 seconds
- Step-ups: 3 x 12 reps each leg

Cooldown:
- 5-10 minutes stretching

DAY 3 - UPPER BODY
Warm-up:
- Shoulder rotations
- Arm swings
- 5 minutes easy movement

Main Workout:
- Incline Push-ups: 3 x 10
- Dumbbell Rows: 3 x 12
- Shoulder Press: 3 x 10
- Biceps Curls: 3 x 12

Cooldown:
- Chest and shoulder stretches

DAY 4 - RECOVERY
Activity:
- 20-30 minute easy walk
- Gentle full-body mobility
- Light stretching

Focus:
Recovery and flexibility.

DAY 5 - LOWER BODY
Warm-up:
- 5-10 minutes walking
- Dynamic leg movements

Main Workout:
- Squats: 3 x 12
- Reverse Lunges: 3 x 10 each leg
- Glute Bridges: 3 x 15
- Calf Raises: 3 x 15

Cooldown:
- Lower-body stretching

DAY 6 - CARDIO + CORE
Warm-up:
- 5 minutes easy movement

Main Workout:
- Brisk walking/jogging: 20 minutes
- Bicycle Crunches: 3 x 15
- Dead Bug: 3 x 10 each side
- Plank: 3 x 30 seconds

Cooldown:
- Gentle stretching

DAY 7 - REST AND RECOVERY
- Rest from intense training
- Easy walking if comfortable
- Hydration
- 7-9 hours of sleep

INTENSITY NOTE:
The requested intensity is {intensity_text}.
Adjust exercise difficulty according to comfort and experience.

SAFETY NOTE:
This is a general fitness plan and is not a medical prescription.
Stop an exercise if it causes pain and seek professional advice when appropriate.
""".strip()


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:
    """
    Generate a personalized 7-day workout plan using Gemini.

    The project uses Gemini for workout generation as described
    in the supplied project documentation.
    """

    demo_mode = os.getenv(
        "DEMO_MODE",
        "true"
    ).lower() == "true"

    api_key = os.getenv("GEMINI_API_KEY")

    if demo_mode or not api_key:
        return _demo_workout(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
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
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day workout plan.

USER INFORMATION
Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Preferred Intensity: {intensity}

REQUIREMENTS

Create exactly 7 days.

For every day include:

1. Day number and focus
2. Warm-up lasting approximately 5-10 minutes
3. Main workout
4. Exercise names
5. Sets and repetitions OR duration
6. Suggested rest
7. Cooldown/recovery guidance

Include suitable rest/recovery days.

Make the plan practical for a normal user.

Use clear plain text formatting.

Do not provide diagnosis or medical treatment.

Do not claim that the plan replaces a doctor,
physiotherapist, dietitian, or qualified trainer.

If an exercise may not be suitable for everyone,
mention that the user should modify or skip it.

The response must contain only the workout plan.
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

        return _demo_workout(
            username,
            age,
            weight,
            goal,
            intensity
        )

    except Exception:
        # Keep the website functional if Gemini temporarily fails.
        return _demo_workout(
            username,
            age,
            weight,
            goal,
            intensity
        )
