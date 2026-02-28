import pytest
import sqlite3
import datetime
from pathlib import Path
from src.database import DatabaseManager

@pytest.fixture
def db_manager(tmp_path):
    # Use a temporary file for the database
    db_file = tmp_path / "test_vocab.db"
    manager = DatabaseManager(str(db_file))
    return manager

def test_database_initialization(db_manager):
    # Verify tables are created
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert "flashcards" in tables
    assert "ai_metadata" in tables
    assert "leitner_boxes" in tables
    assert "review_logs" in tables

def test_add_word(db_manager):
    word_data = {
        "word": "ubiquitous",
        "definition": "present everywhere",
        "translation": "无处不在的",
        "example_sentence": "Smartphones are ubiquitous.",
        "phonetics": "/juːˈbɪkwɪtəs/"
    }
    
    flashcard_id = db_manager.add_word(word_data)
    assert flashcard_id is not None
    
    # Retrieve and verify
    word = db_manager.get_word(flashcard_id)
    assert word["word"] == "ubiquitous"
    assert word["translation"] == "无处不在的"
    
    # Check Leitner Box initialization
    conn = sqlite3.connect(db_manager.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leitner_boxes WHERE flashcard_id = ?", (flashcard_id,))
    box = cursor.fetchone()
    
    assert box is not None
    assert box["current_box"] == 1
    
    expected_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    assert box["next_review_date"] == expected_tomorrow

def test_add_duplicate_word(db_manager):
    word_data = {"word": "unique"}
    db_manager.add_word(word_data)
    
    with pytest.raises(ValueError, match="already exists"):
        db_manager.add_word(word_data)

def test_get_due_cards(db_manager):
    # Add a word
    fid = db_manager.add_word({"word": "testword"})
    
    # It shouldn't be due today (initially due tomorrow)
    due_today = db_manager.get_due_cards()
    assert len(due_today) == 0
    
    # Force the next review date to yesterday to make it due
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    db_manager.update_leitner_box(fid, new_box=1, next_date=yesterday)
    
    due_today = db_manager.get_due_cards()
    assert len(due_today) == 1
    assert due_today[0]["word"] == "testword"
    assert due_today[0]["current_box"] == 1

def test_update_leitner_box(db_manager):
    fid = db_manager.add_word({"word": "progress"})
    
    future_date = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()
    db_manager.update_leitner_box(fid, new_box=2, next_date=future_date)
    
    conn = sqlite3.connect(db_manager.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leitner_boxes WHERE flashcard_id = ?", (fid,))
    box = cursor.fetchone()
    
    assert box["current_box"] == 2
    assert box["next_review_date"] == future_date
    assert box["last_reviewed_date"] == datetime.date.today().isoformat()

def test_log_review(db_manager):
    fid = db_manager.add_word({"word": "review_me"})
    db_manager.log_review(fid, is_correct=True, review_source="manual")
    
    conn = sqlite3.connect(db_manager.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review_logs WHERE flashcard_id = ?", (fid,))
    log = cursor.fetchone()
    
    assert log is not None
    assert log["is_correct"] == 1 # SQLite stores booleans as 1/0
    assert log["review_source"] == "manual"

def test_add_ai_metadata(db_manager):
    fid = db_manager.add_word({"word": "context"})
    metadata = {
        "roots_affixes": "con- (with), text (weave)",
        "synonyms": "background, situation",
        "collocations": "in the context of",
        "etymology": "Latin contextus"
    }
    
    db_manager.add_ai_metadata(fid, metadata)
    
    conn = sqlite3.connect(db_manager.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ai_metadata WHERE flashcard_id = ?", (fid,))
    row = cursor.fetchone()
    
    assert row is not None
    assert row["roots_affixes"] == "con- (with), text (weave)"
    assert row["synonyms"] == "background, situation"

def test_delete_word_cascade(db_manager):
    fid = db_manager.add_word({"word": "delete_me"})
    db_manager.add_ai_metadata(fid, {"synonyms": "remove"})
    db_manager.log_review(fid, is_correct=True, review_source="manual")
    
    # Delete word
    db_manager.delete_word(fid)
    
    # Verify word is gone
    assert db_manager.get_word(fid) is None
    
    # Verify cascading deletes
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM leitner_boxes WHERE flashcard_id = ?", (fid,))
    assert cursor.fetchone()[0] == 0
    
    cursor.execute("SELECT count(*) FROM ai_metadata WHERE flashcard_id = ?", (fid,))
    assert cursor.fetchone()[0] == 0
    
    cursor.execute("SELECT count(*) FROM review_logs WHERE flashcard_id = ?", (fid,))
    assert cursor.fetchone()[0] == 0