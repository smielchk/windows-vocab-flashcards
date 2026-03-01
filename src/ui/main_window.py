import customtkinter as ctk
from .dashboard_view import DashboardView
from .review_view import ReviewView
from .ai_extract_view import AIExtractView
from .add_word_view import AddWordView

class MainWindow(ctk.CTk):
    def __init__(self, db, ai_tutor=None):
        super().__init__()

        self.db = db
        self.ai_tutor = ai_tutor

        self.title("Vocabulary Flashcards")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Configure dark/light mode and default theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")  # modern blue #1f6aa5

        # --- Grid Layout ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Sidebar Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Vocab App", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Sidebar Navigation Buttons
        self.nav_buttons = {}
        self.btn_dashboard = self._create_nav_button("Dashboard", 1, self.show_dashboard)
        self.btn_review = self._create_nav_button("Review Queue", 2, self.show_review)
        self.btn_add_word = self._create_nav_button("Add Word", 3, self.show_add_word)
        self.btn_ai_extract = self._create_nav_button("AI Extract", 4, self.show_ai_extract)

        # --- Main Content Frame ---
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # --- Initialize Views ---
        self.views = {}
        self.views["Dashboard"] = DashboardView(self.main_container, self.db)
        self.views["Review Queue"] = ReviewView(self.main_container, self.db)
        self.views["Add Word"] = AddWordView(self.main_container, self.db)
        self.views["AI Extract"] = AIExtractView(self.main_container, self.db, self.ai_tutor)

        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        # Show initial view
        self.current_view = None
        self.show_dashboard()

    def _create_nav_button(self, name, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=name, 
            corner_radius=8, 
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            font=ctk.CTkFont(size=16),
            command=command
        )
        btn.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons[name] = btn
        return btn

    def _highlight_button(self, name):
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                # Active styling
                btn.configure(fg_color=("#1f6aa5", "#1f6aa5"), text_color="white")
            else:
                # Inactive styling
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def show_view(self, name):
        if self.current_view:
            self.current_view.grid_remove()
        
        self.current_view = self.views[name]
        self.current_view.grid(row=0, column=0, sticky="nsew")
        
        # Trigger refresh if view supports it
        if hasattr(self.current_view, "refresh"):
            self.current_view.refresh()

        self._highlight_button(name)

    def show_dashboard(self):
        self.show_view("Dashboard")

    def show_review(self):
        self.show_view("Review Queue")

    def show_add_word(self):
        self.show_view("Add Word")

    def show_ai_extract(self):
        self.show_view("AI Extract")