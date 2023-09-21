from ..data.datalocator import PROMPTS_FILE

import configparser
import typing
import os
import functools

FILES_KEY = "files"
MODIFY_SECTION = "Modify"


prompts: typing.Dict[str, str] = {}
_modify_prompt = ""


def getPrompt(prompt_key: str) -> str:
    return prompts.get(prompt_key, "")


@functools.cache
def makeModifyPrompt(other_prompt_key: str) -> str:
    return _modify_prompt + "\n" + getPrompt(other_prompt_key)


"""If the prompt singleton is being loaded for the first time run some initalization code"""
first_import = True
if first_import == True:
    first_import = False
    config = configparser.ConfigParser()
    config.read(PROMPTS_FILE)

    for section in config.sections():
        prompt_list = []
        if FILES_KEY in config[section]:
            file_list = config[section][FILES_KEY]
            for file_name in file_list.split(","):
                with open(
                    os.path.join(os.path.dirname(PROMPTS_FILE), file_name),
                    "r",
                ) as f:
                    prompt_list.append(f.read())
            if section != MODIFY_SECTION:
                prompts[section] = "\n".join(prompt_list)
            else:
                _modify_prompt = "\n".join(prompt_list)
