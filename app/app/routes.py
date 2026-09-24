from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)
from app.gemini_generator import (
    generate_workout_gemini,
)
from app.models import User
from app.schemas import (
    FeedbackRequest,
    UserInput,
)
from app.updated_plan import (
    update_workout_plan,
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "FitBuddy - AI Fitness Plan Generator"
        }
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_input = UserInput(
            username=username.strip(),
            user_id=user_id.strip(),
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"Invalid input: {exc}",
                "form": {
                    "username": username,
                    "user_id": user_id,
                    "age": age,
                    "weight": weight,
                    "goal": goal,
                    "intensity": intensity,
                }
            },
            status_code=400,
        )

    existing_user = (
        db.query(User)
        .filter(
            User.user_id == user_input.user_id
        )
        .first()
    )

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": (
                    f"User ID '{user_input.user_id}' already exists. "
                    "Please use another User ID."
                ),
                "form": {
                    "username": user_input.username,
                    "user_id": user_input.user_id,
                    "age": user_input.age,
                    "weight": user_input.weight,
                    "goal": user_input.goal,
                    "intensity": user_input.intensity,
                }
            },
            status_code=400,
        )

    workout_plan = generate_workout_gemini(
        username=user_input.username,
        age=user_input.age,
        weight=user_input.weight,
        goal=user_input.goal,
        intensity=user_input.intensity,
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=user_input.goal
    )

    user = User(
        user_id=user_input.user_id,
        username=user_input.username,
        age=user_input.age,
        weight=user_input.weight,
        goal=user_input.goal,
        intensity=user_input.intensity,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "updated": False,
        }
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        feedback_request = FeedbackRequest(
            user_id=user_id.strip(),
            feedback=feedback.strip(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid feedback: {exc}"
        )

    user = (
        db.query(User)
        .filter(
            User.user_id == feedback_request.user_id
        )
        .first()
    )

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": (
                    f"No user found with User ID "
                    f"'{feedback_request.user_id}'."
                )
            },
            status_code=404,
        )

    revised_plan = update_workout_plan(
        original_plan=user.original_plan,
        feedback=feedback_request.feedback,
    )

    user.updated_plan = revised_plan
    user.feedback = feedback_request.feedback

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "workout_plan": revised_plan,
            "nutrition_tip": user.nutrition_tip,
            "updated": True,
            "feedback": feedback_request.feedback,
        }
    )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )


@router.post(
    "/delete-user/{user_id}"
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    db.delete(user)
    db.commit()

    return RedirectResponse(
        url="/view-all-users",
        status_code=303,
    )


@router.get(
    "/api/users"
)
def api_users(
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "user_id": user.user_id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan": user.original_plan,
            "updated_plan": user.updated_plan,
            "feedback": user.feedback,
            "nutrition_tip": user.nutrition_tip,
            "created_at": (
                user.created_at.isoformat()
                if user.created_at
                else None
            ),
        }
        for user in users
    ]


@router.get(
    "/api/users/{user_id}"
)
def api_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "id": user.id,
        "user_id": user.user_id,
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "original_plan": user.original_plan,
        "updated_plan": user.updated_plan,
        "feedback": user.feedback,
        "nutrition_tip": user.nutrition_tip,
        "created_at": (
            user.created_at.isoformat()
            if user.created_at
            else None
        ),
    }


@router.get(
    "/health"
)
def health_check():
    return {
        "status": "healthy",
        "application": "FitBuddy",
    }
