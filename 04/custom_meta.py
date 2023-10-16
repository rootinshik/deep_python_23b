class CustomMeta(type):
    @staticmethod
    def make_custom_attr_name(attr_name):
        if attr_name.startswith("__") and attr_name.endswith("__"):
            new_attr_name = attr_name
        elif attr_name.startswith("_") and "__" in attr_name:
            new_attr_name = "__custom_".join(attr_name.split("__"))
        elif attr_name.startswith("_"):
            new_attr_name = f"_custom_{attr_name[1:]}"
        else:
            new_attr_name = f"custom_{attr_name}"
        return new_attr_name

    @staticmethod
    def make_custom_class_dict(class_dict):
        new_class_dict = {}
        for key, value in class_dict.items():
            new_class_dict[CustomMeta.make_custom_attr_name(key)] = value
        return new_class_dict

    @staticmethod
    def create_custom_setattr(default_setattr):
        def custom_setattr(self, key, value):
            new_key = CustomMeta.make_custom_attr_name(key)
            default_setattr(self, new_key, value)

        return custom_setattr

    def __new__(mcs, class_name, bases, class_dict, **kwargs):
        class_dict = CustomMeta.make_custom_class_dict(class_dict)
        cls = super().__new__(mcs, class_name, bases, class_dict, **kwargs)

        if len(bases) == 0 or "__setattr__" in class_dict:
            setattr(
                cls,
                "__setattr__",
                CustomMeta.create_custom_setattr(cls.__setattr__)
            )

        return cls
