import ast
from collections import namedtuple
import typing

Import = namedtuple("Import", ["module", "name", "alias", "code"])


def getImports(root):
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


def getImportsUnique(root):
    imports = set()
    imp_statements = set()
    for imp in getImports(root):
        imp_statements.add(imp.code)
        if imp.module:
            imports.add(imp.module.split(".")[0])
        elif imp.name and imp.name != "*":
            imports.add(imp.name.split(".")[0])
    return list(imports), list(imp_statements)


def getFunctions(root) -> typing.List[ast.FunctionDef]:
    """Find the function defenitions and return their code in a list"""
    return [
        node for node in ast.iter_child_nodes(root) if isinstance(node, ast.FunctionDef)
    ]
