import os
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

DEFAULT_KEY_SIZE = 2048

class DigitalSignature:

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size: int = DEFAULT_KEY_SIZE) -> None:
        self.private_key = dsa.generate_private_key(key_size=key_size)
        self.public_key = self.private_key.public_key()

    def save_keys(self, private_path: str, public_path: str) -> None:
        if not self.private_key or not self.public_key:
            raise ValueError("Ключі ще не згенеровані!")

        with open(private_path, "wb") as f_priv:
            f_priv.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(public_path, "wb") as f_pub:
            f_pub.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    def load_private_key(self, path: str) -> None:
        with open(path, "rb") as f_key:
            self.private_key = serialization.load_pem_private_key(
                f_key.read(), password=None
            )
        self.public_key = self.private_key.public_key()

    def load_public_key(self, path: str) -> None:
        with open(path, "rb") as f_key:
            self.public_key = serialization.load_pem_public_key(f_key.read())


    def sign_text(self, text: str) -> str:
        if not self.private_key:
            raise ValueError("Відсутній приватний ключ для підпису!")

        data = text.encode("utf-8")
        signature_bytes = self.private_key.sign(data, hashes.SHA256())
        return signature_bytes.hex()

    def verify_text(self, text: str, signature_hex: str) -> bool:
        if not self.public_key:
            raise ValueError("Відсутній публічний ключ для перевірки!")

        data = text.encode("utf-8")
        try:
            signature_bytes = bytes.fromhex(signature_hex)
        except ValueError:
            return False

        try:
            self.public_key.verify(signature_bytes, data, hashes.SHA256())
            return True
        except InvalidSignature:
            return False


    def sign_file(self, file_path: str, signature_path: str) -> str:
        if not self.private_key:
            raise ValueError("Відсутній приватний ключ для підпису!")
        with open(file_path, "rb") as f_in:
            file_data = f_in.read()

        signature_bytes = self.private_key.sign(file_data, hashes.SHA256())
        signature_hex = signature_bytes.hex()

        with open(signature_path, "w", encoding="utf-8") as f_out:
            f_out.write(signature_hex)

        return signature_hex

    def verify_signature(self, file_path: str, signature_path: str) -> bool:
        if not self.public_key:
            raise ValueError("Відсутній публічний ключ для перевірки!")

        with open(file_path, "rb") as f_file:
            file_data = f_file.read()

        with open(signature_path, "r", encoding="utf-8") as f_sig:
            signature_hex = f_sig.read().strip()

        try:
            signature_bytes = bytes.fromhex(signature_hex)
        except ValueError:
            return False

        try:
            self.public_key.verify(signature_bytes, file_data, hashes.SHA256())
            return True
        except InvalidSignature:
            return False