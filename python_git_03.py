
# selfedu; 12 магический метод __call__
# логика работы метода

class Counter:
    def __init__(self):
        self.__counter = 0

    def __call__(self, step=1, *args, **kwargs):
        print('__call__')
        self.__counter += step
        return self.__counter


c = Counter()
c2 = Counter()
c()
c(2)
res = c(10)
res2 = c2(-5)
print(res, res2)
# out:
# __call__
# __call__
# __call__
# __call__
# 13 -5

# ---
# Замыкание функции с помощью класса с магическим
# методом __call__

class StripChars:
    def __init__(self, chars):
        self.__counter = 0
        self.__chars = chars

    def __call__(self, *args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError('Аргумент должен быть строкой')

        return args[0].strip(self.__chars)


s1 = StripChars('?:!.; ')
s2 = StripChars(' ')
res = s1(' Hello World! ')
s2(' Hello World! ')
res2 = s2(' МегаПрогер! ')
print(res, res2, sep='\n')
# out:
# Hello World
# МегаПрогер!

#---
# Декорация с помощью классов.

import math

class Derivate:
    def __init__(self, func):
        self.__fn = func

    def __call__(self, x, dx=0.0001, *args, **kwargs):
        return (self.__fn(x + dx) - self.__fn(x)) / dx


@Derivate       # = df_sin = Derivate(df_sin)
def df_sin(x):
    return math.sin(x)

#df_sin = Derivate(df_sin)
print(df_sin(math.pi/3))      # 0.49995669789693054

# 'Навык алгоритмизации вырабатывается на решении практических задач.'

# ---------------------------------------------------------------------------------

# selfedu; 28. Введение в обработку исключений
# Блоки try / except

try:
    x, y = map(int, input().split())
    res = x / y
except ValueError:
    print('Ошибка типа данных')
except ZeroDivisionError:
    print('Деление на ноль')

print('Штатное завершение.')
# out:
# Вводим: 1 0
# Деление на ноль
# Штатное завершение.

#---

try:
    x, y = map(int, input().split())
    res = x / y
except (ValueError, ZeroDivisionError):
    print('Ошибка типа данных')

print('Штатное завершение.')

#---

try:
    x, y = map(int, input().split())
    res = x / y
except:
    print('Ошибка')

print('Штатное завершение.')

#-----------------------------------------------------------------

# selfedu; 29. Обработка исключений.
# Блоки finally и else.

try:
    x, y = map(int, input().split())
    res = x / y
except ZeroDivisionError as z:
    print(z)
except ValueError as z:
    print(z)
# out:
# Ввод: a b
# invalid literal for int() with base 10: 'a'
# Ввод: 1 0
# division by zero

#---
# else
try:
    x, y = map(int, input().split())
    res = x / y
except ZeroDivisionError as z:
    print(z)
except ValueError as z:
    print(z)
else:
    print('Исключений не произошло.')
# out:
# Ввод: 1 2
# Исключений не произошло.
# Ввод: a b
# invalid literal for int() with base 10: 'a'

#---
# finally
try:
    x, y = map(int, input().split())
    res = x / y
except ZeroDivisionError as z:
    print(z)
except ValueError as z:
    print(z)
finally:
    print('Блок finally выполняется всегда.')
# Out:
# Ввод: 1 2
# Блок finally выполняется всегда.
# Ввод: a b
# invalid literal for int() with base 10: 'a'
# Блок finally выполняется всегда.

#--
# Пример finally
try:
    f = open('strings.txt')
    f.write('hello')    # Инструкция записи для файла, открытого для чтения.
except FileNotFoundError as z:
    print(z)
except:
    print('Другая ошибка')
finally:
    print('Блок finally выполняется всегда.')
# Out:
# Другая ошибка
# Блок finally выполняется всегда.

#---

try:
    f = open('strings.txt')
    f.write('hello')
except FileNotFoundError as z:
    print(z)
except:
    print('Другая ошибка')
finally:
    if f:
        f.close()
        print('Файл закрыт')
# Out:
# Другая ошибка
# Файл закрыт

#---

try:
    with open('strings.txt') as f:  # Закрывает файл автоматически
        f.write('hello')
except FileNotFoundError as z:
    print(z)
except:
    print('другая ошибка')
# Другая ошибка

#---

def get_values():
    try:
        x, y = map(int, input().split())
        return x, y
    except ValueError as z:
        print(z)
        return 0, 0
    finally:
        print('finally выполняется до return')

x, y = get_values()
print(x, y)
# Out:
# Ввод: 1 2
# finally выполняется до return
# 1 2
# Ввод: a b
# invalid literal for int() with base 10: 'a'
# finally выполняется до return
# 0 0

#---

try:        # Блок try и блоке try
    x, y = map(int, input().split())
    try:
        res = x / y
    except ZeroDivisionError:
        print('деление на ноль')
except ValueError as z:
    print(z)
# a b   -   (отрабатывает внешний блок)
# invalid literal for int() with base 10: 'a'
# 1 0   -   (отрабатывает внутренний блок)
# деление на ноль

#---

def div(a, b):  # Вынос блока try в функцию
    try:
        return a / b
    except ZeroDivisionError:
        return 'деление на ноль'

res = 0
try:
    x, y = map(int, input().split())
    res = div(x, y)
except ValueError as z:
    print(z)

print(res)
# ввод: 1 2
# 0.5
# ввод: a b
# invalid literal for int() with base 10: 'a'
# 0
# ввод: a b     (вызывается блок try из функции div)
# деление на ноль

#---------------------------------------------------------
# selfedu; 30. Распространение исключений.
# (propagation exceptions)

def func2():
    return 1 / 0

def func1():
    return func2()

print('Я к вам пишу - чего же боле?')
print('Что я могу ещё сказать?')
print('Теперь, я знаю, в вашей воле')
func1()
print('Меня презреньем наказать.')
print('Но вы, к моей несчастной доле')
print('Хоть каплю жалости храня,')
print('Вы не оставите меня.')
# out:
# Я к вам пишу - чего же боле?
# Что я могу ещё сказать?
# Теперь, я знаю, в вашей воле
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 11, in <module>
#     func1()
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 6, in func1
#     return func2()
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 3, in func2
#     return 1 / 0
# ZeroDivisionError: division by zero

#---
# Обрабатывать исключения можно на любом уровне.

def func2():
    return 1 / 0

def func1():
    return func2()

print('Я к вам пишу - чего же боле?')
print('Что я могу ещё сказать?')
print('Теперь, я знаю, в вашей воле')
try:
    func1()
except:
    print('func1 error')
print('Меня презреньем наказать.')
print('Но вы, к моей несчастной доле')
print('Хоть каплю жалости храня,')
print('Вы не оставите меня.')
# out:
# Я к вам пишу - чего же боле?
# Что я могу ещё сказать?
# Теперь, я знаю, в вашей воле
# func1 error
# Меня презреньем наказать.
# Но вы, к моей несчастной доле
# Хоть каплю жалости храня,
# Вы не оставите меня.

#---

def func2():
    return 1 / 0

def func1():
    try:
        return func2()
    except:
        print('func1 error')

print('Я к вам пишу - чего же боле?')
print('Что я могу ещё сказать?')
print('Теперь, я знаю, в вашей воле')
func1()
print('Меня презреньем наказать.')
print('Но вы, к моей несчастной доле')
print('Хоть каплю жалости храня,')
print('Вы не оставите меня.')
# out:
# Тот же, что выше

#---
# Как только исключение обрабатывается, дальше оно не вызывается.

def func2():
    try:                # Обрабатывается только этот блок.
        return 1 / 0
    except:
        print('func2 error')

def func1():
    try:
        return func2()
    except:
        print('func1 error')

print('Я к вам пишу - чего же боле?')
print('Что я могу ещё сказать?')
print('Теперь, я знаю, в вашей воле')
func1()
print('Меня презреньем наказать.')
print('Но вы, к моей несчастной доле')
print('Хоть каплю жалости храня,')
print('Вы не оставите меня.')
# out
# Я к вам пишу - чего же боле?
# Что я могу ещё сказать?
# Теперь, я знаю, в вашей воле
# func2 error
# Меня презреньем наказать.
# Но вы, к моей несчастной доле
# Хоть каплю жалости храня,
# Вы не оставите меня.

#------------------------------------------------------
# selfedu; 31. Инструкция raise и пользовательские исключения.

print('Куда ты скачешь, гордый конь,')
print('И где опустишь ты копыта?')
print('О мощный властелин судьбы!')
1 / 0
print('Не так ли ты над самой бездной')
print('На высоте, уздой железной')
print('Россию поднял на дыбы?')
# out
# Куда ты скачешь, гордый конь,
# И где опустишь ты копыта?
# О мощный властелин судьбы!
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 5, in <module>
#     1 / 0
# ZeroDivisionError: division by zero

#---

print('Куда ты скачешь, гордый конь,')
print('И где опустишь ты копыта?')
print('О мощный властелин судьбы!')
raise ZeroDivisionError('деление на ноль')
print('Не так ли ты над самой бездной')
print('На высоте, уздой железной')
print('Россию поднял на дыбы?')
# out
# Куда ты скачешь, гордый конь,
# И где опустишь ты копыта?
# О мощный властелин судьбы!
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 5, in <module>
#     raise ZeroDivisionError('деление на ноль')
# ZeroDivisionError: деление на ноль

#---

print('Куда ты скачешь, гордый конь,')
print('И где опустишь ты копыта?')
print('О мощный властелин судьбы!')
e = ZeroDivisionError('деление на ноль')    # ZeroDivisionError - это класс
raise e
print('Не так ли ты над самой бездной')
print('На высоте, уздой железной')
print('Россию поднял на дыбы?')
# out
# Куда ты скачешь, гордый конь,
# И где опустишь ты копыта?
# О мощный властелин судьбы!
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 6, in <module>
#     raise e
# ZeroDivisionError: деление на ноль

#---

print('Куда ты скачешь, гордый конь,')
print('И где опустишь ты копыта?')
print('О мощный властелин судьбы!')
e = ZeroDivisionError('деление на ноль')
raise 'деление на ноль'                     # Будет вызвано другое исключение
print('Не так ли ты над самой бездной')
print('На высоте, уздой железной')
print('Россию поднял на дыбы?')
# out
# Куда ты скачешь, гордый конь,
# И где опустишь ты копыта?
# О мощный властелин судьбы!
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 6, in <module>
#     raise 'деление на ноль'
# TypeError: exceptions must derive from BaseException

#---

print('Куда ты скачешь, гордый конь,')
print('И где опустишь ты копыта?')
print('О мощный властелин судьбы!')
e = ZeroDivisionError('деление на ноль')
[1, 2, 3][4]
print('Не так ли ты над самой бездной')
print('На высоте, уздой железной')
print('Россию поднял на дыбы?')
# out
# Куда ты скачешь, гордый конь,
# И где опустишь ты копыта?
# О мощный властелин судьбы!
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 6, in <module>
#     [1, 2, 3][4]
# IndexError: list index out of range

#---
# Пример создания пользовательских исключений.

class PrintData:
    def print(self, data):
        self.send_data(data)
        print(f'печать: {str(data)}')

    def send_data(self, data):
        if not self.send_to_print(data):
            raise Exception('принтер не отвечает')  # Генерируем исключение с
                                                    # помощью класса Exception
    def send_to_print(self, data):
        return False


p = PrintData()
p.print('123')
# out
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 16, in <module>
#     p.print('123')
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 4, in print
#     self.send_data(data)
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 9, in send_data
#     raise Exception('принтер не отвечает')
# Exception: принтер не отвечает

p = PrintData()
try:                    # Обработка ошибки
    p.print('123')
except Exception:
    print('принтер не отвечает')
# out
#принтер не отвечает

    def send_to_print(self, data):
        return True         # Если данные отправляются успешно
# out
# печать: 123

#---
# Создаём свой класс, своё исключение, с базовым классом Exception

class ExceptionPrintDate(Exception):
    pass


class PrintData:
    def print(self, data):
        self.send_data(data)
        print(f'печать: {str(data)}')

    def send_data(self, data):
        if not self.send_to_print(data):
            raise ExceptionPrintDate('принтер не отвечает')

    def send_to_print(self, data):
        return True


p = PrintData()
try:
    p.print('123')
except ExceptionPrintDate:
    print('принтер не отвечает')
# out
# печать: 123

    def send_to_print(self, data):
        return False                # меняем на False

p = PrintData()
p.print('123')
# out
# Вызывается исключение, созданное в нашем классе ExceptionPrintDate
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 20, in <module>
#     p.print('123')
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 8, in print
#     self.send_data(data)
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 13, in send_data
#     raise ExceptionPrintDate('принтер не отвечает')
# __main__.ExceptionPrintDate: принтер не отвечает

#---
# Расширяем функционал базового класса Exception

class ExceptionPrintDate(Exception):
    """Класс исключения при отправке данных принтеру"""
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f'Ошибка: {self.message}'


class PrintData:
    def print(self, data):
        self.send_data(data)
        print(f'печать: {str(data)}')

    def send_data(self, data):
        if not self.send_to_print(data):
            raise ExceptionPrintDate('принтер не отвечает')

    def send_to_print(self, data):
        return False


p = PrintData()
p.print('123')
# out
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 25, in <module>
#     p.print('123')
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 13, in print
#     self.send_data(data)
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 18, in send_data
#     raise ExceptionPrintDate('принтер не отвечает')
# __main__.ExceptionPrintDate: Ошибка: принтер не отвечает

def send_data(self, data):
    if not self.send_to_print(data):
        raise ExceptionPrintDate
# out
# Traceback (most recent call last):
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 25, in <module>
#     p.print('123')
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 13, in print
#     self.send_data(data)
#   File "/home/lazutchik/PycharmProjects/data_files/test01.py", line 18, in send_data
#     raise ExceptionPrintDate
# __main__.ExceptionPrintDate: Ошибка: None

#---
# Собственная иерархия исключений

class ExceptionPrint(Exception):
    """Общий класс исключения принтера"""


class ExceptionPrintDate(ExceptionPrint):
    """Класс исключения при отправке данных принтеру"""
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f'Ошибка: {self.message}'


class PrintData:
    def print(self, data):
        self.send_data(data)
        print(f'печать: {str(data)}')

    def send_data(self, data):
        if not self.send_to_print(data):
            raise ExceptionPrintDate

    def send_to_print(self, data):
        return False


p = PrintData()
try:
    p.print('123')
except ExceptionPrintDate:
    print('принтер не отвечает')
except ExceptionPrint:
    print('общая ошибка печати')
# out
# принтер не отвечает
