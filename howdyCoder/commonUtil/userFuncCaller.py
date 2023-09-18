from . import mpLogging
from ..core.commonGlobals import FUNC_GROUP

import typing
from typing import Any
import inspect
import traceback
import io
from contextlib import redirect_stdout, redirect_stderr


class UserFuncCaller:
    """
    Used to call user inputted functions

    Extra care has to be taken when calling a user defined function
    This class should be used in any case where an unkown function is called
    """

    def __init__(
        self,
        code: str = "",
        import_statements: typing.List[str] = None,
        name: str = "",
        *args,
        **kwargs,
    ):
        self._code: str = code
        self._import_statements: typing.List[str] = (
            import_statements if import_statements else []
        )
        self.name: str = name
        self._function_scope: typing.Dict = {}
        self._functionArgNames: list[str] = []
        self._hasVarArg: bool = False
        self._hasVarKwargs: bool = False

    def setup(self):
        for imp in self._import_statements:
            try:
                exec(imp, self._function_scope)
            except Exception as e:
                # this isn't necessarily bad if an override has happened
                mpLogging.warning(
                    "Exception during import statement",
                    description=f"Statement: {imp}, exception: {traceback.format_exc()}",
                    group=FUNC_GROUP,
                )
        res = False
        try:
            exec(self._code, self._function_scope)
        except Exception as e:
            mpLogging.critical(
                "Exception during function statement",
                description=f"Statement: {self._code}, exception: {traceback.format_exc()}",
                group=FUNC_GROUP,
            )
        else:
            # probably worked so lets proceed like normal
            self.defineArgumentFilters()
            res = self.name in self._function_scope
        return res

    def __call__(self, *args, **kwargs):
        """Wrapper function to call func, so that userFuncCaller can still be used as a regular function"""
        return self.callFunc(*args, **kwargs)

    def callFunc(self, *args, _caller_name="", **kwargs) -> Any:
        """
        Call the function in a hopefully safe-ish manner
        Keyword arguments will be filtered out but arguments will be passed forward
        also get any data that was going to stdout or stderr and return that
        """
        filteredParamters = self.filterArguments(kwargs)
        try:
            with redirect_stderr(io.StringIO()) as f_err:
                with redirect_stdout(io.StringIO()) as f_std:
                    ret_val = self._function_scope[self.name](
                        *args, **filteredParamters
                    )
            return ret_val, f_std.getvalue(), f_err.getvalue()
        except Exception as e:
            exception_str = ""
            if _caller_name:
                exception_str = f"Exception while calling from {_caller_name} a function named: {self.name}\n"
            else:
                exception_str = f"Exception while calling function named: {self.name}\n"
            exception_str += "-" * 10 + f"\n{e}"
            mpLogging.error(exception_str, group=FUNC_GROUP)
            return None, None, None

    def filterArguments(self, passed_in_kwarg: typing.Dict[str, Any]) -> dict[str, Any]:
        """
        Compare the kwargs to argument mapping and filter out if **kwarg is not present
        Meant to make it safe to call without worrying about passing in extra kwargs for unkown functions
        Args:
            keyowrdArguments:
                keyword arguments to filter based on passed in functions

        Returns:
            A dict to be used as the new kwargs for the function call
        """

        if not self._hasVarKwargs:
            # sadly **kwargs was not included on passed in function
            # so we're going to filter out the arguments that won't be used now
            if len(self._functionArgNames) > 0:
                return {
                    name: passed_in_kwarg[name]
                    for name in self._functionArgNames
                    if name in passed_in_kwarg
                }
            else:
                # no **kwargs and function has no arguments so pass in nothing
                return {}

        return passed_in_kwarg

    def defineArgumentFilters(self):
        """
        Go through arguments and determine argument names and if special arguments are present
        """
        sig = inspect.signature(self._function_scope[self.name])
        for param in sig.parameters.values():
            """
            POSITIONAL_ONLY not currently supported
            """
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                self._hasVarKwargs = True
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                self._hasVarArg = True
            elif (
                param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                or param.kind == inspect.Parameter.KEYWORD_ONLY
            ):
                self._functionArgNames.append(param.name)
