def add_num(n, m):
    """ Add two numbers """
    return n + m

print(add_num)
print(add_num.__doc__)
print(add_num(1, 2))


def swap(a, b):
    return b, a

print(swap(1, 2))