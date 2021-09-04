import argparse
import os
import ast
from docstringsParser import ModuleParser
import sys
from pdfConverter import pdfConverter
from config import myObj


def parse_name(path):
    pathList = path.split('/')
    splittedName = pathList[-1].split('.')
    if("py" in splittedName):
        splittedName = splittedName[:-1]
    lengthObj = len(splittedName)
    if len(pathList) > 1:
        fullPath = '/'.join(pathList[:-1])
        fullPath += '/' + splittedName[0] + '.py'
    else:
        fullPath = splittedName[0] + '.py'
    moduleName = splittedName[0]
    first = None
    second = None
    if lengthObj > 3:
        raise Exception('Unexpected number of .STUFF')
    if lengthObj >= 2:
        first = splittedName[1]
    if lengthObj == 3:
        second = splittedName[2]
    return myObj(fullPath, moduleName, first, second)


def check_file(path):
    input = path.split('.')[0]
    input += ".py"
    exists = os.path.isfile(input)
    if exists:
        pass
    else:
        raise Exception('You picked the wrong neighbourhood, fool')


def createParser():
    parser = argparse.ArgumentParser(description='Перевод docstrings в PDF.')
    parser.add_argument('-i', '--input',
                        required=True, help='Путь до python файла или его объектов'
                                            '/dir/module.Class or /dir/module.Class.Func')
    return parser

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    input = namespace.input
    check_file(input)
    myTuple = parse_name(input)
    try:
        with open(myTuple.fullPath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception:
        print("No such file")
        sys.exit()
    tree = ast.parse(code)
    lister = ModuleParser(myTuple.moduleName, tree, myTuple, code)
    info = lister.get_info()
    pdf = pdfConverter(lister, "example.pdf")
    print('Successfully created')
