import pytest
import os
from unittest.mock import patch, MagicMock
import sys

# Ensure src module is in path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from ai_tutor import AITutorManager

@pytest.fixture
def manager(monkeypatch):
    """Provides an AITutorManager configured to use mock data."""
    # Force mock behavior via env override
    monkeypatch.setenv("LLM_API_KEY", "your_api_key_here")
    return AITutorManager()

def test_extract_vocabulary_mock(manager):
    """Test extracting vocabulary returns mocked data when use_mock is true."""
    text = "The quick brown fox jumps over the frictionless lazy dog."
    words = manager.extract_vocabulary_from_text(text, target_level="B2")
    
    assert len(words) == 2
    assert words[0]["word"] == "MockWord"
    assert words[1]["word"] == "Frictionless"
    assert "lazy dog" in words[0]["example_sentence"]

def test_extract_vocabulary_empty_text(manager):
    """Test empty text returns empty list."""
    words = manager.extract_vocabulary_from_text("")
    assert words == []

def test_generate_mnemonic_story_mock(manager):
    """Test generating a mnemonic story returns mocked story."""
    words_list = ["apple", "banana"]
    story = manager.generate_mnemonic_story(words_list)
    
    assert "apple" in story
    assert "banana" in story
    assert "happily ever after" in story

def test_generate_mnemonic_story_empty(manager):
    """Test empty word list returns empty string."""
    story = manager.generate_mnemonic_story([])
    assert story == ""
