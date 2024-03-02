from functools import wraps
from time import perf_counter
from datetime import timedelta


def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(
            f"Время выполнения функции {func.__name__}: {timedelta(seconds=end-start)}"
        )
        return result

    return wrapper


def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        params = args + tuple(kwargs.items())
        result = func(*args, **kwargs)
        if params:
            print(f"Функция была вызвана c параметрами: {params}")
        else:
            print(f"Функция была вызвана без параметров")
        return result

    return wrapper


def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    calls_qty = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal calls_qty
        calls_qty += 1
        if 2 <= calls_qty % 10 <= 4 and (calls_qty % 100 < 12 or calls_qty % 100 > 14):
            print(f"Функция была вызвана {calls_qty} раза")
        else:
            print(f"Функция была вызвана {calls_qty} раз без параметров")

        return func(*args, **kwargs)

    return wrapper


def memo(func):
    """
    Декоратор, запоминающий результаты исполнения функции func
    """
    cache = {}

    @wraps(func)
    def fmemo(*args, **kwargs):
        k = (args, frozenset(kwargs.items()))
        if k not in cache:
            cache[k] = func(*args, **kwargs)
        return cache[k]

    return fmemo


def full_info(func):
    """
    Декоратор, который:
        - выводит время, которое заняло на выполнение функции
        - выводит параметры с которыми была вызвана функция
        - выводит количество вызовов функции
        - запоминает результаты исполнения функции
    """

    calls_qty = 0
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal calls_qty
        calls_qty += 1
        start = perf_counter()
        params = args + tuple(kwargs.items())
        k = (args, frozenset(kwargs.items()))
        if k not in cache:
            cache[k] = func(*args, **kwargs)
        end = perf_counter()
        if 2 <= calls_qty % 10 <= 4 and (calls_qty % 100 < 12 or calls_qty % 100 > 14):
            if params:
                print(
                    f"Функция {func.__name__} была вызвана {calls_qty} раза c параметрами: {params}"
                )
            else:
                print(
                    f"Функция {func.__name__} была вызвана {calls_qty} раза без параметров"
                )
        else:
            if params:
                print(
                    f"Функция {func.__name__} была вызвана {calls_qty} раз c параметрами: {params}"
                )
            else:
                print(
                    f"Функция {func.__name__} была вызвана {calls_qty} раз без параметров"
                )
        print(
            f"Время выполнения функции {func.__name__}: {timedelta(seconds=end-start)}"
        )

        return cache[k]

    return wrapper
