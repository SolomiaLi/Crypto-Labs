import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
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

        self.lbl_title = ctk.CTkLabel(self, text="🎀 Лабораторна №5: Цифровий підпис (DSS) 🎀",
                                      font=("Comic Sans MS", 24, "bold"), text_color=TEXT_COLOR)
        self.lbl_title.pack(pady=10)

        # --- Блок ключів ---
        self.frame_keys = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_keys.pack(pady=5, padx=20, fill="x")

        self.btn_gen_keys = ctk.CTkButton(self.frame_keys, text="Згенерувати ключі",
                                          command=self.generate_and_save_keys,
                                          fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_gen_keys.pack(side="left", padx=20, pady=10, expand=True)

        self.btn_load_keys = ctk.CTkButton(self.frame_keys, text="Завантажити ключі",
                                           command=self.load_keys,
                                           fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_load_keys.pack(side="right", padx=20, pady=10, expand=True)

        self.lbl_status = ctk.CTkLabel(self.frame_keys, text="Статус: Ключі відсутні ❌", text_color="red")
        self.lbl_status.pack(pady=5, side="bottom")

        self.frame_text = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_text.pack(pady=10, padx=20, fill="x")

        self.entry_text = ctk.CTkEntry(self.frame_text, placeholder_text="Введіть текст для підпису...", width=350)
        self.entry_text.pack(pady=10, padx=10)

        self.btn_sign_text = ctk.CTkButton(self.frame_text, text="✍️ Підписати текст",
                                           command=self.sign_text_ui,
                                           fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_sign_text.pack(side="left", padx=20, pady=10, expand=True)

        self.btn_verify_text = ctk.CTkButton(self.frame_text, text="✅ Перевірити текст",
                                             command=self.verify_text_ui,
                                             fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_verify_text.pack(side="right", padx=20, pady=10, expand=True)

        self.frame_files = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_files.pack(pady=10, padx=20, fill="x")

        self.btn_sign = ctk.CTkButton(self.frame_files, text="📄 Підписати файл",
                                      command=self.sign_file_ui,
                                      fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_sign.pack(side="left", padx=20, pady=10, expand=True)

        self.btn_verify = ctk.CTkButton(self.frame_files, text="🔍 Перевірити файл",
                                        command=self.verify_file_ui,
                                        fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_verify.pack(side="right", padx=20, pady=10, expand=True)

        self.log_box = ctk.CTkTextbox(self, height=120, fg_color="white", text_color=TEXT_COLOR)
        self.log_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.log("✨ Модуль ЕЦП (стандарт DSS) готовий до роботи.")

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
        self.log("✅ Ключі DSA успішно згенеровані та збережені.")

    def load_keys(self):
        key_path = filedialog.askopenfilename(title="Виберіть ключ (.pem)", filetypes=[("PEM Files", "*.pem")])
        if not key_path: return

        try:
            try:
                self.signer.load_private_key(key_path)
                self.lbl_status.configure(text="Статус: Приватний ключ завантажено ✅", text_color="green")
                self.log("🔑 Завантажено ПРИВАТНИЙ ключ. Можна підписувати.")
            except ValueError:
                self.signer.load_public_key(key_path)
                self.lbl_status.configure(text="Статус: Публічний ключ завантажено ⚠️", text_color="orange")
                self.log("️ Завантажено ПУБЛІЧНИЙ ключ. Можна лише перевіряти.")
        except Exception as e:
            messagebox.showerror("Помилка1", f"Не вдалося завантажити ключ: {e}")

    def sign_text_ui(self):
        if not self.signer.private_key:
            messagebox.showwarning("Увага1", "Для підпису потрібен приватний ключ!")
            return

        text = self.entry_text.get()
        if not text:
            messagebox.showwarning("Увага2", "Введіть текст для підпису!")
            return

        try:
            sig_hex = self.signer.sign_text(text)
            self.log(f"✍️ Текст підписано! HEX-підпис:\n{sig_hex}\n")

            if messagebox.askyesno("Збереження", "Бажаєте зберегти цей підпис у файл?"):
                sigpath = filedialog.asksaveasfilename(title="Зберегти підпис", defaultextension=".sig",
                                                       initialfile="text.sig")
                if sigpath:
                    with open(sigpath, 'w') as f:
                        f.write(sig_hex)
                    self.log(f"💾 Підпис тексту збережено у: {os.path.basename(sigpath)}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def verify_text_ui(self):
        if not self.signer.public_key:
            messagebox.showwarning("Увага3", "Для перевірки потрібен публічний ключ!")
            return

        text = self.entry_text.get()
        if not text:
            messagebox.showwarning("Увага4", "Введіть текст, який потрібно перевірити!")
            return

        sig_hex = simpledialog.askstring("Перевірка", "Вставте HEX-підпис для цього тексту:")
        if not sig_hex: return

        try:
            is_valid = self.signer.verify_text(text, sig_hex.strip())
            if is_valid:
                self.log("✅ ТЕКСТ СПРАВЖНІЙ: Підпис відповідає введеному тексту!")
                messagebox.showinfo("Успіх", "Підпис валідний!")
            else:
                self.log("❌ ПОМИЛКА: Текст змінено або підпис недійсний!")
                messagebox.showerror("Тривога", "Підпис НЕ дійсний!")
        except Exception as e:
            messagebox.showerror("Помилка", "Некоректний формат HEX-підпису!")

    def sign_file_ui(self):
        if not self.signer.private_key:
            messagebox.showwarning("Увага", "Для підпису потрібен приватний ключ!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть файл для підписання")
        if not filepath: return

        sigpath = filedialog.asksaveasfilename(title="Зберегти файл підпису", defaultextension=".sig",
                                               initialfile="document.sig")
        if not sigpath: return

        try:
            sig_hex = self.signer.sign_file(filepath, sigpath)
            self.log(f"✍️ Файл підписано! Створено печатку: {os.path.basename(sigpath)}")
            self.log(f"HEX підпису файлу:\n{sig_hex}\n")  # Виводимо на екран за вимогою
        except Exception as e:
            messagebox.showerror("Помилка підписання", str(e))

    def verify_file_ui(self):
        if not self.signer.public_key:
            messagebox.showwarning("Увага", "Для перевірки потрібен публічний ключ!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть оригінальний файл")
        if not filepath: return

        sigpath = filedialog.askopenfilename(title="Виберіть файл підпису (.sig)")
        if not sigpath: return

        try:
            is_valid = self.signer.verify_signature(filepath, sigpath)
            if is_valid:
                self.log("✅ ПЕРЕВІРКА ФАЙЛУ УСПІШНА: Документ справжній!")
                messagebox.showinfo("Успіх", "Підпис валідний! Документ справжній.")
            else:
                self.log("❌ ПОМИЛКА: Файл підроблено або підпис не відповідає!")
                messagebox.showerror("Тривога1", "Підпис НЕ дійсний! Файл було змінено.")
        except Exception as e:
            self.log("❌ ПОМИЛКА: Підпис недійсний!")
            messagebox.showerror("Тривога2", "Підпис НЕ дійсний або пошкоджений файл підпису.")