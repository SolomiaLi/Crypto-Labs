import unittest
import os
import sys
from unittest import result

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from labs.lab4 import RSACipher


class TestRSACipher(unittest.TestCase):
    def setUp(self):
        self.cipher = RSACipher()
        self.test_file = "test_input.txt"
        self.enc_file = "test_encrypted.enc"
        self.dec_file = "test_decrypted.txt"
        self.priv_key_file = "test_private.pem"
        self.pub_key_file = "test_public.pem"
        self.original_data = b"A" * 500 + b"B" * 50 + b"C" * 10
        with open(self.test_file, "wb") as f:
            f.write(self.original_data)

    def tearDown(self):
        files_to_remove = [
            self.test_file, self.enc_file, self.dec_file,
            self.priv_key_file, self.pub_key_file
        ]
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_key_generation(self):
        self.cipher.generate_keys(1024)  # 1024 для швидкості тестів
        self.assertIsNotNone(self.cipher.private_key)
        self.assertIsNotNone(self.cipher.public_key)

    def test_key_save_and_load(self):
        self.cipher.generate_keys(1024)
        self.cipher.save_keys(self.priv_key_file, self.pub_key_file)

        new_cipher = RSACipher()
        new_cipher.load_private_key(self.priv_key_file)
        new_cipher.load_public_key(self.pub_key_file)

        self.assertIsNotNone(new_cipher.private_key)
        self.assertIsNotNone(new_cipher.public_key)

    def test_save_load_with_password(self):
        self.cipher.generate_keys(1024)
        password = "supersecretpassword"
        self.cipher.save_keys(self.priv_key_file, self.pub_key_file, password=password)

        new_cipher = RSACipher()
        new_cipher.load_private_key(self.priv_key_file, password=password)
        self.assertIsNotNone(new_cipher.private_key)

    def test_exceptions_when_no_keys(self):
        empty_cipher = RSACipher()
        with self.assertRaises(ValueError):
            empty_cipher.save_keys(self.priv_key_file, self.pub_key_file)
        with self.assertRaises(ValueError):
            empty_cipher.encrypt_file(self.test_file, self.enc_file)
        with self.assertRaises(ValueError):
            empty_cipher.decrypt_file(self.enc_file, self.dec_file)

    def test_encryption_and_decryption(self):
        self.cipher.generate_keys(2048)
        self.cipher.encrypt_file(self.test_file, self.enc_file)
        self.cipher.decrypt_file(self.enc_file, self.dec_file)

        with open(self.dec_file, "rb") as f:
            decrypted_data = f.read()

        self.assertEqual(self.original_data, decrypted_data)

    def test_main_execution(self):
        import runpy
        import sys
        import os
        labs_dir = os.path.abspath("labs")
        original_path = sys.path.copy()

        try:
            if labs_dir not in sys.path:
                sys.path.insert(0, labs_dir)
            runpy.run_path("labs/lab4.py", run_name="__main__")
            self.assertIsNone(result)
        finally:
            sys.path = original_path

if __name__ == '__main__':
    unittest.main()