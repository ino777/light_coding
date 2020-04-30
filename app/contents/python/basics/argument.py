def say(name, age=25, live_in='Osaka'):
    print(name, age, live_in)

say('Mike', 22, 'Tokyo')
say(name='Mike', age=22, live_in='Tokyo')
say('Nancy')



def add_numbers(*args):
    total = 0
    for i in args:
        total += i
    return total


print(add_numbers(1, 2, 3, 4, 5))
numbers = (1, 2, 3, 4, 5)
print(add_numbers(*numbers))