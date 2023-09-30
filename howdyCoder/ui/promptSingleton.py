from ..core import datalocator

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
for section, values in datalocator.getConfig(datalocator.PROMPTS).items():
    prompt_list = []
    if FILES_KEY in values:
        file_list = values[FILES_KEY]
        for file_name in file_list.split(","):
            with open(
                os.path.join(
                    datalocator.getDataDirPath(datalocator.PROMPTS),
                    file_name,
                ),
                "r",
            ) as f:
                prompt_list.append(f.read())
        if section != MODIFY_SECTION:
            prompts[section] = "\n".join(prompt_list)
        else:
            _modify_prompt = "\n".join(prompt_list)
