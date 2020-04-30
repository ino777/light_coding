t = ('a', 'b', 'c')
print(t[1])
t[0] = 'A'      # <-- Error!

t += ('d', 'e')
print(t)

empty = ()
single = 10,
print('empty= {}, single= {}'.format(empty, single))

nest = ([7, 7, 'a'], 50.0, 'DDDD')
print(nest)
print('\n')


num_tuple = (10, 20)
x, y = num_tuple
print('x= {}, y= {}'.format(x, y))
z, w = 'A', 'B'
z, w = w, z
print('z= {}, w= {}'.format(z, w))