l = [1, 2, 3]
try:
    l[3] = 4
except IndexError as err:
    print('Error message:', err)
    l = []

print(l)


print('\n')


zero = '0'
if type(zero) is not int:
    raise TypeError("Zero must be int")