"""Migration script to create enrollments table."""
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.db.base import Base, engine
from app.db.models import Enrollment

def create_enrollments_table():
    """Create the enrollments table."""
    print("Creating enrollments table...")
    
    try:
        # Create the table
        Base.metadata.create_all(bind=engine, tables=[Enrollment.__table__])
        print("[+] Successfully created enrollments table")
        return True
    except Exception as e:
        print(f"[X] Error creating enrollments table: {e}")
        return False

if __name__ == "__main__":
    create_enrollments_table()
