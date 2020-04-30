def power_func(a):
    def power(n):
        return a**n
    return power

p = power_func(2)
print(p(1))     # 2**1
print(p(2))     # 2**2
print(p(3))     # 2**3