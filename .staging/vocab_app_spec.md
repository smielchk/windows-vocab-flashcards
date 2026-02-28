# Product Requirements Document (PRD)
## Windows English Vocabulary Flashcard Application

### 1. Product Overview
The **Windows Vocabulary Flashcard App** is a native desktop application built in Python, designed to help users efficiently learn and memorize English vocabulary. It leverages the principles of Spaced Repetition, specifically the Leitner System, to optimize the learning process, ensuring words are reviewed at optimal intervals for long-term retention. 

### 2. Target Audience
* English language learners (ESL/EFL).
* Students preparing for standardized tests (e.g., TOEFL, IELTS, GRE).
* Professionals seeking to expand their English vocabulary.
* Users who prefer an offline, dedicated desktop application over web or mobile apps.

### 3. Functional Requirements

#### 3.1. Word Management
* **[REQ_VOC_001] Add New Word:** The user must be able to add a new flashcard with the following fields: 
  * English Word (Mandatory)
  * Definition/Translation (Mandatory)
  * Example Sentence (Optional)
  * Phonetic Spelling / Pronunciation Notes (Optional)
* **[REQ_VOC_002] Edit Word:** The user must be able to modify the details of an existing flashcard.
* **[REQ_VOC_003] Delete Word:** The user must be able to remove a flashcard from their database. A confirmation prompt should appear before deletion.
* **[REQ_VOC_004] Word List View:** The user must be able to view a searchable and sortable list or table of all their vocabulary words.
* **[REQ_VOC_005] Bulk Import/Export:** The app must support importing and exporting flashcards via standard CSV or JSON files to allow easy backup or sharing.

#### 3.2. Review System (Leitner System / Spaced Repetition)
* **[REQ_VOC_006] Leitner Box Implementation:** The application must categorize words into distinct "boxes" or "levels" (e.g., Box 1 to Box 5). All new words start in Box 1.
* **[REQ_VOC_007] Flashcard Review UI:** During a review session, the UI must initially display only the English Word. The user must click a "Show Answer" button to reveal the Definition, Example Sentence, and Phonetics.
* **[REQ_VOC_008] Self-Assessment:** After revealing the answer, the user must self-assess their recall by selecting either "Correct" or "Incorrect" (or a similar scale like "Easy/Hard").
* **[REQ_VOC_009] Spaced Repetition Logic:** 
  * If the user selects "Correct," the card moves to the next higher box (e.g., Box 1 -> Box 2), increasing the time until the next review.
  * If the user selects "Incorrect," the card drops back to Box 1, requiring a review sooner.
* **[REQ_VOC_010] Daily Review Queue:** The app must automatically calculate and present the queue of cards due for review on the current day based on their current Box interval (e.g., Box 1 = daily, Box 2 = every 3 days, Box 3 = weekly).

#### 3.3. Progress Tracking & Dashboard
* **[REQ_VOC_011] Main Dashboard:** Upon launching, the app must display a dashboard summarizing the current state of learning.
* **[REQ_VOC_012] Total Vocabulary Count:** Display the total number of words in the database.
* **[REQ_VOC_013] Words Due Today:** Display the number of flashcards that need to be reviewed today.
* **[REQ_VOC_014] Box Distribution:** Visually display (e.g., via a bar chart or simple text counters) how many words reside in each Leitner Box, showing the user's mastery progression.
* **[REQ_VOC_015] Study Streak (Optional but Recommended):** Track and display the number of consecutive days the user has completed their due reviews.

### 4. Non-Functional Requirements
* **[REQ_VOC_101] Platform Compatibility:** The app must run natively on Windows 10 and Windows 11.
* **[REQ_VOC_102] Technology Stack:** The application must be written in Python. The GUI should use a mature framework (e.g., PyQt6, PySide6, Tkinter, or CustomTkinter).
* **[REQ_VOC_103] Local Data Storage:** All user data (flashcards, progress, settings) must be stored locally on the user's machine (e.g., using SQLite or JSON). The app must function 100% offline.
* **[REQ_VOC_104] Performance:** The UI must remain responsive and load instantly. Database queries for fetching the daily queue must complete in less than 500ms, even with a database of 10,000+ words.

### 5. Future/Out-of-Scope Features (Post-MVP)
* Audio pronunciation (Text-to-Speech).
* Image attachments for visual learners.
* Cloud synchronization across multiple devices.
* Pre-made deck downloads.