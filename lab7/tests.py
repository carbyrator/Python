import unittest
from unittest.mock import patch
import requests
from .currencies import get_currencies  # импортируйте вашу функцию

class TestGetCurrencies(unittest.TestCase):

    @patch('requests.get')
    def test_get_currencies_success(self, mock_get):
        """
        Проверка корректного возврата реальных данных
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Valute": {
                "USD": {"Value": 73.5},
                "EUR": {"Value": 89.2}
            }
        }

        result = get_currencies(['USD', 'EUR'])
        # Проверяем правильность получения данных
        self.assertEqual(result['USD'], 73.5)
        self.assertEqual(result['EUR'], 89.2)

    @patch('requests.get')
    def test_get_currencies_connection_error(self, mock_get):
        """
        Проверка поведения при ошибке соединения
        """
        mock_get.side_effect = ConnectionError("Сайт не доступен")

        with self.assertRaises(ConnectionError):
            get_currencies(['USD', 'EUR'])

    @patch('requests.get')
    def test_get_currencies_value_error(self, mock_get):
        """
        Проверка поведения при ошибке JSON
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Пришел не JSON")

        with self.assertRaises(ValueError):
            get_currencies(['USD', 'EUR'])

    @patch('requests.get')
    def test_get_currencies_key_error(self, mock_get):
        """
        Проверка поведения при отсутствии ключа 'Valute'
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        with self.assertRaises(KeyError):
            get_currencies(['USD', 'EUR'])

    @patch('requests.get')
    def test_get_currencies_key_error_for_nonexistent_currency(self, mock_get):
        """
        Проверка поведения при отсутствии валюты в ответе
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Valute": {
                "USD": {"Value": 73.5}
            }
        }

        with self.assertRaises(KeyError):
            get_currencies(['USD', 'EUR'])

    @patch('requests.get')
    def test_get_currencies_type_error(self, mock_get):
        """
        Проверка типа данных для валюты
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Valute": {
                "USD": {"Value": "seventy-three"}
            }
        }

        with self.assertRaises(TypeError):
            get_currencies(['USD'])

if __name__ == '__main__':
    unittest.main()
