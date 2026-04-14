import unittest
import sys
import os

# Щоб тести бачили папку labs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from labs import lab1


class TestLab1(unittest.TestCase):

    def test_gcd(self):
        self.assertEqual(lab1.get_gcd(48, 18), 6)
        self.assertEqual(lab1.get_gcd(18, 48), 6)
        self.assertEqual(lab1.get_gcd(101, 10), 1)

    def test_lemer_generator(self):
        seq = lab1.generate_lemer(1, seed=5)
        self.assertEqual(seq[0], 3878)

    def test_generator_bounds(self):
        seq = lab1.generate_lemer(100)
        for num in seq:
            self.assertTrue(0 <= num < lab1.M)

    def test_cesaro(self):
        # Тест: числа, що мають спільний дільник (не взаємно прості)
        self.assertEqual(lab1.cesaro_test([2, 4, 6, 8]), 0)
        # Тест: масив замалий для пар
        self.assertEqual(lab1.cesaro_test([1]), 0)
        # Тест: взаємно прості числа
        res = lab1.cesaro_test([2, 3, 4, 5])
        self.assertGreater(res, 0)

    def test_find_period(self):
        orig_m, orig_a, orig_c = lab1.M, lab1.A, lab1.C
        lab1.M, lab1.A, lab1.C = 10, 3, 1

        period = lab1.find_period()
        self.assertTrue(period, 0)


        lab1.M, lab1.A, lab1.C = orig_m, orig_a, orig_c


if __name__ == '__main__':
    unittest.main()