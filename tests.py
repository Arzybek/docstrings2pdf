import unittest
import docstringsParser as dp
from main import parse_name, check_file
from config import myObj
import ast


class MainTestCase(unittest.TestCase):
    def test_simple_name(self):
        result = parse_name("example.py")
        self.assertTrue(result.first is None)
        self.assertTrue(result.second is None)
        self.assertTrue(result.moduleName == "example")
        self.assertTrue(result.fullPath == "example.py")

    def test_class_name(self):
        result = parse_name("examples/example.Human")
        self.assertTrue(result.first == "Human")
        self.assertTrue(result.second is None)
        self.assertTrue(result.moduleName == "example")
        self.assertTrue(result.fullPath == "examples/example.py")

    def test_class_func_name(self):
        result = parse_name("examples/example.Human.a")
        self.assertTrue(result.first == "Human")
        self.assertTrue(result.second == "a")
        self.assertTrue(result.moduleName == "example")
        self.assertTrue(result.fullPath == "examples/example.py")

    def test_exists(self):
        result = check_file("example.py")
        self.assertTrue(True)


class ParserTestCase(unittest.TestCase):
    def test_func(self):
        with open("example.py", 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        myTup = myObj("example.py", "example", "Human", "a")
        lister = dp.ModuleParser("example", tree, myTup, code)
        info = lister.get_info()
        self.assertEqual(info.name, "a")
        self.assertEqual(info.docstrings, "Built in")
        self.assertEqual(info.definition, "def a(self):")

    def test_class(self):
        with open("example.py", 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        myTup = myObj("example.py", "example", "Animal", None)
        lister = dp.ModuleParser("example", tree, myTup, code)
        info = lister.get_info()
        self.assertEqual(info.name, "Animal")
        self.assertEqual(info.docstrings, "Real animals")
        self.assertEqual(info.definition, "class Animal():")
        self.assertEqual(info.parent, None)
