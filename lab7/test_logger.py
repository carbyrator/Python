import unittest
import io
from .decorator import logger  # Убедитесь, что декоратор импортируется корректно
from .currencies import get_currencies


class TestLoggerDecorator(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

    def test_logging_success(self):
        # Применяем декоратор внутри метода
        @logger(handle=self.stream)
        def test_function(x):
            return x * 2

        # Логи при успешном выполнении
        test_function(5)  # Вызов метода с декоратором
        logs = self.stream.getvalue()
        self.assertIn("INFO: Начало test_function", logs)
        self.assertIn("INFO: Успех test_function", logs)
        self.assertIn("Returned value: 10", logs)

    def test_logging_error(self):
        # Логи при ошибке
        with self.assertRaises(ValueError):
            @logger(handle=self.stream)
            def faulty_function(x):
                raise ValueError("Some error")

            faulty_function(5)

        logs = self.stream.getvalue()
        # Используем assertRegex для проверки, что ошибка была записана в логи
        self.assertRegex(logs, "ERROR")
        self.assertRegex(logs, "ValueError")
if __name__ == '__main__':
    unittest.main()
