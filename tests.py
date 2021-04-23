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
        for i in range(1000):
            filename = (''.join(choice(string.ascii_letters)
                        for _ in range(randint(1, 50))))
            for _ in range(randint(2, 10)):
                sep = choice(('-', '_'))
                ran = randint(1, len(filename))
                filename = filename[:ran] + sep + filename[ran:]
            self.o.p.filename = filename
            name = os.path.splitext(filename)[0]
            expect = ''.join(re.split(' |-|_', name))
            expect = ''.join(re.split(' |-|_', name))
            print("string " + str(i) + ": " + name)
            results = (self.o.get_sort(),
                       self.o.get_art(),
                       self.o.get_name())
            compare = ''.join(''.join(results).split())
            print("expect: " + expect)
            print("result: " + compare)
            self.assertEqual(expect, compare)

    def tearDown(self):
        super(StringsTestCase, self).tearDown()
        del self.o
