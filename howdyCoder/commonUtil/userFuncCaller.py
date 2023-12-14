from . import mpLogging
from ..core.commonGlobals import FUNC_GROUP

import typing
from typing import Any
from dataclasses import dataclass
import inspect
import traceback
import io
from contextlib import redirect_stdout, redirect_stderr


@dataclass
class FunctionArgSpecs:
    has_var_kwarg: bool
    arg_names: typing.List[str]


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
        self._function_name_to_arg_specs: typing.Dict[str, FunctionArgSpecs] = {}

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
            self.defineArgumentFilters(self.name)
            res = self.name in self._function_scope
        return res

    def __call__(self, *args, **kwargs):
        """Wrapper function to call func, so that userFuncCaller can still be used as a regular function"""
        return self.callFunc(self.name, *args, **kwargs)

    def callFunc(self, function_name: str, *args, _caller_name="", **kwargs) -> Any:
        """
        Call the function in a hopefully safe-ish manner
        Keyword arguments will be filtered out but arguments will be passed forward
        also get any data that was going to stdout or stderr and return that
        """
        filteredParamters = self.filterArguments(function_name, kwargs)
        try:
            with redirect_stderr(io.StringIO()) as f_err:
                with redirect_stdout(io.StringIO()) as f_std:
                    ret_val = self._function_scope[function_name](
                        *args, **filteredParamters
                    )
            return ret_val, f_std.getvalue(), f_err.getvalue()
        except Exception as e:
            exception_str = ""
            if _caller_name:
                exception_str = f"Exception while calling from {_caller_name} a function named: {function_name}\n"
            else:
                exception_str = (
                    f"Exception while calling function named: {function_name}\n"
                )
            exception_str += "-" * 10 + f"\n{e}"
            mpLogging.error(exception_str, group=FUNC_GROUP)
            return None, None, None

    def filterArguments(
        self, function_name: str, passed_in_kwarg: typing.Dict[str, Any]
    ) -> dict[str, Any]:
        """
        Compare the kwargs to argument mapping and filter out if **kwarg is not present
        Meant to make it safe to call without worrying about passing in extra kwargs for unkown functions
        Args:
            keyowrdArguments:
                keyword arguments to filter based on passed in functions

        Returns:
            A dict to be used as the new kwargs for the function call
        """
        if function_name not in self._function_name_to_arg_specs:
            self.defineArgumentFilters(function_name)
        function_arg_specs = self._function_name_to_arg_specs[function_name]
        if not function_arg_specs.has_var_kwarg:
            # sadly **kwargs was not included on passed in function
            # so we're going to filter out the arguments that won't be used now
            if len(function_arg_specs.arg_names) > 0:
                return {
                    name: passed_in_kwarg[name]
                    for name in function_arg_specs.arg_names
                    if name in passed_in_kwarg
                }
            else:
                # no **kwargs and function has no arguments so pass in nothing
                return {}

        return passed_in_kwarg

    def defineArgumentFilters(self, function_name: str):
        """
        Go through arguments and determine argument names and if special arguments are present
        """
        sig = inspect.signature(self._function_scope[function_name])
        has_var_kwarg = False
        arg_names = []
        for param in sig.parameters.values():
            """
            POSITIONAL_ONLY not currently supported
            """
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                has_var_kwarg = True
            elif (
                param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                or param.kind == inspect.Parameter.KEYWORD_ONLY
            ):
                arg_names.append(param.name)
        self._function_name_to_arg_specs[function_name] = FunctionArgSpecs(
            has_var_kwarg, arg_names
        )
