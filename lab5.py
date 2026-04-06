import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class DigitalSignature:
    """Клас для створення та перевірки цифрового підпису файлів."""

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size=2048):
        """Генерує пару ключів RSA для підпису."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
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
                f_key.read(), password=None, backend=default_backend()
            )
        self.public_key = self.private_key.public_key()

    def load_public_key(self, path):
        """Завантажує публічний ключ із файлу."""
        with open(path, 'rb') as f_key:
            self.public_key = serialization.load_pem_public_key(
                f_key.read(), backend=default_backend()
            )

    def sign_file(self, file_path, signature_path):
        """Створює цифровий підпис для файлу за допомогою алгоритму PSS."""
        if not self.private_key:
            raise ValueError("Відсутній приватний ключ для підпису!")

        with open(file_path, 'rb') as f_in:
            file_data = f_in.read()

        signature = self.private_key.sign(
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        with open(signature_path, 'wb') as f_out:
            f_out.write(signature)

    def verify_signature(self, file_path, signature_path):
        """Перевіряє автентичність файлу за його підписом."""
        if not self.public_key:
            raise ValueError("Відсутній публічний ключ для перевірки!")

        with open(file_path, 'rb') as f_file, open(signature_path, 'rb') as f_sig:
            file_data = f_file.read()
            signature = f_sig.read()

        try:
            self.public_key.verify(
                signature,
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except (InvalidSignature, ValueError):
            return False