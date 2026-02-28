import os
import sys
import tempfile
import sqlite3
import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.database import DatabaseManager

# Add staging src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from ai_tutor import AITutorManager

@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing."""
    fd, path = tempfile.mkstemp(suffix='.sqlite')
    os.close(fd)
    yield path
    os.unlink(path)

def test_ai_to_db_integration(temp_db):
    """
    E2E Test to demonstrate:
    1. Initializing DB.
    2. Calling AITutorManager to extract vocabulary.
    3. Adding extracted words to the database.
    4. Retrieving the words to verify integration.
    """
    # 1. Initialize Database
    db_manager = DatabaseManager(temp_db)
    
    # Verify tables created
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert 'flashcards' in tables
    assert 'leitner_boxes' in tables
    conn.close()

    # 2. Extract Vocabulary using AI Tutor
    ai_manager = AITutorManager()
    
    # We expect the mock to be used if not configured
    sample_text = "The system achieved frictionless context extraction in a seamless manner."
    extracted_words = ai_manager.extract_vocabulary_from_text(sample_text, target_level="C1")
    
    assert len(extracted_words) > 0, "AI failed to extract any words."
    
    # 3. Add extracted words to the Database
    added_ids = []
    for word_data in extracted_words:
        word_id = db_manager.add_word(word_data)
        assert word_id > 0
        added_ids.append(word_id)
        
    # 4. Verify insertion
    assert len(added_ids) == len(extracted_words)
    
    # Check if Leitner boxes were initialized
    due_cards = db_manager.get_due_cards()
    # Note: They are due tomorrow, so get_due_cards() without param won't fetch them
    # We should get the word manually
    
    db_word = db_manager.get_word(added_ids[0])
    assert db_word is not None
    assert db_word['word'] == extracted_words[0]['word']
    assert db_word['definition'] == extracted_words[0]['definition']
    
    # 5. Generate a story from the DB words
    words_list = [db_manager.get_word(wid)['word'] for wid in added_ids]
    story = ai_manager.generate_mnemonic_story(words_list)
    
    assert story != ""
    for w in words_list:
        assert w in story
