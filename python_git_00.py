
# Бизли, Джонс; книга рецептов; обобщение __init__; стр. 275
#------------------------------
#------------------------------

class Structure:
    # Переменная класса, которая определяет ожидаемые поля
    _fields= []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Устанавливает аргументы
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

# Пример определения класса
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x','y']

    import math
    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2


s = Stock('ACME', 50, 91.1)
print(s)
# <__main__.Stock object at 0x7f965389edc0>
p = Point(2, 3)
print(p)
# <__main__.Point object at 0x7f9653828df0>
c = Circle(4.5)
print(c)
# <__main__.Circle object at 0x7f9653828e20>
print()
s2 = Stock('ACME', 50)
print(s2)

# Вывод
# <__main__.Stock object at 0x7f965389edc0>
# <__main__.Point object at 0x7f9653828df0>
# <__main__.Circle object at 0x7f9653828e20>
#
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test02.py", line 35, in <module>
#     s2 = Stock('ACME', 50)
#   File "/home/lazutchik/PycharmProjects/data_files/test02.py", line 7, in __init__
#     raise TypeError('Expected {} arguments'.format(len(self._fields)))
# TypeError: Expected 3 arguments


# Отображение именованных аргументов, чтобы они соответствовали только
# именам атрибутов, определённым в _fields.
#---

class Structure:
    _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Установка всех позиционных аргументов
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Установка оставшихся именованных аргументов
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # Проверка на оставшиеся любые другие аргументы
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

# Пример использования
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)
    print(f'{s1} - {s2}\n- {s3}')

#Вывод
#<__main__.Stock object at 0x7fefba93adc0> - <__main__.Stock object at 0x7fefba864fd0>
# - <__main__.Stock object at 0x7fefba8c4df0>


# Использование именованных аргументов как средства добавления
# дополнительных атрибутов, не определённых в _fields, к структуре.
#---

class Structure:
    # Переменная класса, которая определяет ожидаемые поля
    _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Установка аргументов
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Установка дополнительных аргументов (если они есть)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
            if kwargs:
                raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))

# Пример использования
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, 91.1, date='8/2/2012')
print(s1, '-', s2)

#Output
# <__main__.Stock object at 0x7f36aae3adc0> - <__main__.Stock object at 0x7f36aad64fd0>

#----------------------------------------------------------------------------------------

# Определение более одного конструктора в классе.
#---

import time

class Date:
    # Основной конструктор
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Альтернативный конструктор
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

    def __str__(self):
        return f'{self.day}.{self.month}.{self.year} г.'

a = Date(2012, 12, 21)  # Первичный
print(a)
b = Date.today()    # Альтернативный
print(b)

# Output
# 21.12.2012 г.
# 25.7.2023 г.


# При определении класса с множественными конструкторами вы должны делать
# функцию __init__() максимально простой - она должна просто присваивать
# атрибутам значения.

import time

class Date:
    def __init__(self, *args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
        self.year, self.month, self.day = args

    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

    def __str__(self):
        return f'{self.day}.{self.month}.{self.year} г.'

a = Date(2012, 12, 21)  # Ясно. Конкретная дата.
b = Date()              # ??? Что тут происходит?

# Class method version
c = Date.today()        # Ясно. Сегодняшняя дата.

print(a, 'Ясно. Конкретная дата.')
print(b, '??? Что тут происходит?')
print(c, 'Ясно. Сегодняшняя дата.')

# Output
# 21.12.2012 г. Ясно. Конкретная дата.
# 26.7.2023 г. ??? Что тут происходит?
# 26.7.2023 г. Ясно. Сегодняшняя дата.


#--------------------------------------------------------------------------------

# __slots__ and __dict__ in python
#---

class Foo(object): __slots__ = ('foo',)
class Bar(object): pass

def get_set_del(obj):
    obj.foo = 'foo'
    obj.foo
    del obj.foo

def test_foo():
    get_set_del(Foo())

def test_bar():
    get_set_del(Bar())

import timeit

print(min(timeit.repeat(test_foo)))
print(min(timeit.repeat(test_bar)))

#Output
# 0.2856877220001479
# 0.3384771319997526

# Использование памяти
#---

class RegularClass: pass
class SlotClass: __slots__ = ('foo', 'bar')

obj = RegularClass()
print(obj.__dict__)
# {}
obj.foo = 5
print(obj.__dict__)
# {'foo': 5}
print()
obj_s = SlotClass()
obj_s.foo = 5
print(obj_s.__slots__)
print(obj_s.__dict__)

# Output
# ('foo', 'bar')
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test04.py", line 13, in <module>
#     print(obj_s.__dict__)
# AttributeError: 'SlotClass' object has no attribute '__dict__'

#---
# Наследование со значениями __slots__ и __dict__

class SlotsClass:
    __slots__ = ('foo', 'bar')

class ChildSlotsClass(SlotsClass):
    pass

obj = ChildSlotsClass()
print(obj.__slots__)
# ('foo', 'bar')
obj.foo = 5
obj.something_new = 3
print(obj.__dict__)
# {'something_new': 3}

#---

class SlotsClass:
    __slots__ = ('foo', 'bar')

class ChildSlotsClass(SlotsClass):
    __slots__ = ('baz',)

obj = ChildSlotsClass()
obj.foo = 5
obj.baz = 6
obj.something_new = 3
print(obj.__dict__)

# Output
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test04.py", line 11, in <module>
#     obj.something_new = 3
# AttributeError: 'ChildSlotsClass' object has no attribute 'something_new'

#---