import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        return 'Args: {0}, Result: {1}, Time: {2}'.format(args, result, elapsed)
    return wrapper

@measure_time
def test(n):
    total = 0
    for i in range(n):
        total += i
    return total

print(test(1000))
print(test(10000))