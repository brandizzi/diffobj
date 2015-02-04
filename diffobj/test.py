import unittest
import random

import diffobj

class Tabula(object): pass

class DiffObjTest(unittest.TestCase):
    def test_create_attribute(self):
        old = Tabula()
        new = Tabula()
        new.attr = 3
        diff = diffobj.diff(old, new)
        diffobj.patch(old, diff)

        self.assertEquals(3, old.attr)
