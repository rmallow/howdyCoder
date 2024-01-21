import typing

VARIABLE_TEXT_LIST_ARG_NAME = "_variable_text_list"  # we represent arg name as a string so we can store it by same var
STARTING_BRACE = "{"
ENDING_BRACE = "}"


def isVarText(text: str):
    return (
        len(text) >= 3
        and text.startswith(STARTING_BRACE)
        and text.endswith(ENDING_BRACE)
    )


def textMerger(data_set: typing.Dict[str, str], *args, **kwargs):
    """For use in internal library"""
    variable_text_list: typing.List[str] = kwargs[VARIABLE_TEXT_LIST_ARG_NAME]
    for x in range(len(variable_text_list)):
        if isVarText(variable_text_list[x]):
            variable_text_list[x] = str(data_set.get(variable_text_list[1:-1], ""))
    return "".join(variable_text_list)
