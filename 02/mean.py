import time
import functools


def mean(calls_to_rem: int = 1) -> callable:

    if not isinstance(calls_to_rem, int) or calls_to_rem <= 0:
        raise ValueError("calls_to_rem must be int and over 0")

    def inner_mean(func: callable) -> callable:
        calls_times: list[float] = [0] * calls_to_rem
        num_calls: int = 0

        @functools.wraps(func)
        def inner(*args, **kwargs):
            start_ts = time.time()
            res = func(*args, **kwargs)
            end_ts = time.time()
            exec_time = end_ts - start_ts

            nonlocal calls_times, num_calls
            calls_times[num_calls % calls_to_rem] = exec_time
            num_calls += 1

            mean_exec = sum(calls_times) / min(num_calls, calls_to_rem)
            print(
                f"Mean execution time = {mean_exec} "
                f"of last {min(num_calls, calls_to_rem)} calls"
            )

            return res

        return inner

    return inner_mean
