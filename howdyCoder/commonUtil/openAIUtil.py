import openai
from . import keyringUtil
import re

MODEL = "gpt-4"
OPEN_AI_API_KEY_NAME = "OPEN_AI_API_KEY"


def setKeyDecorator(func):
    def inner(*args, **kwargs):
        openai.api_key = keyringUtil.getKey(OPEN_AI_API_KEY_NAME)
        return func(*args, **kwargs)

    return inner


def setKeyFromKeyring():
    openai.api_key = keyringUtil.getKey(OPEN_AI_API_KEY_NAME)


def testValidKeySet() -> bool:
    try:
        openai.Model.list()
    except (
        BrokenPipeError,
        EOFError,
        ConnectionResetError,
        openai.error.AuthenticationError,
        openai.error.APIConnectionError,
    ) as e:
        return False
    else:
        return True


def testValid(key: str) -> bool:
    cur_key, openai.api_key = openai.api_key, key
    ret_val = testValidKeySet()
    openai.api_key = cur_key
    return ret_val


@setKeyDecorator
def getChatCompletion(system_prompt: str, user_prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    choices = completion.choices
    first_message = choices[0].message
    content = first_message["content"]
    return content


PIP_SERACH = "pip"
CODE_INDICATOR = "```"
PYTHON_SEARCH = CODE_INDICATOR + "python"

import re


def remove(rem: str, my_string: str):
    return re.sub(".*" + rem + ".*\n?", "", my_string)


def getPythonCodeOnly(code: str):
    """
    OpenAI indicates its code in sections marked by:
    ```python
        ... code here ...
    ```
    So find those sections and then make sure they're not just sections with just a pip install command in it,
    which it somestimes does so skip those.
    """
    start = code.find(PYTHON_SEARCH)
    res = ""
    while start != -1 and not res:
        end = code.find(CODE_INDICATOR, start + len(PYTHON_SEARCH))
        code_subset = code[start + len(PYTHON_SEARCH) : end]
        if stripped := remove(PIP_SERACH, code_subset).strip():
            res = stripped
        else:
            start = code.find(PYTHON_SEARCH, end + len(CODE_INDICATOR))
    return res if res else code


first_load = True
if first_load:
    first_load = False
    setKeyFromKeyring()
