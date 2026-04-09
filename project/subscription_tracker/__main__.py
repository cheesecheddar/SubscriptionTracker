"""
Точка входа для запуска бота командой ``python -m subscription_tracker``.

Загружает переменные окружения и запускает основной цикл бота.
"""

import os
import logging

from dotenv import load_dotenv

from subscription_tracker.bot import create_application


def main() -> None:
    """Инициализирует логирование, загружает конфигурацию и запускает бота."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Переменная окружения BOT_TOKEN не задана.")

    app = create_application(token)
    app.run_polling()


if __name__ == "__main__":
    main()
