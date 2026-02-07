"""Script to migrate questions table to add attachment fields."""
from app.db.session import SessionLocal
from app.db.base import Base, engine
# Import Question model to ensure it's registered with Base.metadata
from app.db.models import Question
from sqlalchemy import text


def migrate_question_attachments():
    """Add attachment fields to the questions table if they don't exist."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MIGRATING QUESTIONS TABLE - ADDING ATTACHMENT FIELDS")
        print("=" * 80)
        print("\nAdding attachment fields to questions table...")
        
        # Check which columns already exist
        inspector_result = db.execute(text(
            "SELECT name FROM pragma_table_info('questions')"
        ))
        existing_columns = [row[0] for row in inspector_result.fetchall()]
        
        if "attachment_path" not in existing_columns:
            try:
                print("  [+] Adding column: attachment_path")
                db.execute(text("ALTER TABLE questions ADD COLUMN attachment_path VARCHAR(500)"))
                db.commit()
                print("  [SUCCESS] attachment_path column added")
            except Exception as e:
                print(f"  [X] Error adding column attachment_path: {e}")
                db.rollback()
        else:
            print("  [-] Column attachment_path already exists, skipping")
        
        if "attachment_filename" not in existing_columns:
            try:
                print("  [+] Adding column: attachment_filename")
                db.execute(text("ALTER TABLE questions ADD COLUMN attachment_filename VARCHAR(255)"))
                db.commit()
                print("  [SUCCESS] attachment_filename column added")
            except Exception as e:
                print(f"  [X] Error adding column attachment_filename: {e}")
                db.rollback()
        else:
            print("  [-] Column attachment_filename already exists, skipping")
        
        print("\n[SUCCESS] Migration complete!")
        print("\nThe questions table has been extended with:")
        print("  - attachment_path (String, nullable) - Path to uploaded file")
        print("  - attachment_filename (String, nullable) - Original filename")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        db.rollback()
        print("\nYou may need to manually add the columns or recreate the table.")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_question_attachments()
