import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Optional import, fallback to a mock if openai is not installed or key is missing
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AITutorManager:
    def __init__(self, env_path: str = None):
        """
        Initializes the AI Tutor Manager by loading environment variables.
        """
        if env_path:
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()
            
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model_name = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        
        # Determine if we should use actual OpenAI or mock
        self.use_mock = not OPENAI_AVAILABLE or not self.api_key or self.api_key == "your_api_key_here"
        
        if not self.use_mock and self.provider == "openai":
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None

    def extract_vocabulary_from_text(self, text: str, target_level: str = "B2") -> List[Dict[str, str]]:
        """
        Analyzes the given text and extracts vocabulary suitable for the target_level.
        Returns a list of dictionaries with word details:
        [{'word': '...', 'definition': '...', 'translation': '...', 'example_sentence': '...', 'phonetics': '...'}, ...]
        """
        if not text.strip():
            return []

        if self.use_mock:
            # Mocked response for testing/development
            return [
                {
                    "word": "MockWord",
                    "definition": f"A mock definition for testing at {target_level} level.",
                    "translation": "Ein Mock-Wort (German)",
                    "example_sentence": f"This is an example sentence containing MockWord from the text: '{text}'.",
                    "phonetics": "/mɒk wɜːd/"
                },
                {
                    "word": "Frictionless",
                    "definition": "Achieved with or involving little difficulty; effortless.",
                    "translation": "Reibungslos",
                    "example_sentence": "The new context extraction feature is completely frictionless.",
                    "phonetics": "/ˈfrɪkʃənləs/"
                }
            ]
            
        # Actual API call structure
        prompt = (
            f"Extract 2-5 vocabulary words from the following text suitable for a {target_level} English learner. "
            "Return the result ONLY as a JSON array of objects, where each object has these exact keys: "
            "'word', 'definition', 'translation', 'example_sentence', 'phonetics'.\n\n"
            f"Text:\n{text}"
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI English tutor. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"} if "gpt" in self.model_name else None,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            # Safely parse JSON array
            # If the model returned it wrapped in an object like {"words": [...]}, handle it
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "words" in parsed:
                return parsed["words"]
            elif isinstance(parsed, list):
                return parsed
            else:
                # Attempt to extract a list from dictionary values if formatted weirdly
                for val in parsed.values():
                    if isinstance(val, list):
                        return val
                return []
        except Exception as e:
            print(f"Error during AI extraction: {e}")
            return []

    def generate_mnemonic_story(self, words_list: List[str]) -> str:
        """
        Generates a short, memorable story that includes all the words in the words_list.
        """
        if not words_list:
            return ""
            
        words_str = ", ".join(words_list)
        
        if self.use_mock:
            return f"Once upon a time, there were some words: {words_str}. They lived happily ever after in a mock story."

        prompt = (
            f"Create a short, memorable, and slightly absurd mnemonic story "
            f"to help a student remember these words: {words_str}. "
            "Highlight the words in uppercase."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a creative AI memory tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during story generation: {e}")
            return f"Could not generate story for: {words_str}"
