fibonacci = [1, 1, 2, 3, 5, 8, 13]
print(fibonacci[0])
print(fibonacci[:4])

fibonacci += [21, 34, 55, 89, 144]
print(fibonacci)

x = [['a', 'b', 'c'], [1, 2, 3]]
print(x, x[0][2])
x[1] = ['d', 'e']
print(x)
print('\n')


stack = [10, 20 ,30]
stack.append(40)
print('stack=', stack)
stack.pop()
stack.pop()
print('stack=', stack)