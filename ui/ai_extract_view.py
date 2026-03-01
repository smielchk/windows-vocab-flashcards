import customtkinter as ctk
import threading

class AIExtractView(ctk.CTkFrame):
    def __init__(self, master, db, ai_tutor):
        super().__init__(master, fg_color="transparent")
        self.db = db
        self.ai_tutor = ai_tutor
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Title Header
        self.title_label = ctk.CTkLabel(self, text="AI Extract Vocabulary", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="nw", pady=(0, 20))
        
        # Container for text area and controls
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Instructions
        self.instructions_label = ctk.CTkLabel(self.content_frame, text="Paste an article, paragraph, or sentence. The AI will extract key vocabulary automatically.", font=ctk.CTkFont(size=16, text_color="gray"))
        self.instructions_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Modern Text Area
        self.text_area = ctk.CTkTextbox(self.content_frame, font=ctk.CTkFont(size=16), corner_radius=15, fg_color=("#f0f0f0", "#2b2b2b"), border_width=1, border_color=("gray70", "gray40"), wrap="word")
        self.text_area.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Controls Frame (Bottom)
        self.controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, sticky="ew")
        self.controls_frame.grid_columnconfigure(0, weight=1) # Spacer
        self.controls_frame.grid_columnconfigure(1, weight=0) # Button
        
        self.status_label = ctk.CTkLabel(self.controls_frame, text="", font=ctk.CTkFont(size=14, text_color="gray"))
        self.status_label.grid(row=0, column=0, sticky="e", padx=(0, 20))
        
        # Accent-colored "Extract Vocabulary" Button
        self.extract_btn = ctk.CTkButton(
            self.controls_frame, 
            text="Extract Vocabulary", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            height=50, 
            width=220, 
            corner_radius=15,
            fg_color="#1f6aa5", # Accent Color
            hover_color="#144870",
            command=self.on_extract_click
        )
        self.extract_btn.grid(row=0, column=1, sticky="e")
        
    def refresh(self):
        # Clear status on view enter
        self.status_label.configure(text="", text_color="gray")
        
    def on_extract_click(self):
        content = self.text_area.get("1.0", "end-1c").strip()
        if not content:
            self.status_label.configure(text="Please enter some text first.", text_color="#D32F2F")
            return
            
        if not self.ai_tutor:
            self.status_label.configure(text="AI Tutor module is not configured.", text_color="#D32F2F")
            return
            
        self.extract_btn.configure(state="disabled", text="Extracting...")
        self.status_label.configure(text="Analyzing text with AI...", text_color="gray")
        
        # Run AI extraction in background thread to keep UI responsive
        threading.Thread(target=self._run_extraction, args=(content,), daemon=True).start()
        
    def _run_extraction(self, content):
        try:
            # Extract vocabulary
            words = self.ai_tutor.extract_vocabulary_from_text(content, target_level="B2")
            
            if not words:
                self._update_status_ui("No suitable words found.", "#D32F2F")
                return
                
            # Save to Database
            added_count = 0
            for word_data in words:
                try:
                    self.db.add_word(word_data)
                    added_count += 1
                except Exception as e:
                    print(f"Failed to add word '{word_data.get('word')}': {e}")
                    
            self._update_status_ui(f"Successfully added {added_count} words! 🎉", "#388E3C")
            self.text_area.delete("1.0", "end") # Clear text on success
            
        except Exception as e:
            self._update_status_ui(f"Extraction failed: {str(e)}", "#D32F2F")
            
    def _update_status_ui(self, msg, color):
        # Update UI thread-safely
        self.after(0, lambda: self.status_label.configure(text=msg, text_color=color))
        self.after(0, lambda: self.extract_btn.configure(state="normal", text="Extract Vocabulary"))