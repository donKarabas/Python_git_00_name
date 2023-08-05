
# https://habr.com/ru/articles/137415/; Пользовательские атрибуты в Python.


# __dict__

class StuffHolder:
    stuff = 'class stuff'

a = StuffHolder()
b = StuffHolder()

print(a.stuff)      # class stuff
print(b.stuff)      # class stuff

b.b_stuff = 'b stuff'

print(b.b_stuff)    # b stuff
print(a.b_stuff)
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/python_git_00.py", line 19, in <module>
#     print(a.b_stuff)
# AttributeError: 'StuffHolder' object has no attribute 'b_stuff'

print(StuffHolder.__dict__)
# {... 'stuff': 'class stuff', ...}
# {'__module__': '__main__', 'stuff': 'class stuff', '__dict__': <attribute '__dict__' of 'StuffHolder' objects>,
# '__weakref__': <attribute '__weakref__' of 'StuffHolder' objects>, '__doc__': None}

print(a.__dict__)       # {}
print(b.__dict__)       # {'b_stuff': 'b stuff'}

print(a.__class__)      # <class '__main__.StuffHolder'>
print(b.__class__)      # <class '__main__.StuffHolder'>

print(a.new_stuff)
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test04.py", line 10, in <module>
#     print(a.new_stuff)
# AttributeError: 'StuffHolder' object has no attribute 'new_stuff'

print(b.new_stuff)
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test04.py", line 10, in <module>
#     print(b.new_stuff)
# AttributeError: 'StuffHolder' object has no attribute 'new_stuff'

StuffHolder.new_stuff = 'new'

print(StuffHolder.__dict__)
# {... 'stuff': 'class stuff', 'new_stuff': 'new', ...}
# {'__module__': '__main__', 'stuff': 'class stuff', '__dict__': <attribute '__dict__' of 'StuffHolder' objects>,
# '__weakref__': <attribute '__weakref__' of 'StuffHolder' objects>, '__doc__': None, 'new_stuff': 'new'}

print(a.new_stuff)  # new
print(b.new_stuff)  # new

c = StuffHolder()
print(c.__dict__)   # {}

c.stuff = 'more c stuff'
print(c.__dict__)   # {'stuff': 'more c stuff'}
print(StuffHolder.__dict__)     # {... 'stuff': 'more stuff', 'new_stuff': 'new', ...}

d = StuffHolder()
print(d.stuff)  # class stuff

d.stuff = 'd stuff'
print(d.stuff)      # d stuff

#-------------------------------------------------------------------
# Дескрипторы.

class FuncHolder:
    def func(self):
        pass

fh = FuncHolder()
print(FuncHolder.func)  # <function FuncHolder.func at 0x7f26df240ca0>
print(FuncHolder.__dict__)
# {... 'func': <function FuncHolder.func at 0x7fe8568fdca0>, ...}
# {'__module__': '__main__', 'func': <function FuncHolder.func at 0x7fe8568fdca0>,
# '__dict__': <attribute '__dict__' of 'FuncHolder' objects>,
# '__weakref__': <attribute '__weakref__' of 'FuncHolder' objects>, '__doc__': None}

print(fh.func)  # <bound method FuncHolder.func of <__main__.FuncHolder object at 0x7f62c7f66dc0>>

print(FuncHolder.func.__class__.__get__)    # <slot wrapper '__get__' of 'function' objects>

# descr.__get__(self, obj, type=None) --> value
# - переопределяет способ получения значения атрибута)
# descr.__set__(self, obj, value) --> None
# - переопределяет способ присваивания значения атрибуту)
# descr.__delete__(self, obj) --> None
# - переопределяет способ удаления атрибута)

#--------------------------------------------------------------

# Дескрипторы данных - Data Descriptor
# - объект, который реализует метод __get__() и __set__()

class DataDesc:
    def __get__(self, obj, cls):
        print('Trying to access from {0} class {1}'.format(obj, cls))

    def __set__(self, obj, val):
        print('Trying to set {0} for {1}'.format(val, obj))

    def __delete__(self, obj):
        print('Trying to delete from {0}'.format(obj))

class DataHolder:
    data = DataDesc()

d = DataHolder()

print(DataHolder.data)
# Trying to access from None class <class '__main__.DataHolder'>
# None

print(d.data)
# Trying to access from <__main__.DataHolder object at 0x7f4fa970ffd0> class <class '__main__.DataHolder'>
# None
d.data
# Trying to access from <__main__.DataHolder object at 0x7fb8bf2d8fd0> class <class '__main__.DataHolder'>

d.data = 1  # Trying to set 1 for <__main__.DataHolder object at 0x7f457e317fd0>
del d.data  # Trying to delete from <__main__.DataHolder object at 0x7f5d7e6c8fd0>

d.__dict__['data'] = 'override!'

print(d.__dict__)   # {'data': 'override!'}
d.data
# Trying to access from <__main__.DataHolder object at 0x7fb4434a4fd0> class <class '__main__.DataHolder'>

print(DataHolder.__dict__)  # {... 'data': <__main__.DataDesc object at 0x7f3a275efdc0>, ...}
DataHolder.data = 'kick descriptor out'
print(DataHolder.__dict__)  # {... 'data': 'kick descriptor out', ...}
print(DataHolder.data)  # kick descriptor out

#-------------------------------------------------------------------------

# Дескрипторы не данных - Non-Data Descriptor
# - объект, который реализует метод __get__()

class NonDataDesc:
    def __get__(self, obj, cls):
        print('Trying to access from {0} class {1}'.format(obj, cls))

class NonDataHolder:
    non_data = NonDataDesc()

n = NonDataHolder()

NonDataHolder.non_data
# Trying to access from None class <class '__main__.NonDataHolder'>

n.non_data
# Trying to access from <__main__.NonDataHolder object at 0x7faf11b0dfd0> class <class '__main__.NonDataHolder'>

n.non_data = 1
print(n.non_data)   # 1
print(n.__dict__)   # {'non_data': 1}

#---
# Создать свойство просто с помощью дескриптора.

class Descriptor:
    def __get__(self, obj, type):
        print('getter used')

    def __set__(self, obj, val):
        print('setter used')

    def __delete__(self, obj):
        print('deleter used')


class MyClass:
    prop = Descriptor()

#---
# Или воспользоваться встроенным классом property,
# он представляет собой дескриптор данных.

class MyClass:

    def _getter(self):
        print("getter used")
    def _setter(self, val):
        print("setter used")
    def _deleter(self):
        print("deleter used")

    prop = property(_getter, _setter, _deleter, "doc string")


m = MyClass()

m.prop          # getter used
m.prop = 1      # setter used
del m.prop      # deleter used

#---
# Дескриптор данных property без каких-либо функций

class MySecondClass:
    prop = property()

m2 = MySecondClass()

m2.prop     # AttributeError: unreadable attribute
m2.prop = 1   # AttributeError: can't set attribute
del m2      # (AttributeError: can't delete attribute)??

#---
# Дескрипторы classmethod, staticmethod

class StaticAndClassMethodHolder:

    def _method(*args):
        print('_method called with ', args)

    static = staticmethod(_method)
    cls = classmethod(_method)

s = StaticAndClassMethodHolder()

s._method()
# _method called with (<__main__.StaticAndClassMethodHolder object at 0x7f41d7f91e20>,)

s.static()  # _method called with ()
s.cls()
# _method called with (<class '__main__.StaticAndClassMethodHolder'>,)

#---------------------------------------------------------------------------

# Методы __getattr__(), __setattr__(), __delattr__() и __getattribute__()

# __getattr__(self, name) будет вызван в случае, если запрашиваемый атрибут не
# найден обычным механизмом (в __dict__ экземпляра, класса и т.д.)

class SmartyPants:
    def __getattr__(self, attr):
        print('Yep, I know', attr)
    tellme = 'It`s a secret'

smarty = SmartyPants()
smarty.name = 'Smartinius Smart'

smarty.quicksort    # Yep, I know quicksort
smarty.python       # Yep, I know python
print(smarty.tellme)    # It`s a secret
print(smarty.name)      # Smartinius Smart

#---
# Следует иметь в виду, что вызов специальных методов (например __len__(), __str__()) через встроенные
# функции или неявный вызов через синтаксис языка осуществляется в обход __getattribute__()

class Optimist:
    attr = 'class attribute'

    def __getattribute__(self, name):
        print('{0} is great!'.format(name))

    def __len__(self):
        print('__len__ is special')
        return 0

o = Optimist()
o.instance_attr = 'instance'

o.attr          # attr is great!
o.dark_beer     # dark_beer is great!
o.instance_attr # instance_attr is great!
o.__len__       # __len__ is great!
len(o)          # __len__ is special (__len__ is special\n 0)??

#---
# __setattr__(self, name, value) будет вызван при попытке установить значение атрибута экземпляра.

class NoSetters:
    attr = 'class attribute'
    def __setattr__(self, name, val):
        print('not setting {0}={1}'.format(name, val))

no_setters = NoSetters()

no_setters.a = 1            # not setting a=1
no_setters.attr = 1         # not setting attr=1
print(no_setters.__dict__)  # {}
print(no_setters.attr)      # class attribute
no_setters.a    # AttributeError: 'NoSetters' object has no attribute 'a'

#---
# При переопределении __getattribute__(), __setattr__(), и __delattr__() следует иметь в виду, что
# стандартный способ получения доступа к атрибутам можно вызвать через object

class GentleGuy:
    def __getattribute__(self, name):
        if name.endswith('_please'):
            return object.__getattribute__(self, name.replace('_please', ''))
        raise AttributeError('And the magic word!?')

gentle = GentleGuy()
gentle.coffee = 'some coffee'

gentle.coffee   # AttributeError: And the magic word!?
print(gentle.coffee_please) # some coffee

# ----------------------------------------------------------------------------------

# __slots__
# # Наличие __slots__ ограничивает возможные имена атрибутов объекта теми, которые там указаны,
# # и снимает необходимость создавать __dict__ экземпляра.

class Slotter:
    __slots__ = ['a', 'b']

s = Slotter()

print(s.__dict__)   # AttributeError: 'Slotter' object has no attribute '__dict__'
s.c = 1     # AttributeError: 'Slotter' object has no attribute 'c'
s.a = 1
s.b = 1
print(s.a, ';', s.b)    # 1 ; 1
print(dir(s))   # [..., 'a', 'b']
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__',
# '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__',
# '__str__', '__subclasshook__', 'a', 'b']