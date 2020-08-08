class Person(object):
    def __init__(self, name, lang):
        self.name = name
        self.lang = lang
    
    def greet(self):
        print('Hello')


class Japanese(Person):
    def __init__(self, name, lang='Japanese'):
        super().__init__(name, lang)
    
    def greet(self):
        print(self.name, '"Konnichiwa"')


class British(Person):
    def __init__(self, name, lang='English'):
        super().__init__(name, lang)
    
    def greet(self):
        print(self.name, '"Hello"')


japanese = Japanese('Taro')
japanese.greet()

british = British('George')
british.greet()