"""
Модуль обработчиков команд Telegram-бота.

Регистрирует команды ``/start``, ``/add``, ``/list``, ``/delete``
и ``/total`` и связывает их с логикой работы с базой данных.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from subscription_tracker.database import Database

# Состояния диалога добавления подписки
NAME, PRICE, DATE = range(3)

db = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду ``/start``.

    Отправляет приветственное сообщение со списком доступных команд.

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    """
    await update.message.reply_text(
        "Привет! Я помогу отслеживать твои подписки.\n\n"
        "/add — добавить подписку\n"
        "/list — список подписок\n"
        "/delete <id> — удалить подписку\n"
        "/total — сумма расходов за месяц"
    )


async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает диалог добавления подписки (шаг 1 — запрос названия).

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    :return: Следующее состояние ``NAME``.
    """
    await update.message.reply_text("Введите название сервиса:")
    return NAME


async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет название и запрашивает стоимость (шаг 2).

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    :return: Следующее состояние ``PRICE``.
    """
    context.user_data["sub_name"] = update.message.text
    await update.message.reply_text("Введите стоимость в рублях:")
    return PRICE


async def add_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет стоимость и запрашивает дату списания (шаг 3).

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    :return: Следующее состояние ``DATE`` или повтор ``PRICE`` при ошибке.
    """
    try:
        context.user_data["sub_price"] = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите числовое значение:")
        return PRICE
    await update.message.reply_text("Введите день списания (1–31):")
    return DATE


async def add_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет дату списания, создаёт подписку в БД, завершает диалог.

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    :return: ``ConversationHandler.END``.
    """
    try:
        day = int(update.message.text)
        if not 1 <= day <= 31:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Введите корректный день (1–31):")
        return DATE

    from subscription_tracker.models import Subscription

    sub = Subscription(
        name=context.user_data["sub_name"],
        price=context.user_data["sub_price"],
        billing_date=day,
        user_id=update.effective_user.id,
    )
    db.add_subscription(sub)
    await update.message.reply_text(f"Подписка «{sub.name}» добавлена!")
    return ConversationHandler.END


async def list_subs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выводит список активных подписок пользователя.

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    """
    subs = db.get_subscriptions(update.effective_user.id)
    if not subs:
        await update.message.reply_text("У вас пока нет подписок.")
        return
    lines = [f"{s.id}. {s.name} — {s.price:.0f} ₽ (день списания: {s.billing_date})" for s in subs]
    await update.message.reply_text("\n".join(lines))


async def delete_sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет подписку по идентификатору.

    Использование: ``/delete 3``

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    """
    if not context.args:
        await update.message.reply_text("Укажите ID: /delete <id>")
        return
    try:
        sub_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")
        return
    db.delete_subscription(sub_id)
    await update.message.reply_text(f"Подписка #{sub_id} удалена.")


async def total(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает суммарные ежемесячные расходы.

    :param update: Входящее обновление Telegram.
    :param context: Контекст обработчика.
    """
    amount = db.total_monthly(update.effective_user.id)
    await update.message.reply_text(f"Итого в месяц: {amount:.0f} ₽")


def create_application(token: str) -> Application:
    """Создаёт и конфигурирует экземпляр ``Application``.

    Регистрирует все обработчики команд и диалог добавления подписки.

    :param token: Токен Telegram-бота.
    :return: Сконфигурированный объект ``Application``.
    """
    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_price)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_date)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("list", list_subs))
    app.add_handler(CommandHandler("delete", delete_sub))
    app.add_handler(CommandHandler("total", total))

    return app
