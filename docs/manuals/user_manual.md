# User Manual - Comprehensive AI-Powered English Learning Hub

Welcome to your personalized, AI-driven English learning experience. This application uses spaced repetition (Leitner System) combined with Generative AI to make vocabulary acquisition effortless.

## 1. Getting Started
1. Launch the application via `uv run main.py`.
2. Upon first launch, ensure your `.env` file is configured with your `OPENAI_API_KEY` for AI features to function.

## 2. Navigation
The left sidebar contains 4 main tabs:
- **Dashboard**: View your total vocabulary count and the number of flashcards due for review today.
- **Add Word**: Manually add a specific word you want to learn.
- **Review Queue**: The core Leitner System. Start reviewing words that are due today.
- **AI Extract**: The zero-friction learning module.

## 3. How to Use "AI Extract" (Zero-Friction Context)
1. Navigate to the **AI Extract** tab.
2. Paste an English article, a YouTube transcript, or any English text into the large text area.
3. Type your target level (e.g., "IELTS", "CET-6", "TOEFL").
4. Click **Extract Vocabulary**. The AI will analyze the text, extract the difficult words, and automatically add them to Box 1 in your review queue, complete with definitions and context sentences from the text.

## 4. How to "Review" Words
1. Go to the **Review Queue** tab.
2. You will see a large flashcard displaying the English word.
3. Think of the definition, then click **Show Answer**.
4. The card will flip, revealing the definition, phonetics, and example sentence.
5. **Self-Assess**:
   - Click **Correct** (Green) if you remembered it. The word will move to a higher box and be reviewed less frequently.
   - Click **Incorrect** (Red) if you forgot. The word will reset to Box 1 for immediate review tomorrow.

## 5. Daily Habits
For optimal results, open the app daily and clear the "Due Today" queue. Consistency is the key to the Leitner Spaced Repetition system.