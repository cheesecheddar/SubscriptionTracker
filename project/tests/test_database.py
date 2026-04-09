"""Тесты для модуля :mod:`subscription_tracker.database`."""

import tempfile
from pathlib import Path

from subscription_tracker.database import Database
from subscription_tracker.models import Subscription


def _make_db() -> Database:
    """Создаёт временную базу данных для тестирования."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    return Database(db_path=Path(tmp.name))


def test_add_and_get() -> None:
    """Проверяет добавление и получение подписки."""
    db = _make_db()
    sub = Subscription(name="Spotify", price=199, billing_date=10, user_id=1)
    sub_id = db.add_subscription(sub)
    assert sub_id is not None

    subs = db.get_subscriptions(user_id=1)
    assert len(subs) == 1
    assert subs[0].name == "Spotify"
    db.close()


def test_delete() -> None:
    """Проверяет мягкое удаление подписки."""
    db = _make_db()
    sub = Subscription(name="Netflix", price=999, billing_date=5, user_id=2)
    sub_id = db.add_subscription(sub)
    db.delete_subscription(sub_id)

    subs = db.get_subscriptions(user_id=2)
    assert len(subs) == 0
    db.close()


def test_total_monthly() -> None:
    """Проверяет подсчёт суммарных расходов."""
    db = _make_db()
    db.add_subscription(Subscription(name="A", price=100, billing_date=1, user_id=3))
    db.add_subscription(Subscription(name="B", price=250, billing_date=15, user_id=3))

    assert db.total_monthly(user_id=3) == 350.0
    db.close()
