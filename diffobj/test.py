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

    def test_drop_attribute(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        diff = diffobj.diff(old, new)
        diffobj.patch(old, diff)

        self.assertFalse(hasattr(old, 'attr'))

    def test_update_attribute(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        new.attr = 4
        diff = diffobj.diff(old, new)
        diffobj.patch(old, diff)

        self.assertEquals(4, old.attr)

    def test_error_if_creating_already_existing_attribute(self):
        old = Tabula()
        new = Tabula()
        new.attr = 3
        diff = diffobj.diff(old, new)

        old.attr = 4
        with self.assertRaises(diffobj.Conflict):
            diffobj.patch(old, diff)

    def test_error_if_updating_different_old_value(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        new.attr = 4
        diff = diffobj.diff(old, new)

        old.attr = 5
        with self.assertRaises(diffobj.Conflict):
            diffobj.patch(old, diff)

    def test_error_if_updating_non_existent_attribute(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        new.attr = 4
        diff = diffobj.diff(old, new)

        delattr(old, 'attr')
        with self.assertRaises(diffobj.Conflict):
            diffobj.patch(old, diff)

    def test_error_if_dropping_different_old_value(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        diff = diffobj.diff(old, new)

        old.attr = 5
        with self.assertRaises(diffobj.Conflict):
            diffobj.patch(old, diff)

    def test_nop_if_dropping_non_existent_attribute(self):
        old = Tabula()
        new = Tabula()
        old.attr = 3
        diff = diffobj.diff(old, new)

        delattr(old, 'attr')
        diffobj.patch(old, diff)        
        self.assertFalse(hasattr(old, 'attr'))

    def test_nop_if_creating_non_existent_attribute(self):
        old = Tabula()
        new = Tabula()
        new.attr = 3
        diff = diffobj.diff(old, new)

        old.attr = 3
        diffobj.patch(old, diff)
        self.assertEquals(3, old.attr)

