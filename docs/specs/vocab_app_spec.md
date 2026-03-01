# Product Requirements Document (PRD)
## Comprehensive AI-Powered English Learning Hub (Windows)

### 1. Executive Summary & Product Vision
The **Comprehensive AI-Powered English Learning Hub** is a native Windows desktop application built in Python. Evolving from a traditional vocabulary flashcard utility, it is designed to be a holistic, AI-driven language immersion environment. The core differentiator of this product is its seamless integration of Spaced Repetition (the Leitner System) with advanced generative AI. 

Rather than treating Reading, Listening, Writing, and Translation as isolated modules, the Hub uses them as dynamic, contextual review vectors. Every interaction with a target word—whether writing a sentence, conversing with the AI Tutor, or reading a generated story—feeds back into the unified Leitner engine. By making learning highly personalized, gamified, and frictionless, the application transforms vocabulary acquisition from rote memorization into an effortless and engaging daily habit.

### 2. Target Audience
* **English language learners (ESL/EFL)** seeking an immersive, all-in-one desktop environment.
* **Test Prep Students** preparing for standardized exams (e.g., TOEFL, IELTS, GRE, CET-4/6).
* **Professionals** seeking to expand their domain-specific English vocabulary.
* **Privacy-Conscious Power Users** who prefer a dedicated offline-first Windows application capable of leveraging local or self-hosted AI models.

### 3. Functional Requirements

#### 3.1. Word Management & Core Engine
* **[REQ_VOC_001] Add New Word:** The user must be able to add a new flashcard. Mandatory fields: English Word, Definition/Translation. Optional fields: Example Sentence, Phonetic Spelling / Pronunciation Notes.
* **[REQ_VOC_002] Edit Word:** The user must be able to modify the details and metadata of an existing flashcard.
* **[REQ_VOC_003] Delete Word:** The user must be able to remove a flashcard from the database. A standard confirmation dialogue is required to prevent accidental data loss.
* **[REQ_VOC_004] Word List View:** The application must provide a robust, searchable, filterable, and sortable data table of all vocabulary words.
* **[REQ_VOC_005] Bulk Import/Export:** The system must support importing and exporting flashcards via standard CSV or JSON formats to ensure data portability and easy backup.

#### 3.2. Spaced Repetition (Leitner System)
* **[REQ_VOC_006] Leitner Box Architecture:** The core engine must categorize words into distinct progression "boxes" (e.g., Box 1 to Box 5). Newly added words strictly initialize in Box 1.
* **[REQ_VOC_007] Standard Flashcard Review UI:** During a standard manual review, the UI must initially obscure the answer. The user clicks "Show Answer" to reveal the Definition, Example Sentence, and Phonetics.
* **[REQ_VOC_008] Self-Assessment & Progression Logic:** Upon revealing the answer, the user self-assesses recall (e.g., "Correct" / "Incorrect"). 
  * "Correct" advances the card to the next higher box (exponentially increasing the next review interval).
  * "Incorrect" drops the card back to Box 1, enforcing immediate short-term review.
* **[REQ_VOC_009] Daily Review Queue Calculation:** The engine must automatically calculate and present the queue of cards strictly due for review on the current day, based on their respective box intervals (e.g., Box 1 = daily, Box 2 = every 3 days, Box 3 = weekly).

#### 3.3. Dashboard & Analytics
* **[REQ_VOC_010] Main Dashboard UI:** Upon application launch, the user is presented with a high-level summary dashboard of their learning state.
* **[REQ_VOC_011] Vocabulary & Box Metrics:** The dashboard must display: (a) Total vocabulary count, (b) Exact number of words due today, and (c) A visual distribution (e.g., bar chart) showing the number of words residing in each Leitner Box to illustrate mastery progression.
* **[REQ_VOC_012] Study Streak Tracking:** The system must track and display the user's "Study Streak" (consecutive days of clearing the daily review queue) to drive behavioral retention.

#### 3.4. Intelligent Vocabulary Acquisition
* **[REQ_VOC_013] Multi-Vocabulary List Support:** Users must be able to import, select, and manage distinct vocabulary sets (e.g., IELTS, GRE) from localized files for focused study tracks.
* **[REQ_VOC_014] AI-Driven Rich Word Metadata:** When a word is added, the app must allow the AI to automatically populate or enhance comprehensive metadata: Pronunciation symbols, Etymology (Roots/Affixes), Derivatives, Synonyms, Common Collocations, and highly contextual Example Sentences.
* **[REQ_VOC_015] LLM Integration Configuration:** The application must support seamless integration of Large Language Models (LLMs) via an `.env` file, enabling users to plug in proprietary APIs (e.g., OpenAI, Gemini) or local models (e.g., via LM Studio/Ollama).
* **[REQ_VOC_016] Zero-Friction Context Extraction:** 
  * *Description:* AI automatically extracts level-appropriate target words from user-provided text.
  * *UI/UX Flow:* User pastes a YouTube transcript or web article URL/text -> AI parses the content against the user's target difficulty level (e.g., "CET-6") -> System presents a curated list of extracted words -> User clicks "Import Deck," immediately adding them to Box 1.

#### 3.5. AI-Integrated Learning Pillars (The "Active Review" System)
*Crucial PM Note: The following modules are not just practice areas; they act as alternative interfaces for the Leitner Review System. Successful interactions in these modules update the word's Leitner Box status globally.*

* **[REQ_VOC_017] Reading - Dynamic Passage Generation:** 
  * *Description:* AI generates cohesive short reading passages tailored to include the user's "Due Today" words.
  * *Leitner Integration:* Words recognized in context without assistance are marked "Correct".
  * *UI/UX Flow:* User clicks "Generate Daily Reading" -> AI drafts a 300-word story natively integrating 10 due words -> User reads the story. If the user clicks a target word for a hint/translation, it is marked "Incorrect" (Box 1). Words not clicked are marked "Correct" and advance to the next Box.
* **[REQ_VOC_018] Reading - Smart Import & Highlighting:** Users can import external articles. The system automatically cross-references the text with the user's Leitner database, visually highlighting known words (Box 4-5) and currently learning words (Box 1-3) in different colors.
* **[REQ_VOC_019] Listening - Immersive TTS:** Provide seamless, high-quality Text-to-Speech (TTS) for vocabulary pronunciation, example sentences, and full reading passages.
* **[REQ_VOC_020] Listening - Conversational Dialogues:** 
  * *Description:* AI generates conversational audio dialogues featuring "Due Today" vocabulary.
  * *Leitner Integration & UI/UX Flow:* User listens to a 1-minute generated dialogue -> The transcript is hidden -> User completes a quick "Fill-in-the-blank" quiz for the target words -> Correctly spelled/identified words advance in their Leitner boxes; missed words reset to Box 1.
* **[REQ_VOC_021] Writing - AI-Evaluated Sentence Construction:** 
  * *Description:* Users construct sentences using specific target words due for review.
  * *Leitner Integration & UI/UX Flow:* System prompts: "Write a sentence using *Ubiquitous*" -> User types their sentence -> AI evaluates for grammatical correctness, natural phrasing, and semantic accuracy -> AI provides a grade and constructive feedback -> A passing grade advances the Leitner box; failing resets it.
* **[REQ_VOC_022] Translation - Context-Aware Practice:** 
  * *Description:* Users translate AI-generated sentences containing target vocabulary from their native language to English (or vice versa).
  * *Leitner Integration & UI/UX Flow:* User is given a source sentence -> Types the translation -> AI evaluates semantic equivalence and specific usage of the target word -> Success advances the Leitner box.

#### 3.6. Gamification & Immersion
* **[REQ_VOC_023] Gamified Mnemonic Stories (记忆小故事):** 
  * *Description:* The AI dynamically generates highly memorable, absurd, or personalized mnemonic stories specifically targeting "leech words" (words repeatedly failing in Box 1).
  * *UI/UX Flow:* System identifies 5 stubborn Box 1 words -> User clicks "Mnemonic Rescue" -> AI generates a quirky, interconnected micro-story utilizing these exact words to build strong associative memories.
* **[REQ_VOC_024] AI Tutor Chat:** 
  * *Description:* An interactive, open-ended chat interface acting as a dedicated language partner.
  * *Leitner Integration & UI/UX Flow:* The AI dynamically injects "Due Today" vocabulary into its conversational prompts. If the user naturally and correctly utilizes their due target words in their replies, the AI detects the usage, provides positive reinforcement, and automatically advances the word's Leitner box in the background.

### 4. Non-Functional Requirements
* **[REQ_VOC_101] Platform Compatibility:** The application must run natively and flawlessly on Windows 10 and Windows 11.
* **[REQ_VOC_102] Technology Stack:** The core application must be written in Python. The GUI must be developed using a mature, modern framework (e.g., PyQt6, PySide6, or CustomTkinter) to ensure a premium desktop feel.
* **[REQ_VOC_103] Local Data Storage & Offline Capability:** All user data (flashcards, progress, app settings) must be stored locally (e.g., SQLite or local JSON). The application's core functionality and manual reviews must function 100% offline. AI features will fail gracefully or fallback to offline modes if the configured API is unreachable.
* **[REQ_VOC_104] Performance & Responsiveness:** The UI must be highly responsive with sub-100ms interaction latency. Database queries for fetching the daily queue must execute in under 500ms, scaling efficiently for databases exceeding 20,000+ words.

### 5. Future/Out-of-Scope Features (Post-MVP)
* Image and multimedia attachments for visual learners.
* Cloud synchronization across multiple desktop/mobile devices.
* A community marketplace for pre-made, high-quality deck downloads.
* Native mobile companion applications (iOS/Android).