import openai
from . import keyringUtil
from ..core import keySingleton
import re


OPEN_AI_KEYRING_NAME = "OPEN_AI_API_KEY"
OPEN_AI_KEY_DATA_NAME = "Open AI (Chat GPT)"

COMPLETION_MODEL = "gpt-4"
TRANSCRIPTION_MODEL = "whisper-1"

PIP_SERACH = "pip"
CODE_INDICATOR = "```"
PYTHON_SEARCH = CODE_INDICATOR + "python"


def setKey(key: str):
    openai.api_key = key


def setKeyFromKeyring():
    openai.api_key = keyringUtil.getKey(OPEN_AI_KEYRING_NAME)


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


def getChatCompletion(system_prompt: str, user_prompt: str):
    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    choices = completion.choices
    first_message = choices[0].message
    content = first_message["content"]
    return content


def transcribeAudio(audio_file):
    audio_file = open(audio_file, "rb")
    return openai.Audio.transcribe(TRANSCRIPTION_MODEL, audio_file)


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


# on first import add to singleton
keySingleton.addKeySetData(
    OPEN_AI_KEY_DATA_NAME,
    keySingleton.KeySetData(OPEN_AI_KEYRING_NAME, setKey, testValid),
)
