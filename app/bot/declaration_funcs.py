import os, json

def get_func_declaration_tool() :
    with open("%s/declaration_funcs.json" % os.path.dirname(__file__), mode="r", encoding="utf-8") as file:
        data_declaration : dict[str, any] = json.load(file)
    function_declarations = [declaration for declaration in data_declaration.values()]
    return [{"type": "function", "function": decl} for decl in function_declarations]