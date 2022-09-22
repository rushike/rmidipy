from rmidiv1.math import functions


def fibonacci(start, end = None, step = 1):
    start, end = start, end if end else 0, start
    i = start
    res = [0, 0]
    for j in range(2):
        res[j] = functions.fibonacci(i)
        yield res[j]
        i += 1
    while i < end:
        res[0], res[1] = res[1],  res[0] + res[1]
        yield res[1]
        i += 1

def serial(start, end = None, step = 1):
    start, end = (start, end) if end else (0, start)
    i = start
    while i < end:
        yield i
        i += 1
