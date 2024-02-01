from . import datalocator
from ..commonUtil import keyringUtil

PARAMETERS = "Parameters"

_parameters = {}

settings_config = datalocator.getConfig(datalocator.SETTINGS)
_parameters = settings_config.get(PARAMETERS, {})
