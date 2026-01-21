"""Script to migrate database to add courses table."""
from app.db.session import SessionLocal
from app.db.base import Base, engine
# Import Course model to ensure it's registered with Base.metadata
from app.db.models import Course


def migrate_courses_table():
    """Create the courses table if it doesn't exist."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MIGRATING DATABASE - ADDING COURSES TABLE")
        print("=" * 80)
        print("\nCreating courses table...")
        
        # Create all tables (Base.metadata.create_all will only create missing tables)
        Base.metadata.create_all(bind=engine)
        
        print("[SUCCESS] Migration complete!")
        print("\nThe courses table has been created with the following structure:")
        print("  - id (Primary Key)")
        print("  - course_number (String)")
        print("  - section (String)")
        print("  - quarter_year (String)")
        print("  - instructor_id (Foreign Key to users)")
        print("  - created_at (Timestamp)")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        print("\nYou may need to manually create the table or check database permissions.")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_courses_table()
