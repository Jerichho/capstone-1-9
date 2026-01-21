"""Script to verify courses table structure."""
from app.db.session import SessionLocal
from app.db.models import Course
from sqlalchemy import inspect


def verify_courses_table():
    """Verify that the courses table exists and has correct structure."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("VERIFYING COURSES TABLE")
        print("=" * 80)
        
        # Check if table exists by inspecting the engine
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        if 'courses' not in tables:
            print("\n[ERROR] Courses table does not exist!")
            return
        
        print("\n[OK] Courses table exists")
        
        # Get column information
        columns = inspector.get_columns('courses')
        print("\nTable structure:")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"  - {col['name']}: {col['type']} {nullable}{default}")
        
        # Count courses
        course_count = db.query(Course).count()
        print(f"\n[OK] Total courses in database: {course_count}")
        
        # Check foreign key relationship
        fks = inspector.get_foreign_keys('courses')
        if fks:
            print("\nForeign keys:")
            for fk in fks:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error verifying table: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    verify_courses_table()
