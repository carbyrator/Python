"""Контроллер с бизнес-логикой пользователей и подписок."""

from typing import Dict, List, Optional

from .databasecontroller import CurrencyRatesCRUD


class UserController:
    """Работает с пользователями и их подписками на валюты."""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        """Принимает контроллер базы данных."""
        self.db = db_controller

    def list_users(self) -> List[Dict]:
        """Возвращает всех пользователей."""
        return self.db.list_users()

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Возвращает словарь пользователя или None."""
        return self.db.get_user(user_id)

    def get_users_with_subscriptions(self) -> List[Dict]:
        """Возвращает пользователей со списком их валют."""
        result = []
        for user in self.list_users():
            result.append(
                {
                    "user": user,
                    "currencies": self.db.list_user_currencies(user["id"]),
                }
            )
        return result

    def get_profile(self, user_id: int) -> Optional[Dict]:
        """Возвращает профиль пользователя: подписки и доступные валюты."""
        user = self.get_user(user_id)
        if not user:
            return None
        return {
            "user": user,
            "subscribed": self.db.list_user_currencies(user_id),
            "available": self.db.list_available_currencies(user_id),
        }

    def subscriptions_map(self) -> Dict[int, List[int]]:
        """Возвращает словарь подписок {user_id: [currency_id]}."""
        return self.db.subscriptions_map()

    def toggle_subscription(self, user_id: int, currency_id: int) -> str:
        """Подписывает или отписывает пользователя на валюту."""
        return self.db.toggle_subscription(user_id, currency_id)
