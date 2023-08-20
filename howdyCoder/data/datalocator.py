"""
Importable settings file
"""
import os
import sys

SETTINGS_FILE = (
    os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)) + r"/settings.ini"
)

LIBRARIES_FILE = (
    os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)) + r"/libraries.ini"
)

TEST_FILE = (
    os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
    + r"/test_config.yml"
)
