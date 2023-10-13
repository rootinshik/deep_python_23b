class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        def edit_custom_setattr(self, key, value):
            classdict["__setattr__"](self, "custom_" + key, value)

        def new_custom_setattr(self, key, value):
            self.__dict__["custom_" + key] = value

        new_classdict = {}
        for key, value in classdict.items():
            if key[-2:] == "__" and key[:2] == "__":
                new_classdict[key] = value
            elif key[0] == "_":
                parts = key.split("__")
                if len(parts) == 2 and parts[0][1:] == name:
                    new_key = parts[0] + "__custom_" + parts[1]
                else:
                    new_key = "_custom_" + key[1:]
                new_classdict[new_key] = value
            else:
                new_classdict["custom_" + key] = value

        if "__setattr__" in classdict:
            new_classdict["__setattr__"] = edit_custom_setattr
        else:
            new_classdict["__setattr__"] = new_custom_setattr

        cls = super().__new__(mcs, name, bases, new_classdict, **kwargs)
        return cls

