import cProfile
from time import time

from memory_profiler import profile

from classes import *


N: int = 100_000


@profile
def comparison(attrs_class, val=Value(), n: int = N):
    start_time = time()
    insts = [attrs_class(val, val) for _ in range(n)]
    end_time = time()
    mean_create_time = (end_time - start_time)

    start_time = time()
    for inst in insts:
        a, b = inst.attr1, inst.attr2
    end_time = time()
    mean_read_time = (end_time - start_time)

    start_time = time()
    for inst in insts:
        inst.attr1 = val
        inst.attr2 = val
    end_time = time()
    mean_edit_time = (end_time - start_time)

    return f"{attrs_class.__name__} - {mean_create_time} " \
           f" read - {mean_read_time}" \
           f" write - {mean_edit_time}"


def main():
    results = []
    classes = [DefaultAttrs, SlotsAttrs, WeakrefAttr]
    for class_ in classes:
        results.append(comparison(class_))
    print(*results, sep="\n")


if __name__ == "__main__":
    cProfile.run("main()")
