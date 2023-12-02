import io
import time
import pstats
import cProfile
import functools

from typing import Callable


def profile_deco(function: Callable):
    pr = cProfile.Profile()

    @functools.wraps(function)
    def inner(*args, **kwargs):
        pr.enable()
        result = function(*args, **kwargs)
        pr.disable()
        return result

    def print_stat():
        s = io.StringIO()
        sort_by = "cumulative"
        pstats.Stats(pr, stream=s).sort_stats(sort_by).print_stats()
        print(s.getvalue())

    setattr(inner, "print_stat", print_stat)
    return inner


if __name__ == "__main__":

    @profile_deco
    def add(a, b):
        time.sleep(1)
        return a + b

    @profile_deco
    def sub(a, b):
        time.sleep(0.5)
        time.sleep(0.125)
        return a - b

    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
