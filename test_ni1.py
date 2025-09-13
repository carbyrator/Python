from Python import ni1
import unittest
class TestMySolution(unittest.TestCase):
    def test_1(self):
        self.assertEqual(ni1.f([3, 3, 3, 3], 6), [0, 1])

    def test_2(self):
        self.assertEqual(ni1.f([-3, -3, -3, -3], 6),'Введите только целые положительные числа')

    def test_3(self):
        self.assertEqual(ni1.f([3.14, 3.14, 3.14, 3.14], 6.28), 'Введите только целые положительные числа')

    def test_4(self):
        self.assertEqual(ni1.f([3.14, -3, 3.14, -3], 0.14), 'Введите только целые положительные числа')

    def test_5(self):
        self.assertEqual(ni1.f([3], 6), 'Введите минимум два целых положительных числа')

    def test_6(self):
        self.assertEqual(ni1.f([3, 'a', 'a', 3], 6), 'Введите только целые положительные числа')

    def test_7(self):
        self.assertEqual(ni1.f([], 6), 'Введите минимум два целых положительных числа')

    def test_8(self):
        self.assertEqual(ni1.f([3, 3, 3, 3], -6), 'Значение целевой суммы должно быть больше нуля')

    def test_9(self):
        self.assertEqual(ni1.f([1, 2, 3, 4], 78), 'Нет подходящей пары для достижения целевой суммы')

    def test_10(self):
        self.assertEqual(ni1.f([True, False], 1), 'Введите только целые положительные числа')

    def test_11(self):
        self.assertEqual(ni1.f([0, 3], 3), 'Введите только целые положительные числа')

    def test_12(self):
        self.assertEqual(ni1.f([3, 'a', -3, True], 6), 'Введите только целые положительные числа')

    def test_13(self):
        self.assertEqual(ni1.f([1, 2, 3, 4], 4), [0, 2])

    def test_14(self):
        self.assertEqual(ni1.f([3, 3, 3, 3], 0), 'Значение целевой суммы должно быть больше нуля')

    def test_15(self):
        self.assertEqual(ni1.f([3, 3, 3, 3], 1), 'Нет подходящей пары для достижения целевой суммы')

    def test_16(self):
        self.assertEqual(ni1.f([1000000, 20000000, 3000000], 4000000), [0, 2])

    def test_17(self):
        self.assertEqual(ni1.f([3, 6, 7, 4, 2, 1, 1, 9], 4), [0, 5])

    def test_18(self):
        self.assertEqual(ni1.f([3, 3, 3, 3], '18'), 'Нет подходящей пары для достижения целевой суммы')

if __name__ == '__main__':
    unittest.main()
