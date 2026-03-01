import os
import sys

# Add the project root to sys.path so 'src' works
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_path)

# Add the staging folder to sys.path so 'ui' resolves
staging_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, staging_path)

import customtkinter as ctk
from src.database import DatabaseManager
from src.ai_tutor import AITutorManager
from ui.main_window import MainWindow

def main():
    print("Initializing Database...")
    db_path = os.path.join(os.path.dirname(__file__), 'flashcards.db')
    db = DatabaseManager(db_path)
    
    print("Initializing AI Tutor...")
    ai_tutor = AITutorManager()
    
    print("Starting GUI...")
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")  
    
    app = MainWindow(db, ai_tutor)
    app.after(1000, lambda: print("GUI initialized successfully!"))
    app.mainloop()

if __name__ == "__main__":
    main()
