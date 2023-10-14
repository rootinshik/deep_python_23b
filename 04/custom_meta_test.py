import unittest

from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_class_attr(self):
        class CustomClass(metaclass=CustomMeta):
            x = 1
            _y = 2
            __z = 3

        self.assertFalse(hasattr(CustomClass, "x"))
        self.assertTrue(hasattr(CustomClass, "custom_x"))
        self.assertEqual(CustomClass.custom_x, 1)

        self.assertFalse(hasattr(CustomClass, "_y"))
        self.assertTrue(hasattr(CustomClass, "_custom_y"))
        self.assertEqual(CustomClass._custom_y, 2)

        self.assertFalse(hasattr(CustomClass, "_CustomClass__z"))
        self.assertTrue(hasattr(CustomClass, "_CustomClass__custom_z"))
        self.assertEqual(CustomClass._CustomClass__custom_z, 3)

    def test_instance_attr(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        inst = CustomClass()

        self.assertFalse(hasattr(inst, "x"))
        self.assertTrue(hasattr(inst, "custom_x"))
        self.assertEqual(inst.custom_x, 50)

        self.assertFalse(hasattr(inst, "val"))
        self.assertTrue(hasattr(inst, "custom_val"))
        self.assertEqual(inst.custom_val, 99)

        self.assertFalse(hasattr(inst, "line"))
        self.assertTrue(hasattr(inst, "custom_line"))
        self.assertEqual(inst.custom_line(), 100)

        self.assertFalse(hasattr(inst, "__custom__str__"))
        self.assertTrue(hasattr(inst, "__str__"))
        self.assertEqual(str(inst), "Custom_by_metaclass")

    def test_dynamic_add_attr(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        inst = CustomClass()
        inst.dynamic = "added later"

        self.assertFalse(hasattr(inst, "dynamic"))
        self.assertTrue(hasattr(inst, "custom_dynamic"))
        self.assertEqual(inst.custom_dynamic, "added later")

    def test_setattr_in_inst_class(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

            def __setattr__(self, key, value):
                super().__setattr__(key, 10)

        inst = CustomClass()
        inst.value = 15

        self.assertFalse(hasattr(inst, "value"))
        self.assertTrue(hasattr(inst, "custom_value"))
        self.assertNotEqual(inst.custom_value, 15)
        self.assertEqual(inst.custom_value, 10)

    def test_setattr_in_parent_class(self):
        class CustomClassParent(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

            def __setattr__(self, key, value):
                super().__setattr__(key, 10)

        class CustomClass(CustomClassParent):
            ...

        inst = CustomClass()
        inst.value = 15

        self.assertFalse(hasattr(inst, "value"))
        self.assertTrue(hasattr(inst, "custom_value"))
        self.assertNotEqual(inst.custom_value, 15)
        self.assertEqual(inst.custom_value, 10)


if __name__ == "__main__":
    unittest.main()
