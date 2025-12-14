"""Database controller that encapsulates SQLite CRUD operations."""

import sqlite3
from typing import Dict, Iterable, List, Optional

from models.currency import Currency


class CurrencyRatesCRUD:
    """Работа с in-memory SQLite и CRUD над сущностями пользователя и валют."""

    def __init__(self) -> None:
        """Создаёт подключение и инициализирует схему."""
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Создаёт таблицы и включает поддержку внешних ключей."""
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
            """
        )
        self.conn.commit()

    # ------------------------- Currency CRUD -------------------------
    def _create(self, currency: Currency) -> int:
        """Добавляет новую валюту и возвращает её id."""
        sql = """
        INSERT INTO currency(num_code, char_code, name, value, nominal)
        VALUES (?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(
            sql,
            (
                currency.num_code,
                currency.char_code,
                currency.name,
                currency.value,
                currency.nominal,
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def _read(self, char_code: Optional[str] = None) -> List[Dict]:
        """Возвращает список валют или одну валюту по символьному коду."""
        cur = self.conn.cursor()
        if char_code:
            cur.execute("SELECT * FROM currency WHERE char_code = ?", (char_code,))
        else:
            cur.execute("SELECT * FROM currency ORDER BY char_code")
        return [dict(row) for row in cur.fetchall()]

    def _update(self, updates: Dict[str, float]) -> None:
        """Обновляет курсы валют по словарю {char_code: value}."""
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        cur = self.conn.cursor()
        for code, value in updates.items():
            cur.execute(sql, (value, code.upper()))
        self.conn.commit()

    def _delete(self, currency_id: int) -> int:
        """Удаляет валюту по id и возвращает количество удалённых строк."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cur.rowcount

    def seed_currencies(self, raw_items: Iterable[Dict]) -> None:
        """Загружает стартовый набор валют с именованными параметрами."""
        sql = """
        INSERT INTO currency(num_code, char_code, name, value, nominal)
        VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        cur = self.conn.cursor()
        cur.executemany(sql, raw_items)
        self.conn.commit()

    # ------------------------- Users -------------------------
    def seed_users(self, names: Iterable[str]) -> None:
        """Добавляет пользователей по списку имён."""
        cur = self.conn.cursor()
        cur.executemany("INSERT INTO user(name) VALUES(?)", [(name,) for name in names])
        self.conn.commit()

    def list_users(self) -> List[Dict]:
        """Возвращает всех пользователей."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user ORDER BY id")
        return [dict(row) for row in cur.fetchall()]

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Возвращает пользователя по id или None."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    # ------------------------- Subscriptions -------------------------
    def seed_subscriptions(self, pairs: Iterable[Dict[str, int]]) -> None:
        """Заполняет таблицу подписок пользователя на валюту."""
        sql = """
        INSERT INTO user_currency(user_id, currency_id)
        VALUES(:user_id, :currency_id)
        """
        cur = self.conn.cursor()
        cur.executemany(sql, pairs)
        self.conn.commit()

    def list_user_currencies(self, user_id: int) -> List[Dict]:
        """Возвращает валюты, на которые подписан пользователь."""
        sql = """
        SELECT c.* FROM currency c
        INNER JOIN user_currency uc ON uc.currency_id = c.id
        WHERE uc.user_id = ?
        ORDER BY c.char_code
        """
        cur = self.conn.cursor()
        cur.execute(sql, (user_id,))
        return [dict(row) for row in cur.fetchall()]

    def list_available_currencies(self, user_id: int) -> List[Dict]:
        """Возвращает валюты, на которые пользователь ещё не подписан."""
        sql = """
        SELECT * FROM currency
        WHERE id NOT IN (
            SELECT currency_id FROM user_currency WHERE user_id = ?
        )
        ORDER BY char_code
        """
        cur = self.conn.cursor()
        cur.execute(sql, (user_id,))
        return [dict(row) for row in cur.fetchall()]

    def subscriptions_map(self) -> Dict[int, List[int]]:
        """Возвращает словарь подписок {user_id: [currency_id, ...]}."""
        cur = self.conn.cursor()
        cur.execute("SELECT user_id, currency_id FROM user_currency")
        mapping: Dict[int, List[int]] = {}
        for row in cur.fetchall():
            mapping.setdefault(row["user_id"], []).append(row["currency_id"])
        return mapping

    def toggle_subscription(self, user_id: int, currency_id: int) -> str:
        """Подписывает или отписывает пользователя и возвращает действие."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id FROM user_currency WHERE user_id = ? AND currency_id = ?",
            (user_id, currency_id),
        )
        existing = cur.fetchone()
        if existing:
            cur.execute("DELETE FROM user_currency WHERE id = ?", (existing["id"],))
            action = "unsubscribed"
        else:
            cur.execute(
                "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)",
                (user_id, currency_id),
            )
            action = "subscribed"
        self.conn.commit()
        return action

    def count_subscriptions(self) -> int:
        """Возвращает количество записей в user_currency."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM user_currency")
        row = cur.fetchone()
        return int(row[0]) if row else 0

    def close(self) -> None:
        """Закрывает соединение с базой."""
        self.conn.close()

    def __del__(self) -> None:
        self.close()
