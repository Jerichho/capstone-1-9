"""Main FastAPI application."""
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from app.api.router import api_router
from app.db.base import Base, engine
from app.db.session import get_db
from app.db.models import User
from app.logging_config import setup_logging

# Import seeding function
from app.db.seed_users import seed_users

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed users if they don’t already exist
seed_users()

# Create FastAPI app
app = FastAPI(
    title="AI Oral Exam Grader",
    description="AI-powered oral exam grading system",
    version="0.1.0"
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
env = Environment(loader=FileSystemLoader("app/templates"))


def render_template(template_name: str, context: dict) -> HTMLResponse:
    """Render a Jinja2 template."""
    template = env.get_template(template_name)
    html_content = template.render(**context)
    return HTMLResponse(content=html_content)

@app.get("/student/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request, db: Session = Depends(get_db)):
    """Student dashboard page with personalized welcome."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Use first_name if available, otherwise fallback to "Student"
    first_name = user.first_name if user.first_name else "Student"
    
    return render_template("student_dashboard.html", {
        "request": request,
        "first_name": first_name
    })

@app.get("/teacher/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(request: Request, db: Session = Depends(get_db)):
    """Teacher dashboard page with personalized welcome."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Use first_name if available, otherwise fallback to "Teacher"
    first_name = user.first_name if user.first_name else "Teacher"
    
    return render_template("teacher_dashboard.html", {
        "request": request,
        "first_name": first_name
    })

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root page - login form."""
    error = request.query_params.get("error", "")
    success = request.query_params.get("success", "")
    return render_template("login.html", {"request": request, "error": error, "success": success})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Signup page - create new account."""
    error = request.query_params.get("error", "")
    return render_template("signup.html", {"request": request, "error": error})


@app.get("/question/{question_id}", response_class=HTMLResponse)
async def question_page(request: Request, question_id: int):
    """Dummy question page for testing login."""
    # You can later render question.html template here
    return render_template("question.html", {"request": request, "question_id": question_id})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)