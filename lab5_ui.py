import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from labs.lab5 import DigitalSignature

BG_COLOR = "#FFF0F5"
BUTTON_COLOR = "#FFB6C1"
HOVER_COLOR = "#FF69B4"
TEXT_COLOR = "#5C4033"


class Lab5Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.signer = DigitalSignature()

        self.lbl_title = ctk.CTkLabel(self, text="🎀 Лабораторна №5: Цифровий підпис (ЕЦП) 🎀",
                                      font=("Comic Sans MS", 24, "bold"), text_color=TEXT_COLOR)
        self.lbl_title.pack(pady=20)

        # --- Блок ключів ---
        self.frame_keys = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_keys.pack(pady=10, padx=20, fill="x")

        self.btn_gen_keys = ctk.CTkButton(self.frame_keys, text="Згенерувати ключі (ЕЦП)",
                                          command=self.generate_and_save_keys,
                                          fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_gen_keys.pack(pady=10)

        self.btn_load_keys = ctk.CTkButton(self.frame_keys, text="Завантажити ключі (.pem)",
                                           command=self.load_keys,
                                           fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_load_keys.pack(pady=5)

        self.lbl_status = ctk.CTkLabel(self.frame_keys, text="Статус: Ключі відсутні ❌", text_color="red")
        self.lbl_status.pack(pady=10)

        # --- Блок роботи з файлами ---
        self.frame_files = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_files.pack(pady=20, padx=20, fill="x")

        self.btn_sign = ctk.CTkButton(self.frame_files, text="✍️ Підписати файл",
                                      command=self.sign_ui,
                                      fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_sign.pack(side="left", padx=20, pady=20, expand=True)

        self.btn_verify = ctk.CTkButton(self.frame_files, text="✅ Перевірити підпис",
                                        command=self.verify_ui,
                                        fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_verify.pack(side="right", padx=20, pady=20, expand=True)

        # --- Логи ---
        self.log_box = ctk.CTkTextbox(self, height=150, fg_color="white", text_color=TEXT_COLOR)
        self.log_box.pack(pady=10, padx=20, fill="x")
        self.log("✨ Модуль ЕЦП готовий до роботи.");

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def generate_and_save_keys(self):
        self.signer.generate_keys(2048)
        priv_path = filedialog.asksaveasfilename(title="Зберегти приватний ключ", defaultextension=".pem",
                                                 initialfile="private_sign.pem")
        if not priv_path: return
        pub_path = filedialog.asksaveasfilename(title="Зберегти публічний ключ", defaultextension=".pem",
                                                initialfile="public_sign.pem")
        if not pub_path: return

        self.signer.save_keys(priv_path, pub_path)
        self.lbl_status.configure(text="Статус: Ключі завантажено ✅", text_color="green")
        self.log("✅ Ключі для підпису успішно згенеровані та збережені.")

    def load_keys(self):
        key_path = filedialog.askopenfilename(title="Виберіть ключ (.pem)", filetypes=[("PEM Files", "*.pem")])
        if not key_path: return

        try:
            # Спробуємо завантажити як приватний, якщо помилка — значить він публічний
            try:
                self.signer.load_private_key(key_path)
                self.lbl_status.configure(text="Статус: Приватний ключ завантажено ✅", text_color="green")
                self.log(f"🔑 Завантажено ПРИВАТНИЙ ключ. Ви можете ПІДПИСУВАТИ файли.")
            except:
                self.signer.load_public_key(key_path)
                self.lbl_status.configure(text="Статус: Публічний ключ завантажено ⚠️", text_color="orange")
                self.log(f"👁️ Завантажено ПУБЛІЧНИЙ ключ. Ви можете лише ПЕРЕВІРЯТИ підписи.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")

    def sign_ui(self):
        if not self.signer.private_key:
            messagebox.showwarning("Увага", "Для підпису потрібен приватний ключ!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть файл для підписання")
        if not filepath: return

        sigpath = filedialog.asksaveasfilename(title="Зберегти файл підпису", defaultextension=".sig",
                                               initialfile="document.sig")
        if not sigpath: return

        try:
            self.signer.sign_file(filepath, sigpath)
            self.log(f"✍️ Файл успішно підписано! Створено печатку: {os.path.basename(sigpath)}")
        except Exception as e:
            messagebox.showerror("Помилка підписання", str(e))

    def verify_ui(self):
        if not self.signer.public_key:
            messagebox.showwarning("Увага", "Для перевірки потрібен публічний ключ!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть оригінальний файл")
        if not filepath: return

        sigpath = filedialog.askopenfilename(title="Виберіть файл підпису (.sig)",
                                             filetypes=[("Signature", "*.sig"), ("All files", "*.*")])
        if not sigpath: return

        try:
            is_valid = self.signer.verify_signature(filepath, sigpath)
            if is_valid:
                self.log("✅ ПЕРЕВІРКА УСПІШНА: Підпис справжній, файл не змінювався!")
                messagebox.showinfo("Успіх", "Підпис валідний! Документ справжній.")
            else:
                self.log("❌ ПОМИЛКА: Файл підроблено або підпис не відповідає файлу!")
                messagebox.showerror("Тривога", "Підпис НЕ дійсний! Файл було змінено.")
        except Exception as e:
            self.log("❌ ПОМИЛКА: Підпис недійсний (InvalidSignature)!")
            messagebox.showerror("Тривога", "Підпис НЕ дійсний! Файл було змінено.")