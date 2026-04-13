import unittest
import os
from labs import lab2
import hashlib


class TestMD5(unittest.TestCase):

    def test_empty_string(self):
        """Перевірка хешування порожнього рядка (Edge case)"""
        expected = "d41d8cd98f00b204e9800998ecf8427e"
        actual = lab2.get_string_hash("")
        self.assertEqual(actual.lower(), expected)

    def test_standard_rfc_vectors(self):
        """Перевірка стандартних тестових векторів (з методички)"""
        test_cases = {
            "a": "0cc175b9c0f1b6a831c399e269772661",
            "abc": "900150983cd24fb0d6963f7d28e17f72",
            "message digest": "f96b697d7cb7938d525a2f31aaf161d0",
            "abcdefghijklmnopqrstuvwxyz": "c3fcd3d76192e4007dfb496cca67e13b",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "d174ab98d277d9f5a5611c2c9f419d9f"
        }

        for text, expected in test_cases.items():
            with self.subTest(text=text):
                actual = lab2.get_string_hash(text)
                self.assertEqual(actual.lower(), expected)

    def test_long_string(self):
        """Перевірка дуже довгого тексту (щоб перевірити розбиття на блоки по 512 біт)"""
        long_text = "1" * 80
        expected = "7478ba1875f17511c12740431336a09e"
        actual = lab2.get_string_hash(long_text)

        true_hash = hashlib.md5(long_text.encode()).hexdigest()
        print(f"СПРАВЖНІЙ ХЕШ: {true_hash}")

        self.assertEqual(actual.lower(), expected)

    def test_file_hashing(self):
        """Перевірка читання та хешування файлу"""
        test_filename = "temp_test_md5.txt"
        test_content = "message digest"
        expected_hash = "f96b697d7cb7938d525a2f31aaf161d0"

        with open(test_filename, "w", encoding="utf-8") as f:
            f.write(test_content)

        try:
            actual_hash = lab2.get_file_hash(test_filename)
            self.assertEqual(actual_hash.lower(), expected_hash)
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()