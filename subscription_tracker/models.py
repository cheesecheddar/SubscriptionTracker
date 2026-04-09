"""
Модели данных приложения.

Содержит dataclass-модели, описывающие сущности предметной области:
подписки пользователя.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Subscription:
    """Подписка пользователя на сервис.

    :param name: Название сервиса (например, «Spotify»).
    :param price: Стоимость подписки в рублях.
    :param billing_date: День месяца, когда происходит списание.
    :param user_id: Telegram ID владельца подписки.
    :param id: Уникальный идентификатор записи в БД (назначается автоматически).
    :param active: Флаг активности подписки.
    """

    name: str
    price: float
    billing_date: int
    user_id: int
    id: int | None = field(default=None)
    active: bool = field(default=True)

    def is_due_today(self) -> bool:
        """Проверяет, приходится ли дата списания на сегодня.

        :return: ``True``, если сегодняшний день совпадает с ``billing_date``.
        """
        return date.today().day == self.billing_date

    def monthly_cost(self) -> float:
        """Возвращает ежемесячные расходы по подписке.

        :return: Стоимость подписки, если она активна, иначе ``0.0``.
        """
        return self.price if self.active else 0.0
