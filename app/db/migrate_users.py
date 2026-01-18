"""Script to migrate users table to add new columns."""
from app.db.session import SessionLocal
from sqlalchemy import text


def migrate_users_table():
    """Add new columns to the users table if they don't exist."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MIGRATING USERS TABLE")
        print("=" * 80)
        print("\nAdding new columns to users table...")
        
        # SQLite syntax for adding columns if they don't exist
        # We'll use a try-catch approach since SQLite doesn't have IF NOT EXISTS for ALTER TABLE
        migrations = [
            ("first_name", "TEXT NOT NULL DEFAULT ''"),
            ("last_name", "TEXT NOT NULL DEFAULT ''"),
            ("student_id", "TEXT"),
            ("instructor_id", "TEXT")
        ]
        
        for column_name, column_def in migrations:
            try:
                # Check if column exists first
                result = db.execute(text(
                    f"SELECT COUNT(*) as count FROM pragma_table_info('users') WHERE name='{column_name}'"
                ))
                exists = result.fetchone()[0] > 0
                
                if not exists:
                    print(f"  [+] Adding column: {column_name}")
                    db.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}"))
                    db.commit()
                else:
                    print(f"  [-] Column {column_name} already exists, skipping")
            except Exception as e:
                print(f"  [X] Error adding column {column_name}: {e}")
                db.rollback()
        
        print("\n[SUCCESS] Migration complete!")
        print("\nNote: Existing users will have empty strings for first_name/last_name")
        print("      and NULL for student_id/instructor_id if they were created before this migration.")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        db.rollback()
        print("\nYou may need to manually add the columns using SQL:")
        print("  ALTER TABLE users ADD COLUMN first_name TEXT NOT NULL DEFAULT '';")
        print("  ALTER TABLE users ADD COLUMN last_name TEXT NOT NULL DEFAULT '';")
        print("  ALTER TABLE users ADD COLUMN student_id TEXT;")
        print("  ALTER TABLE users ADD COLUMN instructor_id TEXT;")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_users_table()
