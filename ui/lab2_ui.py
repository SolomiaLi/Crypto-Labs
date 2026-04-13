import customtkinter as ctk
from tkinter import filedialog
import os
from labs import lab2

FRAME_COLOR = "#FFE4E1"
BUTTON_COLOR = "#FFB6C1"
HOVER_COLOR = "#FF69B4"
TEXT_COLOR = "#5C4033"

class Lab2Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.label = ctk.CTkLabel(self, text="🎀 MD5 Hash & Integrity 🎀", font=("Comic Sans MS", 26, "bold"), text_color=TEXT_COLOR)
        self.label.pack(pady=10)

        self.text_frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=15)
        self.text_frame.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(self.text_frame, text="1. Хешування повідомлення (Тексту):", text_color=TEXT_COLOR, font=("Arial", 14, "bold")).pack(pady=(10, 5))

        text_inner = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        text_inner.pack(fill="x", padx=20, pady=5)

        self.entry_text = ctk.CTkEntry(text_inner, placeholder_text="Введіть текст для хешування...",
                                       fg_color="white", text_color="black", width=400)
        self.entry_text.pack(side="left", padx=(0, 10), expand=True, fill="x")

        btn_hash_text = ctk.CTkButton(text_inner, text="HASH TEXT", command=self.hash_text,
        fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 12, "bold"))
        btn_hash_text.pack(side="right")

        self.file_frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=15)
        self.file_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(self.file_frame, text="2. Хешування файлу та перевірка цілісності:",
                     text_color=TEXT_COLOR, font=("Arial", 14, "bold")).pack(pady=(10, 5))

        self.entry_expected_hash = ctk.CTkEntry(self.file_frame,
        placeholder_text="Еталонний MD5 хеш (тільки для перевірки цілісності)", fg_color="white", text_color="black")
        self.entry_expected_hash.pack(padx=20, pady=5, fill="x")

        file_inner = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        file_inner.pack(fill="x", padx=20, pady=10)

        btn_style = {"fg_color": "#B0E0E6", "hover_color": "#87CEEB", "text_color": TEXT_COLOR,
                     "font": ("Arial", 12, "bold"), "height": 35}

        self.btn_hash_file = ctk.CTkButton(file_inner, text="📁 GET FILE HASH", command=self.hash_file, **btn_style)
        self.btn_hash_file.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.btn_verify_file = ctk.CTkButton(file_inner, text="🛡️ VERIFY INTEGRITY", command=self.verify_file,
                                             **btn_style)
        self.btn_verify_file.pack(side="right", expand=True, fill="x")

        self.result_box = ctk.CTkTextbox(self, fg_color="white", text_color="black", corner_radius=15, font=("Consolas", 13))
        self.result_box.pack(padx=10, pady=5, fill="both", expand=True)

        self.btn_save_log = ctk.CTkButton(self, text="💾 ЗБЕРЕГТИ РЕЗУЛЬТАТИ В ФАЙЛ", command=self.save_log,
        fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 12, "bold"))
        self.btn_save_log.pack(pady=10)

    def write_to_log(self, text):
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")

    def hash_text(self):
        text = self.entry_text.get()

        try:
            result = lab2.get_string_hash(text)
            self.write_to_log(f"Текст: '{text}'\n MD5:  {result.upper()}\n" + "-" * 40)
        except Exception as e:
            self.write_to_log(f"❌ Помилка хешування: {e}")

    def hash_file(self):
        filepath = filedialog.askopenfilename(title="Оберіть файл для хешування")
        if not filepath:
            return

        filename = os.path.basename(filepath)
        self.write_to_log(f"⏳ Рахую хеш для файлу: {filename}...")
        self.update()

        try:
            result = lab2.get_file_hash(filepath)
            self.write_to_log(f"📁 Файл: {filename}\n🔑 MD5:  {result.upper()}\n" + "-" * 40)
        except Exception as e:
            self.write_to_log(f"❌ Помилка читання файлу: {e}")

    def verify_file(self):
        expected = self.entry_expected_hash.get().strip()
        if not expected:
            self.write_to_log("❌ Помилка: Введіть еталонний хеш для порівняння!")
            return

        filepath = filedialog.askopenfilename(title="Оберіть файл для перевірки")
        if not filepath:
            return

        filename = os.path.basename(filepath)
        self.write_to_log(f"🛡️ Перевірка цілісності файлу: {filename}...")
        self.update()

        try:
            actual = lab2.get_file_hash(filepath)
            self.write_to_log(f"   Очікуваний: {expected.upper()}")
            self.write_to_log(f"   Фактичний:  {actual.upper()}")

            if actual.lower() == expected.lower():
                self.write_to_log("✅ ВИСНОВОК: Цілісність підтверджено! Файл не змінено.\n" + "-" * 40)
            else:
                self.write_to_log("🚨 ВИСНОВОК: УВАГА! Хеші не збігаються. Файл пошкоджено або змінено!\n" + "-" * 40)
        except Exception as e:
            self.write_to_log(f"❌ Помилка: {e}")

    def save_log(self):
        logs = self.result_box.get("1.0", "end-1c")
        if not logs.strip():
            self.write_to_log("⚠️ Немає даних для збереження.")
            return

        try:
            with open("lab2_md5_report.txt", "w", encoding="utf-8") as f:
                f.write("=== ЗВІТ З ЛАБОРАТОРНОЇ РОБОТИ №2 (MD5) ===\n\n")
                f.write(logs)
            self.write_to_log("💾 Успіх: Звіт збережено у 'lab2_md5_report.txt'\n" + "-" * 40)
        except Exception as e:
            self.write_to_log(f"❌ Помилка збереження: {e}")