"""Script to migrate exams table to add exam_difficulty column."""
from app.db.session import SessionLocal
from app.db.base import Base, engine
# Import Exam model to ensure it's registered with Base.metadata
from app.db.models import Exam
from sqlalchemy import text


def migrate_exam_difficulty():
    """Add exam_difficulty column to the exams table if it doesn't exist."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MIGRATING EXAMS TABLE - ADDING EXAM DIFFICULTY FIELD")
        print("=" * 80)
        print("\nAdding exam_difficulty column to exams table...")
        
        # Check which columns already exist
        inspector_result = db.execute(text(
            "SELECT name FROM pragma_table_info('exams')"
        ))
        existing_columns = [row[0] for row in inspector_result.fetchall()]
        
        if "exam_difficulty" in existing_columns:
            print("  [-] Column exam_difficulty already exists, skipping")
        else:
            try:
                print("  [+] Adding column: exam_difficulty")
                db.execute(text("ALTER TABLE exams ADD COLUMN exam_difficulty VARCHAR(80)"))
                db.commit()
                print("  [SUCCESS] exam_difficulty column added")
            except Exception as e:
                print(f"  [X] Error adding column exam_difficulty: {e}")
                db.rollback()
        
        print("\n[SUCCESS] Migration complete!")
        print("\nThe exams table has been extended with:")
        print("  - exam_difficulty (String, nullable) - e.g., 'Undergraduate - Senior', 'Graduate', 'PhD'")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        db.rollback()
        print("\nYou may need to manually add the column or recreate the table.")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_exam_difficulty()
