# FitBuddy - AI Fitness Plan Generator

FitBuddy is an AI-powered fitness planning web application built with:

- FastAPI
- Python
- Jinja2
- SQLite
- SQLAlchemy
- Google Gemini
- HTML
- CSS

## Features

- Personalized 7-day workout plan
- Fitness goals:
  - Weight Loss
  - Muscle Gain
  - General Wellness
  - Flexibility
  - Strength
- Workout intensity:
  - Low
  - Medium
  - High
- Nutrition/recovery tip
- AI feedback-based plan updates
- SQLite database
- Admin dashboard
- Delete users
- REST API
- Swagger API documentation
- Demo mode without Gemini API
- Responsive frontend

---

# Project Structure

```text
FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── static/
│   └── css/
│       └── style.css
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
