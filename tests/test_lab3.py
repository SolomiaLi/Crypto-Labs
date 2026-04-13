import unittest
from labs.lab3 import RC5, rc5_cbc_pad_encrypt, rc5_cbc_pad_decrypt

class TestLab3Variant6(unittest.TestCase):
    def setUp(self):
        self.key = b"12345678"
        self.iv = b"random_iv_16byte"
        self.data = b"Testing RC5 w=64 variant 6"

    def test_logic_64bit(self):
        """Перевірка, чи правильно працює 64-бітне слово"""
        cipher = RC5(w=64, r=12, key=self.key)
        block = b"A" * 16  # 128 біт блок
        enc = cipher.encrypt_block(block)
        dec = cipher.decrypt_block(enc)
        self.assertEqual(block, dec)

    def test_full_cycle(self):
        """Тест шифрування файлу (CBC + Padding)"""
        encrypted = rc5_cbc_pad_encrypt(self.data, self.key, self.iv)
        self.assertEqual(len(encrypted), 48)
        decrypted = rc5_cbc_pad_decrypt(encrypted, self.key)
        self.assertEqual(self.data, decrypted)

    def test_padding_standard(self):
        """Перевірка, що падінг додається навіть до кратного блоку"""
        exact_data = b"B" * 16
        encrypted = rc5_cbc_pad_encrypt(exact_data, self.key, self.iv)
        self.assertEqual(len(encrypted), 48)


if __name__ == '__main__':
    unittest.main()