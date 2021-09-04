import ast
from config import  moduleInfo, classInfo, funcInfo
import re
from collections import namedtuple

definition = namedtuple('defs', 'definition name docstring')

def cut_class(info, name):
    for one in info.classes:
        if one.name == name:
            return one
    return None


def cut_func(info, name):
    for fnc in info.functions:
        if fnc.name == name:
            return fnc
    return None

class ModuleParser:
    def __init__(self, name, node, tuple, code):
        self.name = name
        self.node = node
        self.info = None
        self.funcs = []
        self.classes = []
        self.tuple = tuple
        self.current_func = None
        self.current_class = None
        self.code = code
        self.state = 0 # 0 - module, 1 - class, 2 - func, 3 - class.func
        self.set_info()
        self.cut_spec()

    def get_info(self):
        if(self.state==0):
            return self.info
        elif(self.state==1):
            return self.current_class
        elif(self.state==2):
            return self.current_func
        elif(self.state==3):
            return self.current_func

    def set_info(self):
        objects = re.findall(r'((?:class .+?:)|(?:def .+?:))\n*\s*"""((?:\n*|.*?)+)"""', self.code)
        self.all = objects
        for one in objects:
            name = one[0].split(' ')[1].split(':')[0].split('(')[0]
            def_one = definition(one[0], name, one[1])
            if (re.search('class', def_one.definition)):
                self.classes.append(def_one)
            elif (re.search('def', def_one.definition)):
                self.funcs.append(def_one)

        docstrings = ast.get_docstring(self.node)
        classParser = ClassParser(self.classes, self.funcs)
        functionParser = FuncParser(self.funcs)
        for child in ast.iter_child_nodes(self.node):
            if type(child) == ast.ClassDef:
                classParser.visit(child)
            elif type(child) == ast.FunctionDef:
                functionParser.visit(child)

        info = moduleInfo(self.name, docstrings, classParser.info, functionParser.info)
        self.info = info

    def cut_spec(self):
        if self.tuple.first is not None and self.tuple.second is None:
            cls_info = cut_class(self.info, self.tuple.first)
            if cls_info is None:
                fnc_info = cut_func(self.info, self.tuple.first)
                self.current_class = None
                self.current_func = fnc_info
                self.state = 2
            else:
                self.current_class = cls_info
                self.state = 1
        elif self.tuple.second is not None:
            cls_info = cut_class(self.info, self.tuple.first)
            self.current_class = cls_info
            fnc_info = cut_func(cls_info, self.tuple.second)
            self.current_func = fnc_info
            self.state = 3


class ClassParser(ast.NodeVisitor):
    def __init__(self, classes, funcs):
        self.info = []
        self.classes = classes
        self.funcs = funcs

    def visit_ClassDef(self, node):
        name = node.name
        docstrings = ast.get_docstring(node)
        defn = None
        for cls in self.classes:
            if (cls.name == name):
                defn = cls.definition
                break
        funcParser = FuncParser(self.funcs)
        funcParser.visit(node)
        functions = funcParser.info
        class_info = classInfo(name, docstrings, functions, defn)
        self.info.append(class_info)


class FuncParser(ast.NodeVisitor):
    def __init__(self, funcs):
        self.info = []
        self.funcs = funcs

    def visit_FunctionDef(self, node):
        name = node.name
        docstrings = ast.get_docstring(node)
        defn = None
        for func in self.funcs:
            if(func.name == name):
                defn = func.definition
                break
        func_info = funcInfo(name, docstrings, defn)

        self.info.append(func_info)