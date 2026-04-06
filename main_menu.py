import customtkinter as ctk
from ui.lab1_ui import Lab1Frame
from ui.lab2_ui import Lab2Frame
from ui.lab3_ui import Lab3Frame
from ui.lab4_ui import Lab4Frame
from ui.lab5_ui import Lab5Frame

BG_COLOR = "#FFF0F5"
SIDEBAR_COLOR = "#FFE4E1"
BUTTON_COLOR = "#FFB6C1"
HOVER_COLOR = "#FF69B4"
TEXT_COLOR = "#5C4033"

class MainMenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎀 Crypto Labs App 🎀")
        self.geometry("1100x800")
        self.configure(fg_color=BG_COLOR)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, fg_color=SIDEBAR_COLOR, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="✨ MY LABS ✨",
                                       font=("Comic Sans MS", 20, "bold"), text_color=TEXT_COLOR)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        side_btn_style = {"fg_color": BUTTON_COLOR, "hover_color": HOVER_COLOR,
                          "text_color": TEXT_COLOR, "font": ("Arial", 13, "bold"), "width": 180}

        self.btn_lab1 = ctk.CTkButton(self.sidebar_frame, text="🌸 Лабораторна №1", command=self.show_lab1, **side_btn_style)
        self.btn_lab1.grid(row=1, column=0, padx=20, pady=10)

        self.btn_lab2 = ctk.CTkButton(self.sidebar_frame, text="🌸 Лабораторна №2", command=self.show_lab2, **side_btn_style)
        self.btn_lab2.grid(row=2, column=0, padx=20, pady=10)

        self.btn_lab3 = ctk.CTkButton(self.sidebar_frame, text="🌸 Лабораторна №3", command=self.show_lab3, **side_btn_style)
        self.btn_lab3.grid(row=3, column=0, padx=20, pady=10)

        self.btn_lab4 = ctk.CTkButton(self.sidebar_frame, text="🌸 Лабораторна №4", command=self.show_lab4, **side_btn_style)
        self.btn_lab4.grid(row=4, column=0, padx=20, pady=10)

        self.btn_lab5 = ctk.CTkButton(self.sidebar_frame, text="🌸 Лабораторна №5", command=self.show_lab5, **side_btn_style)
        self.btn_lab5.grid(row=5, column=0, padx=20, pady=10)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.current_frame = None
        self.show_lab1()

    def show_lab1(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = Lab1Frame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_lab2(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = Lab2Frame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_lab3(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = Lab3Frame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_lab4(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = Lab4Frame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_lab5(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = Lab5Frame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

def start_app():
    app = MainMenuApp()
    app.mainloop()