import customtkinter as ctk
import struct
import time
from tkinter import filedialog, messagebox
from labs.lab3 import rc5_cbc_pad_encrypt, rc5_cbc_pad_decrypt
from labs.lab2 import MD5
from labs.lab1 import generate_lemer

class Lab3Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        label_font = ("Comic Sans MS", 20, "bold")
        info_font = ("Comic Sans MS", 13)
        text_color = "#5C4033"
        btn_color = "#FFB6C1"
        hover_color = "#FF69B4"
        entry_bg = "#FFF0F5"

        self.label = ctk.CTkLabel(
            self,
            text=" RC5",
            font=label_font,
            text_color=text_color
        )
        self.label.pack(pady=(20, 5))

        self.info_label = ctk.CTkLabel(
            self,
            text="Варіант №6: слово 64 біти, ключ 8 байтів\n",
            font=info_font,
            text_color=text_color
        )
        self.info_label.pack(pady=(0, 20))
        self.input_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.input_container.pack(padx=30, pady=10, fill="x")
        self.pass_label = ctk.CTkLabel(self.input_container, text="🌸 Парольна фраза:", font=("Arial", 12, "bold"), text_color=text_color)
        self.pass_label.pack(pady=(10, 0))

        self.pass_entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text="Введіть секретне слово...",
            width=350,
            height=40,
            show="*",
            fg_color=entry_bg,
            border_color=btn_color,
            text_color=text_color
        )
        self.pass_entry.pack(pady=15, padx=20)
        self.btn_encrypt = ctk.CTkButton(
            self,
            text="🔒 ЗАШИФРУВАТИ ФАЙЛ",
            font=("Arial", 13, "bold"),
            fg_color=btn_color,
            hover_color=hover_color,
            text_color=text_color,
            height=45,
            width=250,
            command=self.process_encrypt
        )
        self.btn_encrypt.pack(pady=10)
        self.btn_decrypt = ctk.CTkButton(
            self,
            text="🔓 РОЗШИФРУВАТИ ФАЙЛ",
            font=("Arial", 13, "bold"),
            fg_color="#FFE4E1",
            hover_color=hover_color,
            text_color=text_color,
            height=45,
            width=250,
            border_width=2,
            border_color=btn_color,
            command=self.process_decrypt
        )
        self.btn_decrypt.pack(pady=10)

    def get_key_from_pass(self, passphrase):
        if not passphrase:
            return None

        md5_engine = MD5()
        md5_engine.update(passphrase.encode('utf-8'))
        hex_result = md5_engine.finalize()
        full_hash_bytes = bytes.fromhex(hex_result)
        return full_hash_bytes[-8:]

    def get_iv(self):
        seed = int(time.time() * 1000) % 1000000

        random_nums = generate_lemer(4, seed=seed)
        iv_bytes = b"".join(struct.pack('<I', num) for num in random_nums)
        return iv_bytes

    def process_encrypt(self):
        passphrase = self.pass_entry.get()
        if not passphrase:
            messagebox.showwarning("Увага", "Будь ласка, введіть пароль! 🌸")
            return

        path = filedialog.askopenfilename(title="Оберіть файл для шифрування")
        if not path: return

        try:
            with open(path, "rb") as f:
                data = f.read()

            key = self.get_key_from_pass(passphrase)
            iv = self.get_iv()
            result = rc5_cbc_pad_encrypt(data, key, iv)

            save_path = filedialog.asksaveasfilename(defaultextension=".enc", title="Зберегти зашифрований файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(result)
                messagebox.showinfo("Успіх", "Файл успішно зашифровано! ✨")
        except Exception as e:
            messagebox.showerror("Помилка", f"Ой! Щось пішло не так:\n{str(e)}")

    def process_decrypt(self):
        passphrase = self.pass_entry.get()
        if not passphrase:
            messagebox.showwarning("Увага", "Введіть пароль для дешифрування! 🌸")
            return

        path = filedialog.askopenfilename(title="Оберіть файл для дешифрування", filetypes=[("Encrypted files", "*.enc")])
        if not path: return

        try:
            with open(path, "rb") as f:
                data = f.read()

            key = self.get_key_from_pass(passphrase)
            result = rc5_cbc_pad_decrypt(data, key)
            save_path = filedialog.asksaveasfilename(title="Зберегти розшифрований файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(result)
                messagebox.showinfo("Успіх", "Файл успішно розшифровано! 🔓")
        except Exception as e:
            messagebox.showerror("Помилка", "Не вдалося розшифрувати. Можливо, пароль невірний? 😿")