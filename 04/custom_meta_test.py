import unittest

from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):

    def test_class_attr(self):
        class CustomClass(metaclass=CustomMeta):
            x = 1
            _y = 2
            __z = 3

        with self.assertRaises(AttributeError):
            CustomClass.x
        self.assertEqual(CustomClass.custom_x, 1)

        with self.assertRaises(AttributeError):
            CustomClass._y
        self.assertEqual(CustomClass._custom_y, 2)

        with self.assertRaises(AttributeError):
            CustomClass._CustomClass__z
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

        with self.assertRaises(AttributeError):
            inst.x
        self.assertEqual(inst.custom_x, 50)

        with self.assertRaises(AttributeError):
            inst.val
        self.assertEqual(inst.custom_val, 99)

        with self.assertRaises(AttributeError):
            inst.line()
        self.assertEqual(inst.custom_line(), 100)

        self.assertEqual(str(inst), "Custom_by_metaclass")
        with self.assertRaises(AttributeError):
            inst.__custom_str__

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

        with self.assertRaises(AttributeError):
            inst.dynamic
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

        with self.assertRaises(AttributeError):
            inst.value()
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

        with self.assertRaises(AttributeError):
            inst.value()
        self.assertNotEqual(inst.custom_value, 15)
        self.assertEqual(inst.custom_value, 10)


if __name__ == "__main__":
    unittest.main()
