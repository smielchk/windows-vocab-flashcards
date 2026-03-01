import customtkinter as ctk
import datetime

class ReviewView(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")
        self.db = db
        self.current_card = None
        self.due_cards = []
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Review Queue", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.status_label = ctk.CTkLabel(self.header_frame, text="Loading...", font=ctk.CTkFont(size=14, text_color="gray"))
        self.status_label.grid(row=0, column=1, sticky="e", padx=20)
        
        # Flashcard Container (The Card)
        self.card_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=("#f0f0f0", "#2b2b2b"), width=600, height=450)
        self.card_frame.grid(row=1, column=0, padx=40, pady=20)
        self.card_frame.grid_propagate(False) # Keep card size fixed for aesthetics
        
        # Configure card internal grid
        self.card_frame.grid_rowconfigure(0, weight=1) # Top spacer
        self.card_frame.grid_rowconfigure(1, weight=0) # Word
        self.card_frame.grid_rowconfigure(2, weight=0) # Phonetics
        self.card_frame.grid_rowconfigure(3, weight=1) # Spacer between word and back info
        self.card_frame.grid_rowconfigure(4, weight=0) # Back info (definition)
        self.card_frame.grid_rowconfigure(5, weight=0) # Example
        self.card_frame.grid_rowconfigure(6, weight=1) # Bottom spacer
        self.card_frame.grid_columnconfigure(0, weight=1)
        
        # Front of card (Word and Phonetics)
        self.word_label = ctk.CTkLabel(self.card_frame, text="No cards due today!", font=ctk.CTkFont(size=48, weight="bold"))
        self.word_label.grid(row=1, column=0, pady=(20, 5))
        
        self.phonetics_label = ctk.CTkLabel(self.card_frame, text="", font=ctk.CTkFont(size=20, slant="italic", text_color="gray"))
        self.phonetics_label.grid(row=2, column=0)
        
        # Back of card (Definition and Example)
        self.back_info_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.back_info_frame.grid_columnconfigure(0, weight=1)
        
        self.definition_label = ctk.CTkLabel(self.back_info_frame, text="", font=ctk.CTkFont(size=22), wraplength=500, justify="center")
        self.definition_label.grid(row=0, column=0, pady=(10, 20))
        
        self.example_label = ctk.CTkLabel(self.back_info_frame, text="", font=ctk.CTkFont(size=18, slant="italic", text_color="gray"), wraplength=500, justify="center")
        self.example_label.grid(row=1, column=0, pady=(0, 20))
        
        # Controls (Bottom Area)
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, pady=(20, 40))
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        
        self.show_answer_button = ctk.CTkButton(
            self.controls_frame, 
            text="Show Answer", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            height=60, 
            width=250, 
            corner_radius=15,
            fg_color=("#1f6aa5", "#1f6aa5"), # Modern blue
            hover_color="#144870",
            command=self.show_answer
        )
        
        self.incorrect_button = ctk.CTkButton(
            self.controls_frame, 
            text="Incorrect", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            height=60, 
            width=200, 
            corner_radius=15,
            fg_color="#D32F2F", # Prominent Red
            hover_color="#B71C1C", 
            command=lambda: self.handle_answer(False)
        )
        
        self.correct_button = ctk.CTkButton(
            self.controls_frame, 
            text="Correct", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            height=60, 
            width=200, 
            corner_radius=15,
            fg_color="#388E3C", # Prominent Green
            hover_color="#1B5E20", 
            command=lambda: self.handle_answer(True)
        )
        
        self.refresh()
        
    def refresh(self):
        self.load_next_card(fetch_new=True)

    def load_next_card(self, fetch_new=False):
        if fetch_new or not self.due_cards:
            self.due_cards = self.db.get_due_cards()
            
        self.status_label.configure(text=f"{len(self.due_cards)} cards remaining")
            
        if not self.due_cards:
            self.current_card = None
            self.show_empty_state()
            return
            
        # Get the first card
        self.current_card = self.due_cards.pop(0)
        
        # Reset UI for front side
        self.back_info_frame.grid_forget()
        self.incorrect_button.grid_forget()
        self.correct_button.grid_forget()
        
        word_text = self.current_card.get('word', 'Unknown')
        phonetics = self.current_card.get('phonetics', '')
        
        self.word_label.configure(text=word_text)
        self.phonetics_label.configure(text=phonetics if phonetics else "")
        
        self.show_answer_button.grid(row=0, column=0, columnspan=2, padx=20)
        
    def show_answer(self):
        if not self.current_card:
            return
            
        self.show_answer_button.grid_forget()
        
        # Construct back side info
        definition = self.current_card.get('definition', '')
        translation = self.current_card.get('translation', '')
        example = self.current_card.get('example_sentence', '')
        
        # Combine translation and definition if both exist
        full_def = f"{translation} - {definition}" if translation and definition else definition or translation
        
        self.definition_label.configure(text=full_def)
        self.example_label.configure(text=f'"{example}"' if example else '')
        
        # Show back of card
        self.back_info_frame.grid(row=4, column=0, rowspan=2, sticky="nsew", pady=20)
        
        # Show grading buttons (spaced out symmetrically)
        self.incorrect_button.grid(row=0, column=0, padx=(0, 20), sticky="e")
        self.correct_button.grid(row=0, column=1, padx=(20, 0), sticky="w")
        
    def show_empty_state(self):
        self.word_label.configure(text="All done for today! 🎉")
        self.phonetics_label.configure(text="")
        self.back_info_frame.grid_forget()
        self.show_answer_button.grid_forget()
        self.incorrect_button.grid_forget()
        self.correct_button.grid_forget()
        self.status_label.configure(text="0 cards remaining")
        
    def handle_answer(self, is_correct: bool):
        if not self.current_card:
            return
            
        flashcard_id = self.current_card['id']
        current_box = self.current_card.get('current_box', 1)
        
        # Leitner intervals
        intervals = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
        
        if is_correct:
            new_box = min(current_box + 1, 5)
        else:
            new_box = 1
            
        days_to_add = intervals.get(new_box, 1)
        next_date = (datetime.date.today() + datetime.timedelta(days=days_to_add)).isoformat()
        last_reviewed = datetime.date.today().isoformat()
        
        # Update Database
        self.db.update_leitner_box(flashcard_id, new_box, next_date, last_reviewed)
        self.db.log_review(flashcard_id, is_correct, "UI_Leitner")
        
        # Load next
        self.load_next_card()