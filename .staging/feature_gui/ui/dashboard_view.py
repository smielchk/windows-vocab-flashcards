import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")
        self.db = db
        
        # Grid layout for content centering
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Dashboard Title
        self.title_label = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 30), sticky="nw")
        
        # Stats container - centered frame
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.grid(row=1, column=0, sticky="n")
        
        self.stats_container.grid_columnconfigure(0, weight=1, uniform="stat")
        self.stats_container.grid_columnconfigure(1, weight=1, uniform="stat")
        
        # Total Vocab Card
        self.total_vocab_frame = ctk.CTkFrame(self.stats_container, corner_radius=15, fg_color=("#e6e6e6", "#2b2b2b"), width=300, height=200)
        self.total_vocab_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.total_vocab_frame.grid_propagate(False)
        self.total_vocab_frame.pack_propagate(False)
        
        self.total_vocab_title = ctk.CTkLabel(self.total_vocab_frame, text="Total Words", font=ctk.CTkFont(size=20, text_color="gray"))
        self.total_vocab_title.pack(pady=(40, 10))
        self.total_vocab_label = ctk.CTkLabel(self.total_vocab_frame, text="0", font=ctk.CTkFont(size=64, weight="bold", text_color=("#1f6aa5", "#2fa572")))
        self.total_vocab_label.pack()
        
        # Due Words Card
        self.due_words_frame = ctk.CTkFrame(self.stats_container, corner_radius=15, fg_color=("#e6e6e6", "#2b2b2b"), width=300, height=200)
        self.due_words_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.due_words_frame.grid_propagate(False)
        self.due_words_frame.pack_propagate(False)
        
        self.due_words_title = ctk.CTkLabel(self.due_words_frame, text="Due Today", font=ctk.CTkFont(size=20, text_color="gray"))
        self.due_words_title.pack(pady=(40, 10))
        self.due_words_label = ctk.CTkLabel(self.due_words_frame, text="0", font=ctk.CTkFont(size=64, weight="bold", text_color=("#1f6aa5", "#2fa572")))
        self.due_words_label.pack()
        
    def refresh(self):
        # Refresh statistics from DB
        try:
            due_cards = self.db.get_due_cards()
            self.due_words_label.configure(text=str(len(due_cards)))
            
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM flashcards")
                total = cursor.fetchone()[0]
                self.total_vocab_label.configure(text=str(total))
        except Exception as e:
            self.total_vocab_label.configure(text="Err")
            print(f"Error fetching total words: {e}")