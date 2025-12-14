import os
import sys
import unittest
from unittest.mock import Mock, patch
from typing import List, Dict

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# Поиск проекта lab8_12
def find_project_path() -> (str, str):
    """
    Ищет путь к проекту lab8_12.

    Проходит по кандидатам и пытается найти каталог с проектом lab8_12.

    Возвращает:
        tuple: Путь к проекту и путь к lab8_12 (если найдено), иначе (None, None).
    """
    candidates = [
        THIS_DIR,
        os.path.join(THIS_DIR, '..'),
        os.path.join(THIS_DIR, 'tmp', 'project'),
    ]
    for candidate in candidates:
        lab_path = os.path.join(candidate, 'lab8_12')
        if os.path.isdir(lab_path):
            return candidate, lab_path
    return None, None


project_dir, lab8_12_dir = find_project_path()
if project_dir:
    sys.path.insert(0, project_dir)
    sys.path.insert(0, lab8_12_dir)
else:
    raise ImportError("Cannot find lab8_12 project")


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

class TestUserModel(unittest.TestCase):
    """ Тестирование модели пользователя. """

    def test_user_creation(self) -> None:
        """ Тестирование создания пользователя. """
        from lab8_12.models.user import User
        user = User(1, "Иван")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Иван")


class TestAuthorModel(unittest.TestCase):
    """Тестирование модели автора. """

    def test_author_creation(self) -> None:
        """ Тестирование создания автора. """
        from lab8_12.models.author import Author
        author = Author("Иван", "P3120")
        self.assertEqual(author.name, "Иван")
        self.assertEqual(author.group, "P3120")


class TestAppModel(unittest.TestCase):
    """ Тестирование модели приложения. """

    def test_app_creation(self) -> None:
        """ Тестирование создания приложения. """
        from lab8_12.models.author import Author
        from lab8_12.models.app import App
        author = Author("Иван", "P3120")
        app = App("Приложение", "1.0", author)
        self.assertEqual(app.name, "Приложение")
        self.assertEqual(app.version, "1.0")
        self.assertIs(app.author, author)


class TestCurrencyModel(unittest.TestCase):
    """ Тестирование модели валюты. """

    def test_currency_creation(self) -> None:
        """ Тестирование создания валюты. """
        from lab8_12.models.currency import Currency
        currency = Currency("R01235", "840", "USD", "Доллар США", 90.5, 1)
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")


class TestUserCurrencyModel(unittest.TestCase):
    """ Тестирование модели связи пользователя и валюты. """

    def test_user_currency_creation(self) -> None:
        """ Тестирование создания связи между пользователем и валютой. """
        from lab8_12.models.user_currency import UserCurrency
        uc = UserCurrency(1, 2, "R01235")
        self.assertEqual(uc.user_id, 2)
        self.assertEqual(uc.currency_id, "R01235")


class TestGetCurrencies(unittest.TestCase):
    """ Тестирование функции получения валют. """

    def test_parse_xml_success(self) -> None:
        """ Тестирование успешного парсинга XML-ответа при получении курсов валют. """
        from lab8_12.utils.currencies_api import get_currencies

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <ValCurs Date="02.12.2025" name="Foreign Currency Market">
            <Valute ID="R01235">
                <NumCode>840</NumCode>
                <CharCode>USD</CharCode>
                <Nominal>1</Nominal>
                <Name>Доллар США</Name>
                <Value>90,5000</Value>
            </Valute>
        </ValCurs>"""

        mock_response = Mock()
        mock_response.read.return_value = xml.encode('utf-8')
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_response)
        mock_context.__exit__ = Mock(return_value=None)

        with patch('lab8_12.utils.currencies_api.urlopen', return_value=mock_context):
            data = get_currencies()

        self.assertIn("USD", data)
        self.assertEqual(data["USD"]["value"], 90.5)


class TestTemplates(unittest.TestCase):
    """ Тестирование шаблонов. """

    def setUp(self):
        """ Настройка Jinja2 и моделей перед каждым тестом. """
        templates_path = os.path.join(lab8_12_dir, 'templates')
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(templates_path), autoescape=True)

        # Импорт моделей
        from lab8_12.models.user import User
        from lab8_12.models.currency import Currency
        self.User = User
        self.Currency = Currency

    def test_index_template(self):
        """ Тестирование рендеринга главной страницы с пользователями и валютами. """
        template = self.env.get_template('index.html')

        user = self.User(1, 'Тестовый')
        cur = self.Currency('R00001', '000', 'TST', 'Тестовая валюта', 10.0, 2)

        html = template.render(
            app_name='Тест',
            app_version='0.1',
            author_name='Автор',
            author_group='P0000',
            page_title='Тестовая',
            last_update='2025-12-06 12:00:00',
            users_with_subscriptions=[{'user': user, 'currencies': [cur]}],
            total_currencies=1,
            total_users=1,
            total_subscriptions=1
        )

        self.assertIn('Тестовый', html)
        self.assertIn('TST', html)

    def test_users_template(self):
        """ Тестирование рендеринга страницы с пользователями. """
        template = self.env.get_template('users.html')

        user = self.User(1, 'Иван')

        html = template.render(
            app_name='Тест',
            app_version='0.1',
            author_name='Автор',
            author_group='P0000',
            page_title='Тестовая',
            last_update='2025-12-06 12:00:00',
            users_with_subscriptions=[{'user': user, 'currencies': []}]
        )

        self.assertIn('Иван', html)


if __name__ == '__main__':
    unittest.main()
