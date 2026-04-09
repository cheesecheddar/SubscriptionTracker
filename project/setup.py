"""Скрипт сборки пакета subscription-tracker с помощью setuptools."""

from setuptools import setup, find_packages

setup(
    name="subscription-tracker",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "python-telegram-bot>=21.0",
        "APScheduler>=3.10",
        "python-dotenv>=1.0",
    ],
    entry_points={
        "console_scripts": [
            "subscription-tracker=subscription_tracker.__main__:main",
        ],
    },
)
