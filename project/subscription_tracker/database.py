"""
Модуль для работы с базой данных SQLite.

Предоставляет класс :class:`Database` для выполнения CRUD-операций
над подписками пользователей.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List

from subscription_tracker.models import Subscription

DEFAULT_DB_PATH = Path("subscriptions.db")


class Database:
    """Обёртка над SQLite для хранения подписок.

    :param db_path: Путь к файлу базы данных. По умолчанию ``subscriptions.db``.

    Пример использования::

        db = Database()
        db.add_subscription(Subscription(name="VK Музыка", price=169, billing_date=15, user_id=123))
        subs = db.get_subscriptions(user_id=123)
    """

    def __init__(self, db_path: Path = DEFAULT_DB_PATH) -> None:
        """Инициализирует соединение и создаёт таблицы при необходимости."""
        self._conn = sqlite3.connect(str(db_path))
        self._create_tables()

    def _create_tables(self) -> None:
        """Создаёт таблицу ``subscriptions``, если она ещё не существует."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL,
                name         TEXT    NOT NULL,
                price        REAL    NOT NULL,
                billing_date INTEGER NOT NULL,
                active       INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        self._conn.commit()

    def add_subscription(self, sub: Subscription) -> int:
        """Добавляет подписку в базу данных.

        :param sub: Объект :class:`~subscription_tracker.models.Subscription`.
        :return: ``id`` вставленной записи.
        """
        cursor = self._conn.execute(
            "INSERT INTO subscriptions (user_id, name, price, billing_date, active) "
            "VALUES (?, ?, ?, ?, ?)",
            (sub.user_id, sub.name, sub.price, sub.billing_date, int(sub.active)),
        )
        self._conn.commit()
        return cursor.lastrowid  # type: ignore[return-value]

    def get_subscriptions(self, user_id: int) -> List[Subscription]:
        """Возвращает список активных подписок пользователя.

        :param user_id: Telegram ID пользователя.
        :return: Список объектов :class:`~subscription_tracker.models.Subscription`.
        """
        rows = self._conn.execute(
            "SELECT id, user_id, name, price, billing_date, active "
            "FROM subscriptions WHERE user_id = ? AND active = 1",
            (user_id,),
        ).fetchall()
        return [
            Subscription(
                id=r[0], user_id=r[1], name=r[2],
                price=r[3], billing_date=r[4], active=bool(r[5]),
            )
            for r in rows
        ]

    def delete_subscription(self, sub_id: int) -> None:
        """Помечает подписку как неактивную (мягкое удаление).

        :param sub_id: Идентификатор подписки.
        """
        self._conn.execute(
            "UPDATE subscriptions SET active = 0 WHERE id = ?", (sub_id,)
        )
        self._conn.commit()

    def total_monthly(self, user_id: int) -> float:
        """Считает суммарные ежемесячные расходы пользователя.

        :param user_id: Telegram ID пользователя.
        :return: Сумма стоимостей всех активных подписок.
        """
        row = self._conn.execute(
            "SELECT COALESCE(SUM(price), 0) FROM subscriptions "
            "WHERE user_id = ? AND active = 1",
            (user_id,),
        ).fetchone()
        return float(row[0])

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self._conn.close()
