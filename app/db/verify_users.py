"""Script to verify user fields are being stored in the database."""
from app.db.session import SessionLocal
from app.db.models import User
from tabulate import tabulate


def verify_users():
    """Display all users from the database with their fields."""
    db = SessionLocal()
    
    try:
        # Query all users
        users = db.query(User).all()
        
        if not users:
            print("No users found in the database.")
            print("\nTo test: Create a new account through the signup page at /signup")
            return
        
        print("=" * 80)
        print("USERS IN DATABASE")
        print("=" * 80)
        print(f"\nTotal users: {len(users)}\n")
        
        # Prepare data for table display
        table_data = []
        for user in users:
            table_data.append([
                user.id,
                user.email,
                user.role,
                user.first_name,
                user.last_name,
                user.student_id or "N/A",
                user.instructor_id or "N/A"
            ])
        
        headers = [
            "ID",
            "Email",
            "Role",
            "First Name",
            "Last Name",
            "Student ID",
            "Instructor ID"
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        print("\n" + "=" * 80)
        print("FIELD VERIFICATION")
        print("=" * 80)
        
        # Check for any users missing required fields
        issues = []
        for user in users:
            if not user.first_name:
                issues.append(f"User {user.email} is missing first_name")
            if not user.last_name:
                issues.append(f"User {user.email} is missing last_name")
            if user.role == "student" and not user.student_id:
                issues.append(f"Student {user.email} is missing student_id")
            if user.role == "teacher" and not user.instructor_id:
                issues.append(f"Teacher {user.email} is missing instructor_id")
        
        if issues:
            print("\n[WARNING] Issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n[OK] All users have the required fields populated correctly!")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error querying database: {e}")
        print("\nNote: If you see a column error, you may need to update your database schema.")
        print("The User model was updated with new columns (first_name, last_name, student_id, instructor_id).")
    finally:
        db.close()


if __name__ == "__main__":
    verify_users()
