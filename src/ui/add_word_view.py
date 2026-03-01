import customtkinter as ctk

class AddWordView(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.title_label = ctk.CTkLabel(self, text="Add New Word", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        self._add_field("Word:", 1, "word_entry")
        self._add_field("Definition:", 2, "definition_entry")
        self._add_field("Translation:", 3, "translation_entry")
        self._add_field("Example Sentence:", 4, "example_entry")
        self._add_field("Phonetics:", 5, "phonetics_entry")
        
        self.save_button = ctk.CTkButton(self, text="Save Word", command=self.save_word)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=30)
        
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=7, column=0, columnspan=2)
        
    def _add_field(self, label_text, row, attr_name):
        label = ctk.CTkLabel(self, text=label_text, anchor="e")
        label.grid(row=row, column=0, padx=20, pady=10, sticky="e")
        entry = ctk.CTkEntry(self, width=300)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")
        setattr(self, attr_name, entry)
        
    def save_word(self):
        word = self.word_entry.get().strip()
        if not word:
            self.status_label.configure(text="Word field is required!", text_color="red")
            return
            
        word_data = {
            "word": word,
            "definition": self.definition_entry.get().strip(),
            "translation": self.translation_entry.get().strip(),
            "example_sentence": self.example_entry.get().strip(),
            "phonetics": self.phonetics_entry.get().strip()
        }
        
        try:
            self.db.add_word(word_data)
            self.status_label.configure(text=f"Successfully added '{word}'!", text_color="green")
            # Clear fields
            self.word_entry.delete(0, 'end')
            self.definition_entry.delete(0, 'end')
            self.translation_entry.delete(0, 'end')
            self.example_entry.delete(0, 'end')
            self.phonetics_entry.delete(0, 'end')
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
