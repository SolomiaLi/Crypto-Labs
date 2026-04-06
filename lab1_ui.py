import customtkinter as ctk
import random
import math
from labs import lab1

FRAME_COLOR = "#FFE4E1"
BUTTON_COLOR = "#FFB6C1"
HOVER_COLOR = "#FF69B4"
TEXT_COLOR = "#5C4033"

class Lab1Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.label = ctk.CTkLabel(self, text="🎀 Generator 🎀",
                                  font=("Comic Sans MS", 26, "bold"), text_color=TEXT_COLOR)
        self.label.pack(pady=10)

        self.param_frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=15)
        self.param_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(self.param_frame, text="Налаштування параметрів (залиште пустими для дефолту):",
                     text_color=TEXT_COLOR, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        self.entries = {}
        labels = [("A (multiplier)", "a_entry", lab1.A),
                  ("C (increment)", "c_entry", lab1.C),
                  ("M (modulus)", "m_entry", lab1.M),
                  ("X0 (seed)", "x0_entry", lab1.X0)]

        for i, (text, attr, default) in enumerate(labels):
            ctk.CTkLabel(self.param_frame, text=text, text_color=TEXT_COLOR).grid(row=1, column=i, padx=10)
            entry = ctk.CTkEntry(self.param_frame, placeholder_text=str(default), fg_color="white", text_color="black", width=160)
            entry.grid(row=2, column=i, padx=10, pady=10)
            self.entries[attr] = entry

        self.action_frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=15)
        self.action_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(self.action_frame, text="1. Генерація послідовності", text_color=TEXT_COLOR, font=("Arial", 13, "bold")).pack(pady=(10, 0), padx=20, anchor="w")
        gen_inner = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        gen_inner.pack(fill="x", padx=20, pady=10)

        self.entry_n = ctk.CTkEntry(gen_inner, placeholder_text="Кількість чисел (N)", fg_color="white", text_color="black", width=300)
        self.entry_n.pack(side="left", padx=(0, 10))

        btn_gen = ctk.CTkButton(gen_inner, text="GENERATE", command=self.run_generation, fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 12, "bold"))
        btn_gen.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(self.action_frame, text="2. Аналіз та тести", text_color=TEXT_COLOR, font=("Arial", 13, "bold")).pack(pady=(5, 0), padx=20, anchor="w")
        btn_style = {"fg_color": "#B0E0E6", "hover_color": "#87CEEB", "text_color": TEXT_COLOR, "font": ("Arial", 12, "bold"), "height": 35}

        self.btn_period = ctk.CTkButton(self.action_frame, text="CHECK PERIOD", command=self.run_period, **btn_style)
        self.btn_period.pack(padx=20, pady=5, fill="x")

        self.btn_cesaro = ctk.CTkButton(self.action_frame, text="RUN CESARO TEST", command=self.run_cesaro, **btn_style)
        self.btn_cesaro.pack(padx=20, pady=(5, 15), fill="x")

        self.result_box = ctk.CTkTextbox(self, fg_color="white", text_color=TEXT_COLOR, corner_radius=15, font=("Consolas", 12))
        self.result_box.pack(padx=10, pady=10, fill="both", expand=True)

    def update_params(self):
        try:
            if self.entries["a_entry"].get(): lab1.A = int(self.entries["a_entry"].get())
            if self.entries["c_entry"].get(): lab1.C = int(self.entries["c_entry"].get())
            if self.entries["m_entry"].get(): lab1.M = int(self.entries["m_entry"].get())
            if self.entries["x0_entry"].get(): lab1.X0 = int(self.entries["x0_entry"].get())
        except ValueError:
            self.write_to_log("❌ Помилка: Параметри мають бути цілими числами!")

    def write_to_log(self, text):
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")

    def run_generation(self):
        try:
            self.update_params()
            n = int(self.entry_n.get()) if self.entry_n.get() else 20
            sequence = lab1.generate_lemer(n, seed=lab1.X0)
            self.write_to_log(f"🌸 Послідовність (N={n}):\n{sequence}")
            with open("lab1_results.txt", "w", encoding="utf-8") as f:
                f.write(f"Параметри: A={lab1.A}, C={lab1.C}, M={lab1.M}, X0={lab1.X0}\nРезультат:\n{str(sequence)}")
            self.write_to_log("📁 Результати збережено в 'lab1_results.txt'")
        except Exception as e:
            self.write_to_log(f"❌ Помилка генерації: {e}")

    def run_period(self):
        self.update_params()
        self.write_to_log("⏳ Рахую період...")
        self.update()
        period = lab1.find_period()
        self.write_to_log(f"✨ Період генератора: {period}")
        if period == lab1.M:
            self.write_to_log("✅ Висновок: Період максимальний.")
        else:
            self.write_to_log(f"⚠️ Висновок: Період менший за M.")

    def run_cesaro(self):
        try:
            self.update_params()
            n = int(self.entry_n.get()) if self.entry_n.get() else 1000
            lemer_seq = lab1.generate_lemer(n, seed=lab1.X0)
            lemer_pi = lab1.cesaro_test(lemer_seq)
            system_seq = [random.randint(1, lab1.M) for _ in range(n)]
            system_pi = lab1.cesaro_test(system_seq)
            self.write_to_log(f"📊 Тест Чезаро (N={n}):\n   🍓 Мій Лемер: π ≈ {lemer_pi:.6f}\n   🍏 System:   π ≈ {system_pi:.6f}\n   🎯 Реальне π: {math.pi:.6f}")
            accuracy = max(0, 100 - (abs(math.pi - lemer_pi) / math.pi * 100))
            self.write_to_log(f"✨ Достовірність: {accuracy:.2f}%")
        except Exception as e:
            self.write_to_log(f"❌ Помилка тесту: {e}")