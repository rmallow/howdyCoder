from .commonGlobals import KEY, MAPPING, ACTION_LIST, DATA_SOURCES, ProgramTypes

import typing
from enum import Enum
from dataclasses import dataclass, field, fields
from dataclass_wizard import JSONWizard, property_wizard, fromdict


@dataclass(frozen=True)
class KeyLabelPair:
    key: str
    label: str


@dataclass()
class StreamSettings:
    url: str
    key_label_list: typing.List[KeyLabelPair]

    def toConfig(self):
        return_config = {KEY: self.url}
        if len(self.key_label_list) > 0:
            return_config[MAPPING] = {}
            for key_label in self.key_label_list:
                return_config[MAPPING][key_label.key] = key_label.label
        return return_config


class Modes(str, Enum):
    NONE = ""
    STANDBY = "Standby"
    STARTED = "Started"
    STOPPED = "Stopped"


@dataclass
class ProgramStatusData:
    send_time: float = 0.0
    receive_time: float = 0.0
    runtime: float = 0.0
    mode: Modes = Modes.STANDBY
    back_time: float = 0.0
    type_: str = ProgramTypes.PROGRAM.value


@dataclass
class AlgoStatusData(ProgramStatusData):
    data_length: int = 0
    feed_last_update_time: float = 0.0
    columns: list = field(default_factory=list)


@dataclass
class InputData(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    code: str = ""
    data_source_name: str = ""
    val: typing.Any = None


@dataclass
class FunctionSettings(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    code: str = ""
    name: str = ""
    imports: typing.List[str] = field(default_factory=list)
    import_statements: typing.List[str] = field(default_factory=list)
    user_func: typing.Any = None


@dataclass
class InputSettings(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    name: str = ""
    requires_new: bool = False
    period: int = 1


@dataclass
class Parameter(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    name: str = ""
    value: typing.Any = None


@dataclass
class ItemSettings(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    name: str = ""
    type_: str = ""
    flatten: bool = False
    period: int = 1
    single_shot: bool = False
    parameters: typing.Dict[str, Parameter] = field(default_factory=dict)
    setup_funcs: typing.Dict[str, FunctionSettings] = field(default_factory=dict)

    def clear(self):
        self.__init__({})


@dataclass
class ActionSettings(ItemSettings, JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    input_: typing.Dict[str, InputSettings] = field(default_factory=dict)
    input_data_type: str = ""
    aggregate: str = ""
    calc_func: FunctionSettings | None = None
    output_func: FunctionSettings | None = None


@dataclass
class DataSourceSettings(ItemSettings, JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    output: typing.Union[typing.List[str], typing.Dict[str, str]] = field(
        default_factory=list
    )
    # type specific
    get_func: FunctionSettings | None = None
    input_type: str = ""
    key: str = ""


USER_FUNC = "user_func"
SETUP_FUNCS = "setup_funcs"

test_once = True
if test_once:
    test_once = False

    assert any(
        field.name == SETUP_FUNCS for field in fields(ItemSettings)
    ), "Changed setuup funcs field name without changing string"
    assert any(
        field.name == USER_FUNC for field in fields(FunctionSettings)
    ), "Changed user func field name without changing string"


@dataclass
class AlgoSettings(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    name: str = ""
    data_sources: typing.Dict[str, DataSourceSettings] = field(default_factory=dict)
    action_list: typing.Dict[str, ActionSettings] = field(default_factory=dict)

    def clear(self):
        self.__init__({})

    def getGroupDict(self, group: str) -> typing.Dict[str, ItemSettings]:
        if group == ACTION_LIST:
            return self.action_list
        elif group == DATA_SOURCES:
            return self.data_sources
        assert False, "invalid group"


@dataclass
class ScriptSettings(ItemSettings, JSONWizard, metaclass=property_wizard):
    function: FunctionSettings | None = None


@dataclass
class ProgramSettings(JSONWizard, metaclass=property_wizard):
    class _(JSONWizard.Meta):
        key_transform_with_dump = "SNAKE"

    type_: str = ""
    name: str = ""
    settings: typing.Union[AlgoSettings, ScriptSettings] = None
