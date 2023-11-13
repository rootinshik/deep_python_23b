import weakref


class DefaultAttrs:
    def __init__(self, val1, val2):
        self.attr1 = val1
        self.attr2 = val2


class SlotsAttrs:
    __slots__ = ("attr1", "attr2")

    def __init__(self, val1, val2):
        self.attr1 = val1
        self.attr2 = val2


class WeakrefAttr:
    def __init__(self, val1, val2):
        self.attr1 = weakref.ref(val1)
        self.attr2 = weakref.ref(val2)


class Value:
    ...
