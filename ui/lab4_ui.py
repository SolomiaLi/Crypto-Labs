import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import os
from labs.lab4 import RSACipher

BG_COLOR = "#FFF0F5"
BUTTON_COLOR = "#FFB6C1"
HOVER_COLOR = "#FF69B4"
TEXT_COLOR = "#5C4033"


class Lab4Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.rsa = RSACipher()

        self.lbl_title = ctk.CTkLabel(self, text="🎀 RSA Алгоритм 🎀",
                                      font=("Comic Sans MS", 24, "bold"), text_color=TEXT_COLOR)
        self.lbl_title.pack(pady=20)

        self.frame_keys = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_keys.pack(pady=10, padx=20, fill="x")

        self.lbl_keys = ctk.CTkLabel(self.frame_keys, text="🔑 Управління ключами",
                                     font=("Arial", 16, "bold"), text_color=TEXT_COLOR)
        self.lbl_keys.pack(pady=10)

        self.btn_gen_keys = ctk.CTkButton(self.frame_keys, text="Згенерувати нові ключі (2048 біт)",
                                          command=self.generate_and_save_keys,
                                          fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_gen_keys.pack(pady=5)

        self.btn_load_keys = ctk.CTkButton(self.frame_keys, text="Завантажити ключі (.pem)",
                                           command=self.load_keys,
                                           fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_load_keys.pack(pady=5)

        self.lbl_status = ctk.CTkLabel(self.frame_keys, text="Статус: Ключі відсутні ❌", text_color="red")
        self.lbl_status.pack(pady=10)

        self.frame_files = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=15)
        self.frame_files.pack(pady=20, padx=20, fill="x")

        self.btn_encrypt = ctk.CTkButton(self.frame_files, text="🔒 Зашифрувати файл",
                                         command=self.encrypt_ui,
                                         fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_encrypt.pack(side="left", padx=20, pady=20, expand=True)

        self.btn_decrypt = ctk.CTkButton(self.frame_files, text="🔓 Розшифрувати файл",
                                         command=self.decrypt_ui,
                                         fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.btn_decrypt.pack(side="right", padx=20, pady=20, expand=True)

        self.log_box = ctk.CTkTextbox(self, height=150, fg_color="white", text_color=TEXT_COLOR)
        self.log_box.pack(pady=10, padx=20, fill="x")
        self.log("✨ Система готова до роботи.");

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def generate_and_save_keys(self):
        self.log("⏳ Генерую ключі RSA (2048 біт)... Це може зайняти секунду.")
        self.update()

        self.rsa.generate_keys(2048)

        priv_path = filedialog.asksaveasfilename(title="Зберегти приватний ключ", defaultextension=".pem",
                                                 initialfile="private.pem")
        if not priv_path: return

        pub_path = filedialog.asksaveasfilename(title="Зберегти публічний ключ", defaultextension=".pem",
                                                initialfile="public.pem")
        if not pub_path: return

        self.rsa.save_keys(priv_path, pub_path)
        self.lbl_status.configure(text="Статус: Ключі завантажено (згенеровано) ✅", text_color="green")
        self.log(f"✅ Ключі успішно збережено у:\n- {priv_path}\n- {pub_path}")

    def load_keys(self):
        priv_path = filedialog.askopenfilename(title="Виберіть приватний ключ (private.pem)",
                                               filetypes=[("PEM Files", "*.pem")])
        if not priv_path: return

        try:
            self.rsa.load_private_key(priv_path)
            self.lbl_status.configure(text="Статус: Ключі завантажено ✅", text_color="green")
            self.log(f"✅ Приватний (та публічний) ключ завантажено з: {priv_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")

    def encrypt_ui(self):
        if not self.rsa.public_key:
            messagebox.showwarning("Увага", "Спочатку згенеруйте або завантажте ключі!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть файл для шифрування")
        if not filepath: return

        savepath = filedialog.asksaveasfilename(title="Зберегти зашифрований файл", defaultextension=".enc",
                                                initialfile="secret.enc")
        if not savepath: return

        file_size = os.path.getsize(filepath)
        self.log(f"⏳ Починаю шифрування файлу ({file_size} байт)...")
        self.update()

        start_time = time.time()
        try:
            self.rsa.encrypt_file(filepath, savepath)
            end_time = time.time()
            elapsed = end_time - start_time
            self.log(f"🔒 Файл успішно зашифровано!")
            self.log(f"⏱ Час шифрування (RSA): {elapsed:.4f} секунд.")
        except Exception as e:
            messagebox.showerror("Помилка шифрування", str(e))

    def decrypt_ui(self):
        if not self.rsa.private_key:
            messagebox.showwarning("Увага", "Для розшифрування потрібен приватний ключ!")
            return

        filepath = filedialog.askopenfilename(title="Виберіть зашифрований файл (.enc)")
        if not filepath: return

        savepath = filedialog.asksaveasfilename(title="Зберегти розшифрований файл", defaultextension=".txt",
                                                initialfile="decrypted.txt")
        if not savepath: return

        self.log(f"⏳ Починаю розшифрування файлу...")
        self.update()

        start_time = time.time()
        try:
            self.rsa.decrypt_file(filepath, savepath)
            end_time = time.time()
            elapsed = end_time - start_time
            self.log(f"🔓 Файл успішно розшифровано!")
            self.log(f"⏱ Час розшифрування (RSA): {elapsed:.4f} секунд.")
        except Exception as e:
            messagebox.showerror("Помилка розшифрування", "Невірний ключ або файл пошкоджено.\n" + str(e))