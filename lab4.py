import os
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size=2048):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def save_keys(self, private_path, public_path, password=None):
        if not self.private_key or not self.public_key:
            raise ValueError("Ключі ще не згенеровані!")

        enc_alg = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()

        with open(private_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=enc_alg
            ))

        with open(public_path, 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, path, password=None):
        with open(path, 'rb') as f:
            pemlines = f.read()
        pwd_bytes = password.encode() if password else None

        self.private_key = serialization.load_pem_private_key(
            pemlines,
            password=pwd_bytes,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def load_public_key(self, path):
        with open(path, 'rb') as f:
            pemlines = f.read()
        self.public_key = serialization.load_pem_public_key(
            pemlines,
            backend=default_backend()
        )

    def encrypt_file(self, input_path, output_path):
        if not self.public_key:
            raise ValueError("Публічний ключ не завантажено!")

        chunk_size = 190

        with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break

                encrypted_chunk = self.public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(encrypted_chunk)

    def decrypt_file(self, input_path, output_path):
        if not self.private_key:
            raise ValueError("Приватний ключ не завантажено!")
        chunk_size = 256

        with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break

                decrypted_chunk = self.private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(decrypted_chunk)

if __name__ == "__main__":
    try:
        from lab3 import rc5_cbc_pad_encrypt

        has_lab3 = True
    except ImportError:
        has_lab3 = False

    print("\n=== ПОРІВНЯННЯ ШВИДКОСТІ: RSA vs RC5 ===")

    # 1. Створюємо тестовий файл (50 КБ)
    file_size_kb = 50
    test_file = "speed_test.bin"
    enc_rsa_file = "speed_rsa_enc.bin"
    enc_rc5_file = "speed_rc5_enc.bin"

    with open(test_file, "wb") as f:
        f.write(os.urandom(file_size_kb * 1024))

    print(f"Згенеровано файл: {file_size_kb} KB")

    # 2. Тест RSA
    rsa_cipher = RSACipher()
    rsa_cipher.generate_keys(2048)  # <--- ВАЖЛИВО: ТУТ МАЄ БУТИ 2048!

    start_time = time.perf_counter()
    rsa_cipher.encrypt_file(test_file, enc_rsa_file)
    rsa_time = time.perf_counter() - start_time
    print(f"[*] Час шифрування RSA: {rsa_time:.4f} сек")

    # 3. Тест RC5
    if has_lab3:
        with open(test_file, "rb") as f:
            raw_data = f.read()

        key_bytes = os.urandom(16)
        iv_bytes = os.urandom(16)

        start_time = time.perf_counter()

        encrypted_rc5_data = rc5_cbc_pad_encrypt(raw_data, key_bytes, iv_bytes)

        with open(enc_rc5_file, "wb") as f:
            f.write(encrypted_rc5_data)

        rc5_time = time.perf_counter() - start_time
        print(f"[*] Час шифрування RC5: {rc5_time:.4f} сек")

    for f in [test_file, enc_rsa_file, enc_rc5_file]:
        if os.path.exists(f):
            os.remove(f)