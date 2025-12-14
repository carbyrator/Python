#!/usr/bin/env python3
"""Простой MVC-сервер для мониторинга валют с актуальными курсами ЦБ РФ."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from controllers import (
    CurrencyController,
    CurrencyRatesCRUD,
    PageController,
    UserController,
)
from models import App, Author
from utils.currencies_api import get_currencies, get_test_currencies

# ------------------------- Инициализация MVC -------------------------
env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
author = Author("Шанин Иван", "P3120")
app = App("Мониторинг валют", "1.1.0", author)
last_update_time = datetime.now()
AUTO_REFRESH_SECONDS = 60 * 60  # автообновление раз в час


def last_update_as_str() -> str:
    """Возвращает время последнего обновления курсов в текстовом виде."""
    return last_update_time.strftime("%Y-%m-%d %H:%M:%S")


db_controller = CurrencyRatesCRUD()
currency_controller = CurrencyController(db_controller)
user_controller = UserController(db_controller)
page_controller = PageController(env, app, author, last_update_as_str)


def seed_database() -> None:
    """Заполняет in-memory БД пользователями, валютами и подписками."""
    currency_data = fetch_rates()
    db_controller.seed_currencies(list(currency_data.values()))
    db_controller.seed_users(
        ["Чингиз Халилов", "Милана Карелина", "Слава Федоров", "Олег Брискиндик"]
    )

    # Связываем пользователей с валютами по char_code.
    currency_rows = {row["char_code"]: row for row in db_controller._read()}
    subscriptions = []
    if "USD" in currency_rows:
        subscriptions.append({"user_id": 1, "currency_id": currency_rows["USD"]["id"]})
        subscriptions.append({"user_id": 2, "currency_id": currency_rows["USD"]["id"]})
    if "EUR" in currency_rows:
        subscriptions.append({"user_id": 1, "currency_id": currency_rows["EUR"]["id"]})
    for char_code in ("GBP", "CNY"):
        if char_code in currency_rows:
            subscriptions.append(
                {
                    "user_id": 3 if char_code == "GBP" else 4,
                    "currency_id": currency_rows[char_code]["id"],
                }
            )
    db_controller.seed_subscriptions(subscriptions)
    bump_last_update()


def bump_last_update() -> None:
    """Фиксирует текущее время обновления курсов."""
    global last_update_time
    last_update_time = datetime.now()


def fetch_rates() -> dict:
    """Возвращает словарь курсов из API или тестовый набор при ошибке сети."""
    def _normalize(raw_data: dict) -> dict:
        normalized = {}
        for code, payload in raw_data.items():
            nominal = payload.get("nominal", 1) or 1
            rate_per_unit = float(payload["value"]) / nominal
            code_upper = code.upper()
            normalized[code_upper] = {
                "num_code": payload["num_code"],
                "char_code": code_upper,
                "name": payload["name"],
                "value": rate_per_unit,
                "nominal": nominal,
            }
        return normalized

    try:
        raw = get_currencies()
    except Exception:
        raw = get_test_currencies()

    return _normalize(raw)


def refresh_from_api() -> int:
    """
    Подтягивает актуальные курсы, обновляет существующие записи и добавляет новые.

    Returns:
        Количество обновлённых или добавленных валют.
    """
    currency_data = fetch_rates()
    existing = {row["char_code"]: row for row in db_controller._read()}
    updates: dict[str, float] = {}
    created = 0

    for code, payload in currency_data.items():
        code_upper = code.upper()
        if code_upper in existing:
            updates[code_upper] = payload["value"]
        else:
            currency_controller.add_currency(
                payload["num_code"],
                code_upper,
                payload["name"],
                payload["value"],
                payload["nominal"],
            )
            created += 1

    if updates:
        currency_controller.update_many(updates)

    bump_last_update()
    return len(updates) + created


def ensure_fresh_rates() -> None:
    """Автообновление, если последний апдейт старше установленного интервала."""
    elapsed = (datetime.now() - last_update_time).total_seconds()
    if elapsed >= AUTO_REFRESH_SECONDS:
        refresh_from_api()


seed_database()


# ------------------------- HTTP обработчик -------------------------
class CurrencyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов для страниц и JSON-API."""

    def do_GET(self) -> None:
        """Маршрутизирует GET-запросы по путям."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        ensure_fresh_rates()

        if path == "/":
            self.show_index()
        elif path == "/users":
            self.show_users()
        elif path == "/user":
            self.show_user(query_params)
        elif path == "/currencies":
            self.show_currencies()
        elif path == "/author":
            self.show_author()
        elif path == "/currency/delete":
            self.delete_currency(query_params)
        elif path == "/currency/create":
            self.create_currency(query_params)
        elif path == "/currency/update":
            self.update_currency(query_params)
        elif path == "/toggle_subscription":
            self.toggle_subscription(query_params)
        elif path == "/refresh_currencies":
            self.refresh_currencies()
        else:
            self.send_error(404, "Страница не найдена")

    # ------------------------- View helpers -------------------------
    def _send_html(self, html: str, status: int = 200) -> None:
        """Возвращает HTML-ответ с нужным статусом."""
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_json(self, data: dict, status: int = 200) -> None:
        """Возвращает JSON-ответ (используется для Ajax-запросов)."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    # ------------------------- Route handlers -------------------------
    def show_index(self) -> None:
        """Главная страница со сводной информацией."""
        users_with_subscriptions = user_controller.get_users_with_subscriptions()
        currencies = currency_controller.list_currencies()
        context = {
            "users_with_subscriptions": users_with_subscriptions,
            "total_currencies": len(currencies),
            "total_users": len(user_controller.list_users()),
            "total_subscriptions": db_controller.count_subscriptions(),
        }
        html = page_controller.render("index.html", context)
        self._send_html(html)

    def show_users(self) -> None:
        context = {"users_with_subscriptions": user_controller.get_users_with_subscriptions()}
        html = page_controller.render("users.html", context)
        self._send_html(html)

    def show_user(self, query_params: dict) -> None:
        """Показывает профиль выбранного пользователя."""
        try:
            user_id = int(query_params.get("id", ["0"])[0])
        except ValueError:
            self.send_error(400, "Неверный ID пользователя")
            return

        profile = user_controller.get_profile(user_id)
        if not profile:
            self.send_error(404, "Пользователь не найден")
            return

        context = {
            "user": profile["user"],
            "subscribed_currencies": profile["subscribed"],
            "available_currencies": profile["available"],
        }
        html = page_controller.render("user.html", context)
        self._send_html(html)

    def show_currencies(self) -> None:
        context = {
            "currencies": currency_controller.list_currencies(),
            "users": user_controller.list_users(),
            "user_subscriptions": user_controller.subscriptions_map(),
        }
        html = page_controller.render("currencies.html", context)
        self._send_html(html)

    def show_author(self) -> None:
        """Отображает страницу с информацией об авторе."""
        html = page_controller.render("base.html", {"page_title": "Об авторе"})
        self._send_html(html)

    def delete_currency(self, query_params: dict) -> None:
        """Удаляет валюту по id из таблицы currency."""
        try:
            currency_id = int(query_params.get("id", ["0"])[0])
        except ValueError:
            self.send_error(400, "Некорректный id валюты")
            return

        deleted = currency_controller.delete_currency(currency_id)
        status = 200 if deleted else 404
        message = "Валюта удалена" if deleted else "Валюта не найдена"
        html = page_controller.render("base.html", {"page_title": message})
        self._send_html(html, status=status)

    def create_currency(self, query_params: dict) -> None:
        """Создаёт новую валюту на основе GET-параметров."""
        required_fields = ["num_code", "char_code", "name", "value", "nominal"]
        missing = [field for field in required_fields if field not in query_params]
        if missing:
            self.send_error(400, f"Не указаны поля: {', '.join(missing)}")
            return

        try:
            num_code = query_params["num_code"][0]
            char_code = query_params["char_code"][0]
            name = query_params["name"][0]
            value = float(query_params["value"][0])
            nominal = int(query_params["nominal"][0])
        except (ValueError, IndexError):
            self.send_error(400, "Некорректные параметры валюты")
            return

        currency_controller.add_currency(num_code, char_code, name, value, nominal)
        html = page_controller.render("base.html", {"page_title": "Валюта добавлена"})
        self._send_html(html)

    def update_currency(self, query_params: dict) -> None:
        updates = {}
        for code, values in query_params.items():
            if not values:
                continue
            try:
                updates[code.upper()] = float(values[0])
            except ValueError:
                continue

        if not updates:
            self.send_error(400, "Нет данных для обновления")
            return

        currency_controller.update_many(updates)
        bump_last_update()
        html = page_controller.render(
            "base.html",
            {
                "page_title": "Курсы обновлены",
                "updates": updates,
            },
        )
        self._send_html(html)

    def show_currency_console(self) -> None:
        currency_controller.show_console()
        html = page_controller.render("base.html", {"page_title": "Данные отправлены в консоль"})
        self._send_html(html)

    def toggle_subscription(self, query_params: dict) -> None:
        """Подписывает или отписывает пользователя на валюту через Ajax."""
        try:
            user_id = int(query_params.get("user_id", ["0"])[0])
            currency_id = int(query_params.get("currency_id", ["0"])[0])
        except ValueError:
            self._send_json({"success": False, "error": "Некорректные параметры"}, status=400)
            return

        action = user_controller.toggle_subscription(user_id, currency_id)
        self._send_json({"success": True, "action": action})

    def refresh_currencies(self) -> None:
        """Подтягивает актуальные курсы с API и обновляет существующие записи."""
        fresh_data = fetch_rates()
        existing_codes = {row["char_code"] for row in db_controller._read()}
        updates = {code: payload["value"] for code, payload in fresh_data.items() if code in existing_codes}

        if updates:
            currency_controller.update_many(updates)
            bump_last_update()
        self._send_json({"success": True, "updated": len(updates)})

    def log_message(self, format, *args):
        pass


def run_server() -> None:
    """Запускает HTTP сервер на 8080."""
    server_address = ("", 8081)
    httpd = HTTPServer(server_address, CurrencyHandler)
    print(f"Сервер запущен на http://localhost:8081")
    print(f"Приложение: {app.name} v{app.version}")
    print(f"Автор: {author.name}, группа: {author.group}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
