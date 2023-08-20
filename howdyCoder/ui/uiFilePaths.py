import os
import pathlib


UI_DIR = "qtUiFiles/"
RES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), "res")

"""
Progress Steps UI Files
"""
CHECKMARK_IMAGE = os.path.join(RES_DIR, "checkmark.png")
X_IMAGE = os.path.join(RES_DIR, "x.png")

"""
matplotlib files
"""
BASE_MPL_STYLE = os.path.join(RES_DIR, "base.mplstyle")
