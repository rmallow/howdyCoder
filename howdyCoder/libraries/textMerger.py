import typing

VARIABLE_TEXT_LIST_ARG_NAME = "_variable_text_list"  # we represent arg name as a string so we can store it by same var
STARTING_BRACE = "${"
ENDING_BRACE = "}"


def isVarText(text: str):
    return (
        len(text) > len(STARTING_BRACE) + len(ENDING_BRACE)
        and text.startswith(STARTING_BRACE)
        and text.endswith(ENDING_BRACE)
    )


def textMerger(data_set: typing.Dict[str, str], *args, **kwargs):
    """For use in internal library"""
    variable_text_list: typing.List[str] = kwargs[VARIABLE_TEXT_LIST_ARG_NAME]
    res = []
    for text in variable_text_list:
        if isVarText(text):
            text = str(
                data_set.get(text[len(STARTING_BRACE) : -len(ENDING_BRACE)], "")[0]
            )
        res.append(text)
    return "".join(res)
