"""Бизнес-логика, связанная с валютами."""

from typing import Dict, List

from .databasecontroller import CurrencyRatesCRUD
from models.currency import Currency


class CurrencyController:
    """Высокоуровневые операции над валютами и проксирование к БД."""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        """Принимает контроллер базы данных."""
        self.db = db_controller

    def list_currencies(self) -> List[Dict]:
        """Возвращает список валют из базы."""
        return self.db._read()

    def add_currency(
        self, num_code: str, char_code: str, name: str, value: float, nominal: int
    ) -> int:
        """Создаёт валюту и возвращает её id."""
        currency = Currency(num_code, char_code, name, value, nominal)
        return self.db._create(currency)

    def update_currency(self, char_code: str, value: float) -> None:
        """Обновляет один курс по символьному коду."""
        self.db._update({char_code: value})

    def update_many(self, updates: Dict[str, float]) -> None:
        """Групповое обновление курсов."""
        self.db._update(updates)

    def delete_currency(self, currency_id: int) -> int:
        """Удаляет валюту по id и возвращает количество удалённых строк."""
        return self.db._delete(currency_id)

    def show_console(self) -> List[Dict]:
        """Выводит курсы в консоль (для отладки) и возвращает данные."""
        currencies = self.db._read()
        for row in currencies:
            print(f"{row['char_code']}: {row['value']} ({row['nominal']})")
        return currencies
