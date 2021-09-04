class myObj:
    def __init__(self, path, name, first, second):
        self.fullPath = path
        self.moduleName = name
        self.first = first
        self.second = second


class moduleInfo:
    def __init__(self, name, docstrings, classes, functions):
        self.name = name
        self.docstrings = docstrings
        self.classes = classes
        self.functions = functions


class classInfo:
    def __init__(self, name, docstrings, functions, definition):
        self.name = name
        self.docstrings = docstrings
        self.functions = functions
        self.definition = definition
        self.get_parent(definition)

    def get_parent(self, definition):
        name = definition.split(' ')[1].split(':')[0].split('(')[1].split(')')[0]
        self.parent = name if name!="" else None

    def __str__(self):
        return "Name: {} \n" \
               "Docstrings: {} \n" \
               "Parent: {}" \
               "Functions: {}".format(self.name, self.docstrings, self.parent, self.functions)


class funcInfo:
    def __init__(self, name, docstrings, definition):
        self.name = name
        self.docstrings = docstrings
        self.definition = definition

    def __str__(self):
        return "Name: {} \n" \
               "Docstrings: {} \n" \
               "Definition: {}".format(self.name, self.docstrings, self.definition)
