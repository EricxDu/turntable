from random import choice, randint
import os
import re
import string
import unittest

from turntable import TurnTable


class FakeMPlayer():
    def __init__(self):
        return None


class TestTable(TurnTable):
    def __init__(self):
        self.p = FakeMPlayer


class StringsTestCase(unittest.TestCase):
    def setUp(self):
        super(StringsTestCase, self).setUp()
        self.o = TestTable()

    def test_strings(self):
        for i in range(100):
            print("test: " + str(i))
            filename = (''.join(choice(string.ascii_letters)
                        for _ in range(randint(1, 60))))
            for _ in range(randint(2, 20)):
                sep = choice((' ', '-', '.', '_'))
                ran = randint(1, len(filename))
                filename = filename[:ran] + sep + filename[ran:]
            self.o.p.filename = filename
            name = os.path.splitext(filename)[0]
            expect = ''.join(re.split(' |-|\.|_', name))
            results = (self.o.get_sort(),
                       self.o.get_art(),
                       self.o.get_name())
            compare = ''.join(''.join(results).split())
            print("parse string: " + name)
            print("expect: " + expect)
            print("result: " + compare)
            self.assertEqual(expect, compare)

    def tearDown(self):
        super(StringsTestCase, self).tearDown()
        del self.o
