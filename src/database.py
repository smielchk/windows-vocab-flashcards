import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create flashcards table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL,
                    definition TEXT,
                    translation TEXT,
                    example_sentence TEXT,
                    phonetics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create ai_metadata table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flashcard_id INTEGER,
                    roots_affixes TEXT,
                    synonyms TEXT,
                    collocations TEXT,
                    etymology TEXT,
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
                )
            ''')
            
            # Create leitner_boxes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leitner_boxes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flashcard_id INTEGER,
                    current_box INTEGER DEFAULT 1,
                    next_review_date DATE,
                    last_reviewed_date DATE,
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
                )
            ''')
            
            # Create review_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flashcard_id INTEGER,
                    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_correct BOOLEAN,
                    review_source TEXT,
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()

    def add_word(self, word_data: dict) -> int:
        """
        Adds a new word to the flashcards table and initializes its Leitner box.
        word_data should contain: word, definition, translation, example_sentence, phonetics.
        Returns the new flashcard_id.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Insert into flashcards
                cursor.execute('''
                    INSERT INTO flashcards (word, definition, translation, example_sentence, phonetics)
                    VALUES (:word, :definition, :translation, :example_sentence, :phonetics)
                ''', {
                    'word': word_data.get('word'),
                    'definition': word_data.get('definition', ''),
                    'translation': word_data.get('translation', ''),
                    'example_sentence': word_data.get('example_sentence', ''),
                    'phonetics': word_data.get('phonetics', '')
                })
                flashcard_id = cursor.lastrowid
                
                # Initialize Leitner box (Box 1, next review is tomorrow)
                tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
                cursor.execute('''
                    INSERT INTO leitner_boxes (flashcard_id, current_box, next_review_date)
                    VALUES (?, 1, ?)
                ''', (flashcard_id, tomorrow))
                
                conn.commit()
                return flashcard_id
            except sqlite3.IntegrityError:
                raise ValueError(f"Word '{word_data.get('word')}' already exists in the database.")

    def get_due_cards(self, target_date: str = None) -> list:
        """
        Retrieves all flashcards that are due for review on or before target_date.
        If target_date is None, uses today's date.
        """
        if target_date is None:
            target_date = datetime.date.today().isoformat()
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id, f.word, f.definition, f.translation, f.example_sentence, f.phonetics,
                       l.current_box, l.next_review_date
                FROM flashcards f
                JOIN leitner_boxes l ON f.id = l.flashcard_id
                WHERE l.next_review_date <= ?
            ''', (target_date,))
            return [dict(row) for row in cursor.fetchall()]

    def update_leitner_box(self, flashcard_id: int, new_box: int, next_date: str, last_reviewed: str = None):
        """
        Updates the Leitner box and scheduling for a flashcard.
        """
        if last_reviewed is None:
            last_reviewed = datetime.date.today().isoformat()
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE leitner_boxes
                SET current_box = ?, next_review_date = ?, last_reviewed_date = ?
                WHERE flashcard_id = ?
            ''', (new_box, next_date, last_reviewed, flashcard_id))
            conn.commit()

    def log_review(self, flashcard_id: int, is_correct: bool, review_source: str):
        """
        Logs a review event to the review_logs table.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO review_logs (flashcard_id, is_correct, review_source)
                VALUES (?, ?, ?)
            ''', (flashcard_id, is_correct, review_source))
            conn.commit()
            
    def get_word(self, flashcard_id: int) -> dict:
        """
        Retrieves a flashcard by ID.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    def delete_word(self, flashcard_id: int):
        """
        Deletes a flashcard and its associated data (due to CASCADE).
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
            conn.commit()

    def add_ai_metadata(self, flashcard_id: int, metadata: dict):
        """
        Adds or updates AI metadata for a flashcard.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if exists
            cursor.execute('SELECT id FROM ai_metadata WHERE flashcard_id = ?', (flashcard_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE ai_metadata
                    SET roots_affixes = ?, synonyms = ?, collocations = ?, etymology = ?
                    WHERE flashcard_id = ?
                ''', (
                    metadata.get('roots_affixes', ''),
                    metadata.get('synonyms', ''),
                    metadata.get('collocations', ''),
                    metadata.get('etymology', ''),
                    flashcard_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO ai_metadata (flashcard_id, roots_affixes, synonyms, collocations, etymology)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    flashcard_id,
                    metadata.get('roots_affixes', ''),
                    metadata.get('synonyms', ''),
                    metadata.get('collocations', ''),
                    metadata.get('etymology', '')
                ))
            conn.commit()
