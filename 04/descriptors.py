class Probability:
    def __set_name__(self, owner, name):
        self.name = f"_prob_descr_{name}"

    def __get__(self, obj, obj_type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, (float, int)):
            raise ValueError("Int or float required")

        if not 0 <= val <= 1:
            raise ValueError("Probability must be in [0; 1]")

        return setattr(obj, self.name, val)


class LatexInLineMathEquation:
    def __set_name__(self, owner, name):
        self.name = f"_LatexInLineMathEquation_descr_{name}"

    def __get__(self, obj, obj_type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise ValueError("Value must be str")

        if len(val) <= 2 or val[0] != "$" \
                or val[-1] != "$" \
                or val.count("$") > 2:
            raise ValueError("Incorrect inline math equation")

        if not LatexInLineMathEquation.is_brackets_closed(val, {"{": "}"}):
            raise ValueError("{} brackets not closed")

        return setattr(obj, self.name, val)

    @staticmethod
    def is_brackets_closed(string, brackets):
        brackets_queue = []
        for symb in string:
            if symb in brackets:
                brackets_queue.append(brackets[symb])
            elif len(brackets_queue) != 0 and symb in brackets_queue[-1]:
                brackets_queue.pop()
        return len(brackets_queue) == 0


class FootballMatchScore:
    def __set_name__(self, owner, name):
        self.name = f"_FootballMatchScore_desc_{name}"

    def __get__(self, obj, obj_type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, (list, tuple, dict)):
            raise ValueError("List, tuple or dict is required")

        if not len(val) == 2:
            raise ValueError("Length of value must be equals 2")

        scores = val.values() if isinstance(val, dict) else val

        if not all(isinstance(score, int) and score >= 0 for score in scores):
            raise ValueError("Scores must be natural")

        return setattr(obj, self.name, list(scores))
