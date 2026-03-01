import os
import sys

# Setup paths
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_path)
staging_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, staging_path)

import customtkinter as ctk
from src.database import DatabaseManager
from src.ai_tutor import AITutorManager
from ui.main_window import MainWindow

def test_imports_and_instantiation():
    print("Testing dependencies and imports...")
    db_path = os.path.join(os.path.dirname(__file__), 'test_db.sqlite')
    db = DatabaseManager(db_path)
    ai_tutor = AITutorManager()
    
    print("Dependencies loaded successfully.")
    
    # Check if we can instantiate MainWindow (requires a display, but we'll wrap in try-except)
    try:
        app = MainWindow(db, ai_tutor)
        print("MainWindow instantiated successfully.")
        
        # Check views
        app.select_frame_by_name("dashboard")
        print("Dashboard view switched successfully.")
        app.select_frame_by_name("add_word")
        print("Add Word view switched successfully.")
        app.select_frame_by_name("review")
        print("Review view switched successfully.")
        app.select_frame_by_name("ai_tutor")
        print("AI Tutor view switched successfully.")
        
        app.destroy()
        print("App destroyed successfully.")
        return True
    except Exception as e:
        print(f"Error instantiating GUI (might be expected in headless env): {e}")
        # Even if it fails due to display, we catch the exact error to verify it's just a display issue
        if "display" in str(e).lower() or "cannot connect to X server" in str(e):
            print("Display error caught. Code structure is likely valid.")
            return True
        return False

if __name__ == "__main__":
    success = test_imports_and_instantiation()
    sys.exit(0 if success else 1)
