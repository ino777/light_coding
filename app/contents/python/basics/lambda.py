square = lambda x: x**2
print(square)
print(square(3))


members = [('Mike', 22), ('Nancy', 19), ('Tim', 25)]
members.sort(key=lambda member: member[1])
print(members)