from time import time


def calculate_time(func):
    def wrapper(*args, **kwargs):
        t = time()
        returned_value = func(*args, **kwargs)
        print(f'time spent in {func.__name__}: {time() - t}s')
        return returned_value

    return wrapper
