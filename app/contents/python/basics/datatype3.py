d = {
    'x': 100,
    'y': 500
}

print(d['x'])
print(d['z'])   #<-- Error!

d['y'] = 999
print(d)

print('keys:', d.keys())