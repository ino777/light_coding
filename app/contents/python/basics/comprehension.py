squares = [i**2 for i in range(10) if i % 2 == 0]
print('squares:', squares)

muls = tuple(i*j for i in range(1,3) for j in range(1,3))
print('muls', muls)

names = ['Mike', 'Nancy', 'Tim']
ages = [18, 26, 25]
profiles = {name:age for name, age in zip(names, ages)}
print('profiles', profiles)

a = {i for i in range(10)}
print('set a:', a)