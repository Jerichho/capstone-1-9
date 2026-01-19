"""Script to fix student_id column in exams table to be nullable."""
from app.db.session import SessionLocal
from sqlalchemy import text


def fix_student_id_nullable():
    """Make student_id nullable in exams table."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("FIXING STUDENT_ID CONSTRAINT IN EXAMS TABLE")
        print("=" * 80)
        
        # Check current schema
        result = db.execute(text("PRAGMA table_info(exams)"))
        columns = result.fetchall()
        
        student_id_info = None
        for col in columns:
            if col[1] == 'student_id':
                student_id_info = col
                break
        
        if student_id_info is None:
            print("[ERROR] student_id column not found!")
            return
        
        # Check if it's already nullable (SQLite stores NOT NULL as 3rd element, 0 means nullable)
        is_nullable = student_id_info[3] == 0
        
        if is_nullable:
            print("[+] student_id is already nullable. No changes needed.")
            return
        
        print("[!] student_id is currently NOT NULL. Need to recreate table...")
        
        # Get list of existing columns
        existing_column_names = [col[1] for col in columns]
        print(f"\n[INFO] Existing columns: {', '.join(existing_column_names)}")
        
        # SQLite doesn't support ALTER COLUMN to change nullability
        # We need to recreate the table
        
        # Step 0: Clean up any leftover tables from previous failed migration
        try:
            db.execute(text("DROP TABLE IF EXISTS exams_new"))
            db.commit()
            print("\n[+] Cleaned up any leftover tables from previous migration")
        except Exception as e:
            print(f"    [!] Note: {e}")
        
        # Step 1: Create new table with correct schema
        # Note: exam_id, course_number, section, exam_name, quarter_year are NOT NULL per model
        # But we'll make them nullable in the table to allow old data migration, 
        # and new inserts will be validated by the application
        print("\n[+] Creating new table with correct schema...")
        db.execute(text("""
            CREATE TABLE exams_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id VARCHAR(100) UNIQUE,
                course_number VARCHAR(20),
                section VARCHAR(10),
                exam_name VARCHAR(100),
                quarter_year VARCHAR(20),
                instructor_name VARCHAR(200),
                instructor_id INTEGER,
                date_start DATETIME,
                date_end DATETIME,
                date_published DATETIME,
                date_end_availability DATETIME,
                student_id INTEGER,
                status VARCHAR(50) DEFAULT 'in_progress',
                final_grade REAL,
                final_explanation TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(instructor_id) REFERENCES users(id)
            )
        """))
        db.commit()
        print("    [OK] New table created")
        
        # Step 2: Copy data from old table to new table
        # Only copy columns that exist in the old table
        print("\n[+] Copying data from old table...")
        
        # Build column lists dynamically
        columns_to_copy = []
        select_expressions = []
        
        # Always copy id, status, final_grade, final_explanation, created_at, completed_at if they exist
        standard_cols = ['id', 'student_id', 'status', 'final_grade', 'final_explanation', 'created_at', 'completed_at']
        new_cols = ['exam_id', 'course_number', 'section', 'exam_name', 'quarter_year', 
                   'instructor_name', 'instructor_id', 'date_start', 'date_end', 
                   'date_published', 'date_end_availability']
        
        for col in standard_cols + new_cols:
            if col in existing_column_names:
                columns_to_copy.append(col)
                select_expressions.append(col)
            elif col in new_cols:
                # New column doesn't exist in old table, use NULL
                columns_to_copy.append(col)
                select_expressions.append('NULL')
        
        if not columns_to_copy:
            print("    [!] No columns to copy")
        else:
            columns_str = ', '.join(columns_to_copy)
            select_str = ', '.join(select_expressions)
            
            copy_sql = f"""
                INSERT INTO exams_new ({columns_str})
                SELECT {select_str}
                FROM exams
            """
            db.execute(text(copy_sql))
            db.commit()
            print(f"    [OK] Data copied ({len(columns_to_copy)} columns)")
        
        # Step 3: Drop old table
        print("\n[+] Dropping old table...")
        db.execute(text("DROP TABLE exams"))
        db.commit()
        print("    [OK] Old table dropped")
        
        # Step 4: Rename new table
        print("\n[+] Renaming new table...")
        db.execute(text("ALTER TABLE exams_new RENAME TO exams"))
        db.commit()
        print("    [OK] Table renamed")
        
        # Step 5: Recreate indexes
        print("\n[+] Recreating indexes...")
        indexes = [
            ("ix_exams_exam_id", "CREATE INDEX ix_exams_exam_id ON exams(exam_id)"),
            ("ix_exams_course_number", "CREATE INDEX ix_exams_course_number ON exams(course_number)"),
            ("ix_exams_instructor_id", "CREATE INDEX ix_exams_instructor_id ON exams(instructor_id)"),
        ]
        
        for idx_name, idx_sql in indexes:
            try:
                db.execute(text(idx_sql))
                db.commit()
                print(f"    [OK] Index {idx_name} created")
            except Exception as e:
                print(f"    [!] Index {idx_name} may already exist or error: {e}")
        
        print("\n[SUCCESS] Migration complete!")
        print("student_id is now nullable in the exams table.")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    fix_student_id_nullable()
