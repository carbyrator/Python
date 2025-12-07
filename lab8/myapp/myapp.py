#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import time
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies

# Инициализация Jinja2
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=True
)

# Инициализация данных
author = Author("Шанин Иван", "P3120")
app = App("Мониторинг валют", "1.0.0", author)

# Тестовые данные пользователей
users = [
    User(1, "Алексей Петров"),
    User(2, "Мария Сидорова"),
    User(3, "Дмитрий Иванов"),
    User(4, "Елена Кузнецова"),
]

# Подписки пользователей (UserCurrency)
user_subscriptions = [
    UserCurrency(1, 1, "R01235"),  # Алексей -> USD
    UserCurrency(2, 1, "R01239"),  # Алексей -> EUR
    UserCurrency(3, 2, "R01235"),  # Мария -> USD
    UserCurrency(4, 3, "R01035"),  # Дмитрий -> GBP
    UserCurrency(5, 4, "R01375"),  # Елена -> CNY
]

# Получение курсов валют
currencies_data = get_currencies()
currencies = []
for char_code, data in currencies_data.items():
    currencies.append(Currency(
        id=data['id'],
        num_code=data['num_code'],
        char_code=data['char_code'],
        name=data['name'],
        value=data['value'],
        nominal=data['nominal']
    ))

last_update_time = datetime.now()


class CurrencyHandler(BaseHTTPRequestHandler):
    """
    Обработчик запросов для мониторинга валют.

    Этот класс обрабатывает HTTP-запросы на различные пути, такие как:
    - Главная страница с общей информацией.
    - Страница пользователей.
    - Страница конкретного пользователя с подписанными валютами.
    - Страница с курсами валют.
    - Страница с информацией об авторе.
    - Обработка подписки и отписки от валют.
    - Обновление курсов валют.
    """

    def do_GET(self):
        """ Обработка GET-запросов. """
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/':
            self.show_index()
        elif path == '/users':
            self.show_users()
        elif path == '/user':
            self.show_user(query_params.get('id', [''])[0])
        elif path == '/currencies':
            self.show_currencies()
        elif path == '/author':
            self.show_author()
        elif path == '/toggle_subscription':
            self.toggle_subscription(query_params)
        elif path == '/refresh_currencies':
            self.refresh_currencies()
        else:
            self.send_error(404, "Страница не найдена")

    def _render_template(self, template_name: str, context: dict = None):
        """ Рендерит HTML-шаблон с контекстом. """
        if context is None:
            context = {}

        base_context = {
            'app_name': app.name,
            'app_version': app.version,
            'author_name': author.name,
            'author_group': author.group,
            'page_title': 'Мониторинг валют',
            'last_update': last_update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        base_context.update(context)

        template = env.get_template(template_name)
        html_content = template.render(**base_context)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def _send_json(self, data: dict):
        """ Отправляет JSON-ответ на запрос. """
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def show_index(self):
        """
        Отображает главную страницу с общим списком пользователей и их подписками на валюты.
        """
        users_with_subscriptions = []

        for user in users:
            user_currencies = []
            for sub in user_subscriptions:
                if sub.user_id == user.id:
                    currency = next((c for c in currencies if c.id == sub.currency_id), None)
                    if currency:
                        user_currencies.append(currency)

            users_with_subscriptions.append({
                'user': user,
                'currencies': user_currencies
            })

        context = {
            'users_with_subscriptions': users_with_subscriptions,
            'total_currencies': len(currencies),
            'total_users': len(users),
            'total_subscriptions': len(user_subscriptions)
        }
        self._render_template('index.html', context)

    def show_users(self):
        """
        Отображает список всех пользователей с их подписками на валюты.
        """
        users_with_subscriptions = []

        for user in users:
            user_currencies = []
            for sub in user_subscriptions:
                if sub.user_id == user.id:
                    currency = next((c for c in currencies if c.id == sub.currency_id), None)
                    if currency:
                        user_currencies.append(currency)

            users_with_subscriptions.append({
                'user': user,
                'currencies': user_currencies
            })

        context = {
            'users_with_subscriptions': users_with_subscriptions
        }
        self._render_template('users.html', context)

    def show_user(self, user_id: str):
        """
        Отображает страницу конкретного пользователя с его подписками и доступными валютами.
        """
        try:
            user_id = int(user_id)
            user = next((u for u in users if u.id == user_id), None)

            if not user:
                self.send_error(404, "Пользователь не найден")
                return

            subscribed_currency_ids = [sub.currency_id for sub in user_subscriptions if sub.user_id == user_id]
            subscribed_currencies = [c for c in currencies if c.id in subscribed_currency_ids]
            available_currencies = [c for c in currencies if c.id not in subscribed_currency_ids]

            context = {
                'user': user,
                'subscribed_currencies': subscribed_currencies,
                'available_currencies': available_currencies
            }
            self._render_template('user.html', context)

        except ValueError:
            self.send_error(400, "Неверный ID пользователя")

    def show_currencies(self):
        """
        Отображает страницу с курсами всех валют.
        """
        user_subscriptions_dict = {}
        for user in users:
            user_subscriptions_dict[user.id] = [
                sub.currency_id for sub in user_subscriptions if sub.user_id == user.id
            ]

        context = {
            'currencies': currencies,
            'users': users,
            'user_subscriptions': user_subscriptions_dict
        }
        self._render_template('currencies.html', context)

    def show_author(self):
        """
        Отображает страницу с информацией об авторе.
        """
        context = {
            'page_title': 'Об авторе'
        }
        self._render_template('base.html', context)

    def toggle_subscription(self, query_params: dict):
        """ Переключает подписку пользователя на валюту. """
        try:
            user_id = int(query_params.get('user_id', [''])[0])
            currency_id = query_params.get('currency_id', [''])[0]

            user = next((u for u in users if u.id == user_id), None)
            currency = next((c for c in currencies if c.id == currency_id), None)

            if not user or not currency_id:
                self._send_json({'success': False, 'error': 'Пользователь или валюта не найдены'})
                return

            existing_sub = next(
                (sub for sub in user_subscriptions
                 if sub.user_id == user_id and sub.currency_id == currency_id),
                None
            )

            if existing_sub:
                user_subscriptions.remove(existing_sub)
                self._send_json({'success': True, 'action': 'unsubscribed'})
            else:
                new_id = max([sub.id for sub in user_subscriptions], default=0) + 1
                new_sub = UserCurrency(new_id, user_id, currency_id)
                user_subscriptions.append(new_sub)
                self._send_json({'success': True, 'action': 'subscribed'})

        except Exception as e:
            self._send_json({'success': False, 'error': str(e)})

    def refresh_currencies(self):
        """
        Обновляет курсы валют, загружая новые данные с API.
        """
        global currencies, last_update_time

        try:
            currencies_data = get_currencies()
            currencies = []
            for char_code, data in currencies_data.items():
                currencies.append(Currency(
                    id=data['id'],
                    num_code=data['num_code'],
                    char_code=data['char_code'],
                    name=data['name'],
                    value=data['value'],
                    nominal=data['nominal']
                ))

            last_update_time = datetime.now()
            self._send_json({'success': True, 'message': 'Курсы обновлены'})

        except Exception as e:
            self._send_json({'success': False, 'error': str(e)})

    def log_message(self, format, *args):
        """
        Отключает стандартное логирование.
        """
        pass


def run_server():
    """
    Запускает HTTP сервер на порту 8080 для обслуживания запросов.
    """
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, CurrencyHandler)
    print(f"Сервер запущен на http://localhost:8080")
    print(f"Приложение: {app.name} v{app.version}")
    print(f"Автор: {author.name}, группа: {author.group}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
