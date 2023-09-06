"""
Importable settings file
"""
import os
import sys

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))

SETTINGS_FILE = os.path.join(CURRENT_FILE_PATH, "settings.ini")

LIBRARIES_FILE = os.path.join(CURRENT_FILE_PATH, "libraries.ini")

PROMPTS_FILE = os.path.join(
    CURRENT_FILE_PATH, "..", "..", "howdyCoderPrompts", "prompts.ini"
)

TEST_FILE = os.path.join(CURRENT_FILE_PATH, "test_config.ini")
