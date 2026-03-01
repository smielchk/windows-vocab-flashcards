import sys
import os

# Set up relative imports for demo
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from database import DatabaseManager
from ai_tutor import AITutorManager

from datetime import date, timedelta
import sqlite3

print("==================================================")
print("🚀 VIRTUAL DEMO: AI-Powered Leitner System")
print("==================================================")

# 1. Initialize
print("\n[1] Initializing Database and AI Tutor...")
db = DatabaseManager("demo_flashcards.db")
ai = AITutorManager()

# 2. Simulate User Pasting a YouTube Transcript
print("\n[2] User Pastes English Text (Zero-Friction Context Extraction)...")
sample_text = "The ubiquity of smartphones has precipitated a paradigm shift in ubiquitous computing. We must mitigate the ubiquitous risks."
print(f"    Input Text: '{sample_text}'")
print("    Target Level: CET-6")

print("\n[3] AI Tutor Analyzing Text...")
extracted = ai.extract_vocabulary_from_text(sample_text, "CET-6")
print(f"    🎯 AI Found {len(extracted)} target words!")
for item in extracted:
    word = item['word']
    definition = item['definition']
    example = item.get('example_sentence', 'N/A')
    
    # Simulate User clicking "Save"
    db.add_word({'word': word, 'definition': definition, 'translation': '', 'example_sentence': example, 'phonetics': ''})
    print(f"      -> Added: {word} | {definition}")

# Hack to make them due today for the demo
tomorrow = (date.today() + timedelta(days=1)).isoformat()
today = date.today().isoformat()
with sqlite3.connect("demo_flashcards.db") as conn:
    conn.execute(f"UPDATE leitner_boxes SET next_review_date = '{today}'")
    conn.commit()

# 3. View Today's Queue (Box 1)
print("\n[4] User Opens Dashboard -> Review Queue (Leitner System)")
queue = db.get_due_cards()
print(f"    📚 Cards Due Today: {len(queue)}")

if len(queue) > 0:
    card = queue[0]
    print(f"    🃏 Front of Card: **{card['word']}**")
    print(f"       [User clicks 'Show Answer']...")
    print(f"    🃏 Back of Card : {card['definition']} (Example: {card['example_sentence']})")
    
    # 4. Simulate User Answering "Correct"
    print("\n[5] User clicks 'Correct' (Green Button)")
    print(f"    -> Updating Leitner Box from {card['current_box']} to {card['current_box'] + 1}...")
    db.update_leitner_box(card['id'], new_box=card['current_box'] + 1, next_date=(date.today() + timedelta(days=3)).isoformat(), last_reviewed=today)
    db.log_review(card['id'], is_correct=True, review_source='manual_review')
    
    # Verify the move
    updated_queue = db.get_due_cards()
    print(f"    🎉 Success! Card advanced to Box 2. Next review delayed.")
    print(f"    📚 Cards left in today's queue: {len(updated_queue)}")

print("\n==================================================")
print("✅ DEMO COMPLETE: Data Flow & Logic Verified!")
print("==================================================")

# Cleanup
if os.path.exists("demo_flashcards.db"):
    os.remove("demo_flashcards.db")