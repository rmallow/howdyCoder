from ..core.commonGlobals import DATA_SET

import ast
from collections import namedtuple
import typing

Import = namedtuple("Import", ["module", "name", "alias", "code"])


def getImports(root: ast.Module):
    """Find the imports in the module and return these in a a named tuple"""
    # walk will recursively check so this will find ALL import_statements
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            module = ""
        elif isinstance(node, ast.ImportFrom):
            module = node.module
        else:
            continue

        for n in node.names:
            yield Import(module, n.name, n.asname, ast.unparse(node))


def getImportsUnique(root: ast.Module):
    imports = set()
    imp_statements = set()
    for imp in getImports(root):
        imp_statements.add(imp.code)
        if imp.module:
            imports.add(imp.module.split(".")[0])
        elif imp.name and imp.name != "*":
            imports.add(imp.name.split(".")[0])
    return list(imports), list(imp_statements)


def getFunctions(root: ast.Module) -> typing.List[ast.FunctionDef]:
    """Find the function defenitions and return their code in a list"""
    return [
        node for node in ast.iter_child_nodes(root) if isinstance(node, ast.FunctionDef)
    ]


def getSuggestedParameterNames(root: ast.Module) -> typing.List[str]:
    function_defs = getFunctions(root)
    """
    FunctionDef contains an ast.arguments that has posonlyargs, args, vararg, kwonlyargs, and kwarg
    posonlyargs - as of right now we don't pass in any posonlyargs, and they are not allowed
    args and kwonlyargs - these we do pass in and will return
    vararg and kwarg - these are *args and **kwargs type arguments and will be ignored as we don't suggest these
    """
    parameters = set()
    for f in function_defs:
        parameters.update([arg.arg for arg in f.args.args])
        parameters.update([arg.arg for arg in f.args.kwonlyargs])
    return list(parameters)


def getSuggestedDataSetNames(root: ast.Module) -> typing.List[str]:
    function_defs = getFunctions(root)
    data_set_names = set()

    def handleConstants(c: ast.Constant):
        nonlocal data_set_names
        if isinstance(c, ast.Constant):
            try:
                v = ast.literal_eval(ast.unparse(c))
                if isinstance(v, str):
                    data_set_names.add(v)
            except Exception as _:
                pass  # this really shouldn't

    for f in function_defs:
        for node in ast.walk(f):
            if isinstance(node, ast.Subscript):
                if ast.unparse(node.value) == DATA_SET:
                    handleConstants(node.slice)
                    for slice_child in ast.iter_child_nodes(node.slice):
                        handleConstants(slice_child)
    return list(data_set_names)
