import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from labs.lab5 import DigitalSignature


class TestDigitalSignature(unittest.TestCase):
    def setUp(self):
        self.ds = DigitalSignature()
        self.test_file = "file_to_sign.bin"
        self.sig_file = "file.sig"
        self.priv_key = "ds_private.pem"
        self.pub_key = "ds_public.pem"


        with open(self.test_file, "wb") as f:
            f.write(b"Secret data for digital signature test")

    def tearDown(self):

        for f in [self.test_file, self.sig_file, self.priv_key, self.pub_key]:
            if os.path.exists(f):
                os.remove(f)

    def test_full_cycle(self):
        """Перевірка повного циклу: генерація -> підпис -> успішна верифікація"""
        self.ds.generate_keys()
        self.ds.sign_file(self.test_file, self.sig_file)

        is_valid = self.ds.verify_signature(self.test_file, self.sig_file)
        self.assertTrue(is_valid, "Підпис має бути дійсним для оригінального файлу")

    def test_tampered_file(self):
        """Перевірка підробки: якщо файл змінено, підпис має бути недійсним"""
        self.ds.generate_keys()
        self.ds.sign_file(self.test_file, self.sig_file)

        with open(self.test_file, "wb") as f:
            f.write(b"Modified data")

        is_valid = self.ds.verify_signature(self.test_file, self.sig_file)
        self.assertFalse(is_valid, "Підпис має бути недійсним після зміни файлу")

    def test_save_load_keys(self):
        """Перевірка збереження та завантаження ключів"""
        self.ds.generate_keys()
        self.ds.save_keys(self.priv_key, self.pub_key)

        new_ds = DigitalSignature()
        new_ds.load_private_key(self.priv_key)
        new_ds.sign_file(self.test_file, self.sig_file)

        new_ds.load_public_key(self.pub_key)
        self.assertTrue(new_ds.verify_signature(self.test_file, self.sig_file))

    def test_errors(self):
        """Перевірка виняткових ситуацій"""
        with self.assertRaises(ValueError):
            self.ds.sign_file(self.test_file, self.sig_file)


if __name__ == "__main__":
    unittest.main()