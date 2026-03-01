# Windows Vocabulary Flashcards
## Comprehensive AI-Powered English Learning Hub

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Framework](https://img.shields.io/badge/GUI-CustomTkinter-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A next-generation, native Windows desktop application designed to transform English vocabulary acquisition from rote memorization into an effortless and engaging daily habit. This application seamlessly integrates **Spaced Repetition (the Leitner System)** with **Advanced Generative AI (LLMs)**.

## 🌟 Key Features

### 1. The Leitner Engine (Spaced Repetition)
- **Scientific Memory Curve**: Words are categorized into 5 mastery boxes.
- **Dynamic Intervals**: Correct answers advance words to longer intervals (1, 3, 7, 14, 30 days). Incorrect answers reset them to Box 1 for immediate review.
- **Daily Review Queue**: Automatically curates your required study list for the day.

### 2. Zero-Friction Context Extraction (AI-Powered)
- Paste any English text (e.g., an article, YouTube transcript, or document).
- The integrated AI Tutor will automatically scan the text and extract target vocabulary tailored to your desired difficulty level (e.g., IELTS, CET-6, TOEFL).
- One-click import directly into your Leitner Box 1.

### 3. Mnemonic Stories & Contextual Learning
- **Gamified Mnemonic Stories**: Select stubborn words you keep forgetting, and the AI will weave them into an absurd, memorable mini-story to build strong neural associations.
- **Rich Metadata Generation**: Automatically fetches phonetics, synonyms, collocations, roots/affixes, and context-aware example sentences.

### 4. Modern & Minimalist UI
- Built with **CustomTkinter** for a beautiful, modern Windows 11 feel.
- Dark mode support, card-based layout, and distraction-free review interface.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/smielchk/windows-vocab-flashcards.git
   cd windows-vocab-flashcards
   ```

2. **Set up the AI Configuration:**
   Copy the example environment file and add your LLM API Key.
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` and set `OPENAI_API_KEY` or your chosen AI provider's key.*

3. **Install Dependencies & Run:**
   Using `uv`, you can install dependencies and run the app in one command:
   ```bash
   uv run main.py
   ```
   *(Alternatively, run `bash run.sh` on Unix-like systems).*

---

## 🏗️ Architecture & Technology Stack
- **Architecture**: Model-View-Controller (MVC)
- **GUI Framework**: `CustomTkinter`
- **Database**: `SQLite3` (100% Offline-First Data Storage)
- **AI Integration**: `openai` python client + `python-dotenv` for local environment management.

## 🤝 Contribution & SOP
This project was scaffolded using an AI **Virtual R&D Team** workflow.
All major changes must adhere to the strict `DEVELOPMENT_WORKFLOW.md` (BA/SA Document -> TDD -> Pre-MR Check -> E2E GUI Demo).