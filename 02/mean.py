import time
import functools


def mean(k_calls: int = 0) -> callable:
    def inner_mean(func: callable) -> callable:
        calls_times: list[float] = [0] * k_calls
        num_calls: int = 0

        @functools.wraps(func)
        def inner(*args, **kwargs):
            start_ts = time.time()
            res = func(*args, **kwargs)
            end_ts = time.time()
            exec_time = end_ts - start_ts

            nonlocal calls_times, num_calls
            calls_times[num_calls % k_calls] = exec_time
            num_calls += 1

            mean_exec = sum(calls_times) / min(num_calls, k_calls)
            print(f"Mean execution time = {mean_exec}")

            return res

        return inner

    return inner_mean
