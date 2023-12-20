from ..core import datalocator

import typing
import os
import functools

FILES_KEY = "files"
MODIFY_SECTION = "Modify"
ONLINE_CHAT_SECTION = "Online Chat"


prompts: typing.Dict[str, str] = {}

_hidden_sections = {MODIFY_SECTION: "", ONLINE_CHAT_SECTION: ""}


def getPrompt(prompt_key: str) -> str:
    return prompts.get(prompt_key, "")


@functools.cache
def makeModifyPrompt(other_prompt_key: str) -> str:
    return _hidden_sections[MODIFY_SECTION] + "\n" + getPrompt(other_prompt_key)


@functools.cache
def makeOnlinePrompt(other_prompt_key: str) -> str:
    return getPrompt(other_prompt_key) + "\n" + _hidden_sections[ONLINE_CHAT_SECTION]


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
        if section not in _hidden_sections:
            prompts[section] = "\n".join(prompt_list)
        else:
            _hidden_sections[section] = "\n".join(prompt_list)
