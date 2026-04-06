import os
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature


class DigitalSignature:
    """Клас для створення та перевірки цифрового підпису за стандартом DSS (DSA)."""

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size=2048):
        """Генерує пару ключів DSA (DSS) для підпису."""
        # Використовуємо алгоритм DSA 
        self.private_key = dsa.generate_private_key(key_size=key_size)
        self.public_key = self.private_key.public_key()

    def save_keys(self, private_path, public_path):
        """Зберігає ключі у форматі PEM."""
        if not self.private_key or not self.public_key:
            raise ValueError("Ключі ще не згенеровані!")

        with open(private_path, 'wb') as f_priv:
            f_priv.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(public_path, 'wb') as f_pub:
            f_pub.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, path):
        """Завантажує приватний ключ із файлу."""
        with open(path, 'rb') as f_key:
            self.private_key = serialization.load_pem_private_key(
                f_key.read(), password=None
            )
        self.public_key = self.private_key.public_key()

    def load_public_key(self, path):
        """Завантажує публічний ключ із файлу."""
        with open(path, 'rb') as f_key:
            self.public_key = serialization.load_pem_public_key(f_key.read())

    # --- ПІДПИС ТА ПЕРЕВІРКА РЯДКІВ (ТЕКСТУ) ---

    def sign_text(self, text: str) -> str:
        """Створює підпис для тексту. Повертає підпис у шістнадцятковому (HEX) форматі."""
        if not self.private_key:
            raise ValueError("Відсутній приватний ключ для підпису!")

        data = text.encode('utf-8')
        signature_bytes = self.private_key.sign(data, hashes.SHA256())
        return signature_bytes.hex()  # Конвертуємо в HEX!

    def verify_text(self, text: str, signature_hex: str) -> bool:
        """Перевіряє підпис тексту. Очікує підпис у HEX форматі."""
        if not self.public_key:
            raise ValueError("Відсутній публічний ключ для перевірки!")

        data = text.encode('utf-8')
        try:
            signature_bytes = bytes.fromhex(signature_hex)  # Конвертуємо з HEX назад у байти
            self.public_key.verify(signature_bytes, data, hashes.SHA256())
            return True
        except (InvalidSignature, ValueError):
            return False

    # --- ПІДПИС ТА ПЕРЕВІРКА ФАЙЛІВ ---

    def sign_file(self, file_path, signature_path):
        """Створює підпис для файлу і зберігає його в інший файл у форматі HEX."""
        if not self.private_key:
            raise ValueError("Відсутній приватний ключ для підпису!")

        with open(file_path, 'rb') as f_in:
            file_data = f_in.read()

        signature_bytes = self.private_key.sign(file_data, hashes.SHA256())
        signature_hex = signature_bytes.hex()

        # Записуємо у файл як звичайний текст ('w'), бо це HEX-рядок
        with open(signature_path, 'w') as f_out:
            f_out.write(signature_hex)

        return signature_hex  # Повертаємо, щоб показати на екрані UI

    def verify_signature(self, file_path, signature_path):
        """Перевіряє автентичність файлу за його HEX-підписом із файлу."""
        if not self.public_key:
            raise ValueError("Відсутній публічний ключ для перевірки!")

        with open(file_path, 'rb') as f_file:
            file_data = f_file.read()

        with open(signature_path, 'r') as f_sig:  # Читаємо як текст ('r')
            signature_hex = f_sig.read().strip()

        try:
            signature_bytes = bytes.fromhex(signature_hex)
            self.public_key.verify(signature_bytes, file_data, hashes.SHA256())
            return True
        except (InvalidSignature, ValueError):
            return False