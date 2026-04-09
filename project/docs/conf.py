"""Конфигурация Sphinx для проекта SubscriptionTracker."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "SubscriptionTracker"
author = "Студент ИКБО-42-24"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

language = "ru"

html_theme = "alabaster"
html_static_path = ["_static"]
