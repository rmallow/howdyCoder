from ..data.datalocator import PROMPTS_FILE

import configparser
import typing
import os

prompts: typing.Dict[str, str] = {}

"""If the prompt singleton is being loaded for the first time run some initalization code"""
first_import = True
if first_import == True:
    first_import = False
    config = configparser.ConfigParser()
    config.read(PROMPTS_FILE)

    for section in config.sections():
        if "file" in config[section]:
            with open(
                os.path.join(os.path.dirname(PROMPTS_FILE), config[section]["file"]),
                "r",
            ) as f:
                prompts[section] = f.read()
