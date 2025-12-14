import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_path() -> tuple[str | None, str | None]:
    candidates = [
        THIS_DIR,
        os.path.join(THIS_DIR, ".."),
        os.path.join(THIS_DIR, "tmp", "project"),
    ]
    for candidate in candidates:
        lab_path = os.path.join(candidate, "lab9")
        if os.path.isdir(lab_path):
            return candidate, lab_path
    return None, None


project_dir, lab8_12_dir = find_project_path()
if project_dir:
    sys.path.insert(0, project_dir)
    sys.path.insert(0, lab8_12_dir)
else:
    raise ImportError("Cannot find lab9 project")


class TestCurrencyModel(unittest.TestCase):
    def test_currency_validation(self) -> None:
        from lab9.models.currency import Currency

        currency = Currency("840", "usd", "Доллар США", 90.5, 1)
        self.assertEqual(currency.char_code, "USD")
        self.assertAlmostEqual(currency.get_value_per_unit(), 90.5)

        with self.assertRaises(ValueError):
            Currency("840", "US", "Доллар США", 90.5, 1)
        with self.assertRaises(ValueError):
            Currency("840", "EUR", "Евро", -1, 1)


class TestDatabaseController(unittest.TestCase):
    def setUp(self) -> None:
        from lab9.controllers.databasecontroller import CurrencyRatesCRUD
        from lab9.models.currency import Currency

        self.Currency = Currency
        self.db = CurrencyRatesCRUD()

    def tearDown(self) -> None:
        self.db.close()

    def test_currency_crud(self) -> None:
        usd = self.Currency("840", "USD", "Доллар", 90.0, 1)
        currency_id = self.db._create(usd)
        rows = self.db._read()
        self.assertEqual(rows[0]["id"], currency_id)

        self.db._update({"USD": 91.1})
        updated = self.db._read("USD")[0]
        self.assertAlmostEqual(updated["value"], 91.1)

        deleted = self.db._delete(currency_id)
        self.assertEqual(deleted, 1)
        self.assertEqual(self.db._read(), [])

    def test_subscriptions(self) -> None:
        self.db.seed_users(["Test"])
        cur_id = self.db._create(self.Currency("840", "USD", "Доллар", 90.0, 1))
        self.db.seed_subscriptions([{"user_id": 1, "currency_id": cur_id}])
        subscribed = self.db.list_user_currencies(1)
        self.assertEqual(len(subscribed), 1)
        action = self.db.toggle_subscription(1, cur_id)
        self.assertEqual(action, "unsubscribed")


class TestCurrencyController(unittest.TestCase):
    def test_list_currencies_with_mock(self) -> None:
        from lab9.controllers.currencycontroller import CurrencyController

        mock_db = MagicMock()
        mock_db._read.return_value = [{"id": 1, "char_code": "USD", "value": 90}]
        controller = CurrencyController(mock_db)
        result = controller.list_currencies()
        self.assertEqual(result[0]["char_code"], "USD")
        mock_db._read.assert_called_once()


class TestGetCurrencies(unittest.TestCase):
    def test_parse_xml_success(self) -> None:
        from lab9.utils.currencies_api import get_currencies

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
        mock_response.read.return_value = xml.encode("utf-8")
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_response)
        mock_context.__exit__ = Mock(return_value=None)

        with patch("lab9.utils.currencies_api.urlopen", return_value=mock_context):
            data = get_currencies()

        self.assertIn("USD", data)
        self.assertEqual(data["USD"]["value"], 90.5)


class TestTemplates(unittest.TestCase):
    def setUp(self) -> None:
        from jinja2 import Environment, FileSystemLoader

        templates_path = os.path.join(lab8_12_dir, "templates")
        self.env = Environment(loader=FileSystemLoader(templates_path), autoescape=True)

    def test_index_template(self) -> None:
        template = self.env.get_template("index.html")
        user = {"id": 1, "name": "Тестовый"}
        currency = {"char_code": "TST", "name": "Тестовая", "value": 10.0, "nominal": 2}
        html = template.render(
            app_name="Тест",
            app_version="0.1",
            author_name="Автор",
            author_group="P0000",
            page_title="Тестовая",
            last_update="2025-12-06 12:00:00",
            users_with_subscriptions=[{"user": user, "currencies": [currency]}],
            total_currencies=1,
            total_users=1,
            total_subscriptions=1,
        )
        self.assertIn("Тестовый", html)
        self.assertIn("TST", html)

    def test_users_template(self) -> None:
        template = self.env.get_template("users.html")
        user = {"id": 1, "name": "Иван"}
        html = template.render(
            app_name="Тест",
            app_version="0.1",
            author_name="Автор",
            author_group="P0000",
            page_title="Тестовая",
            last_update="2025-12-06 12:00:00",
            users_with_subscriptions=[{"user": user, "currencies": []}],
        )
        self.assertIn("Иван", html)


if __name__ == "__main__":
    unittest.main()
