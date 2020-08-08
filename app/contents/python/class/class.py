class Person(object):
    """ Person class """
    i = 100
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say(self):
        print(self.name, self.age)


print(Person.i)
Person.i = 200

# インスタンス化
p = Person('Mike', 25)
p.say()
print(p.i)