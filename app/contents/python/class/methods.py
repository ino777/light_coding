class Person(object):
    i = 100

    def __init__(self, name):
        self.name = name
    
    # インスタンスメソッド
    def say(self):
        print(self.name)
    
    # 静的メソッド
    @staticmethod
    def greet():
        print('Hello')
    
    # クラスメソッド
    @classmethod
    def show_i(cls):
        print(cls.i)


Person.greet()
Person.show_i()

p = Person('Mike')
p.say()