from collections import defaultdict

from ..core.dataStructs import (
    AlgoSettings,
)

import typing

NodeMapping = typing.DefaultDict[str, typing.List[str]]


def getTopoSort(
    algo_config: AlgoSettings,
) -> typing.Tuple[typing.List[typing.List[str]], NodeMapping, NodeMapping]:
    levels = [[]]
    for key, data_source in algo_config.data_sources.items():
        for output in data_source.output:
            levels[0].append(f"{key}-{output}")
    outgoing_mapping = defaultdict(list)
    incoming_mapping = defaultdict(list)
    incoming_count = defaultdict(int)
    for key, action in algo_config.action_list.items():
        incoming_count[key] = len(action.input_)
        for name in action.input_.keys():
            outgoing_mapping[name].append(key)
            incoming_mapping[key].append(name)

    while levels[-1]:
        levels.append([])
        for n in levels[-2]:
            for other in outgoing_mapping[n]:
                incoming_count[other] -= 1
                if incoming_count[other] == 0:
                    levels[-1].append(other)
                    del incoming_count[other]
    del levels[-1]
    return levels, outgoing_mapping, incoming_mapping
