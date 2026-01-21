from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import User

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    # Plain-text comparison (NO hashing)
    if user.password_hash != password:
        return None

    return user

def create_user(db: Session, email: str, password: str, role: str = "student", 
                first_name: str = "", last_name: str = "", 
                student_id: str = None, instructor_id: str = None):
    """Create a new user account.
    
    Args:
        db: Database session
        email: User email (must be unique)
        password: User password (stored as-is, no hashing)
        role: User role (default: "student")
        first_name: User's first name
        last_name: User's last name
        student_id: Student ID (for students only)
        instructor_id: Instructor ID (for teachers only)
    
    Returns:
        User object if created successfully, None if email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None
    
    # Create new user (plain-text password, no hashing)
    user = User(
        email=email,
        password_hash=password,
        role=role,
        first_name=first_name,
        last_name=last_name,
        student_id=student_id if role == "student" else None,
        instructor_id=instructor_id if role == "teacher" else None
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None