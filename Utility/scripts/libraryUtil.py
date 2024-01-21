# first include howdy coder as it's needed
import sys
import os
import pathlib


import argparse

HOWDY_CODER_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
sys.path.append(os.path.realpath(HOWDY_CODER_DIR))

from howdyCoder.core import libraryBase

PY_TO_AFL_ACTION = "pyToAfl"


def main():
    parser = argparse.ArgumentParser(description="Arguments for library utility script")
    parser.add_argument("action", choices=[PY_TO_AFL_ACTION])
    parser.add_argument("-py", dest="py_file_path")
    parser.add_argument("-afl", dest="config_file_path")
    parser.add_argument("-name", dest="name")
    parser.add_argument("-group", dest="group")
    parser.add_argument("-specific", dest="specific_function")

    args = parser.parse_args()
    if args.action == PY_TO_AFL_ACTION:
        try:
            libraryBase.pyToAfl(
                args.py_file_path,
                args.config_file_path,
                args.name,
                args.group,
                args.specific_function,
            )
        except AttributeError as e:
            print("missing some arguments for py to afl")


if __name__ == "__main__":
    main()
