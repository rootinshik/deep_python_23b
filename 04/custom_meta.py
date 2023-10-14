class CustomMeta(type):
    @staticmethod
    def make_custom_class_dict(class_dict, class_name):
        new_class_dict = {}

        for key, value in class_dict.items():
            if key[-2:] == "__" and key[:2] == "__":
                new_class_dict[key] = value

            elif key[0] == "_":
                parts = key.split("__")
                if len(parts) == 2 and parts[0][1:] == class_name:
                    new_key = parts[0] + "__custom_" + parts[1]
                else:
                    new_key = "_custom_" + key[1:]
                new_class_dict[new_key] = value

            else:
                new_class_dict["custom_" + key] = value
        return new_class_dict

    @staticmethod
    def create_custom_setattr(default_setattr):
        def custom_setattr(self, key, value):
            default_setattr(self, "custom_" + key, value)

        return custom_setattr

    def __new__(mcs, name, bases, class_dict, **kwargs):
        custom_class_dict = CustomMeta.make_custom_class_dict(class_dict, name)
        cls = super().__new__(mcs, name, bases, custom_class_dict, **kwargs)
        if len(bases) == 0 or "__setattr__" in class_dict:
            setattr(
                cls,
                "__setattr__",
                CustomMeta.create_custom_setattr(cls.__setattr__)
            )
        return cls
