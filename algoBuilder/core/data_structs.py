from .configConstants import KEY, MAPPING

from dataclasses import dataclass
import typing


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
