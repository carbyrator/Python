from Python import lab2
import unittest


class TestMySolution(unittest.TestCase):

    def test_guess_number_binary(self):
        """Тест бинарного поиска."""
        self.assertEqual(lab2.guess_number(78, list(range(1, 101)), '2'),
                         'Угадываемое число: 78, количество попыток: 5')

    def test_guess_number_linear(self):
        """Тест линейного поиска."""
        self.assertEqual(lab2.guess_number(78, list(range(1, 101)), '1'),
                         'Угадываемое число: 78, количество попыток: 78')

    def test_not_found_binary(self):
        """Тест ситуации, когда число не найдено (бинарный поиск)."""
        self.assertEqual(lab2.guess_number(105, list(range(1, 101)), '2'), 'Число не найдено')

    def test_not_found_linear(self):
        """Тест ситуации, когда число не найдено (линейный поиск)."""
        self.assertEqual(lab2.guess_number(105, list(range(1, 101)), '1'), 'Число не найдено')

    def test_empty_list(self):
        """Тест пустой последовательности."""
        self.assertEqual(lab2.guess_number(10, [], '2'), 'Число не найдено')

    def test_single_element_list(self):
        """Тест одностраничного списка."""
        self.assertEqual(lab2.guess_number(10, [10], '2'), 'Угадываемое число: 10, количество попыток: 1')

    def test_negative_number(self):
        """Тест отрицательного числа."""
        self.assertEqual(lab2.guess_number(-10, list(range(1, 100)), '2'), 'Число не найдено')


if __name__ == '__main__':
    unittest.main()
