class Person(object):
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
        print('Set "{}" as name'.format(new_name))
    
    @name.deleter
    def name(self):
        del self._name
        print('Name is deleted')


p = Person('Mike')
print(p.name)

p.name = 'Tim'
print(p.name)

del p.name