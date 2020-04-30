i = 0
while i < 3:
    print(i **2)
    i += 1
else:
    print('Done.')



num = 5
while(True):
    print('{}...'.format(num))
    num -= 1
    if (num == 0):
        print('boom!')
        break