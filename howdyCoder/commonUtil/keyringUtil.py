import keyring

KEYRING_APP_NAME = "HowdyCoder"


def isKeySet(key_name: str):
    return keyring.get_password(KEYRING_APP_NAME, key_name) is not None


def getKey(key_name: str):
    return keyring.get_password(KEYRING_APP_NAME, key_name)


def setKey(key_name: str, key: str):
    keyring.set_password(KEYRING_APP_NAME, key_name, key)
