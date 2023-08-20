
# Построим несколько домов, добавим в них комнат, а затем выполним сравнения.

from functools import total_ordering

class Room:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(self.name,
                                              self.living_space_footage,
                                              self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage


# Построим несколько домов и добавим в них комнаты
h1 = House('h1', 'Cape')
h1.add_room(Room('Master Bedroom', 14, 21))
h1.add_room(Room('Living Room', 18, 20))
h1.add_room(Room('Kitchen', 12, 16))
h1.add_room(Room('Office', 12, 12))
h2 = House('h2', 'Ranch')
h2.add_room(Room('Master Bedroom', 14, 21))
h2.add_room(Room('Living Room', 18, 20))
h2.add_room(Room('Kitchen', 12, 16))
h3 = House('h3', 'Split')
h3.add_room(Room('Master Bedroom', 14, 21))
h3.add_room(Room('Living Room', 18, 20))
h3.add_room(Room('Office', 12, 16))
h3.add_room(Room('Kitchen', 15, 17))

houses = [h1, h2, h3]

print('Is h1 bigger than h2?', h1 > h2)     # Is h1 bigger than h2? True
print('Is h2 smaller than h3?', h2 < h3)    # Is h2 smaller than h3? True
print('Is h2 greater than or equal to h1?', h2 >= h1)   # Is h2 greater than or equal to h1? False
print('Which one is biggest?', max(houses)) # Which one is biggest? h3: 1101 square foot Split
print('Which is smallest?', min(houses))    # Which is smallest? h2: 846 square foot Ranch

#---
# Методы, созданные @total_ordering
__le__ = lambda self, other: self <  other or self == other
__gt__ = lambda self, other: not (self < other or self == other)
__ge__ = lambda self, other: not (self < other)
__ne__ = lambda self, other: not self == other

#-------------------------------------------------------------------------------
# Мой код. Монеты coin по Геддису. Оформление for, toss, print

import random

class Coin:
    def __init__(self):
        self.__sideup = 'Орёл'

    def toss(self):
        if random.randint(0, 1) == 0:
            self.__sideup = 'Орёл'
        else:
            self.__sideup = 'Решка'

    def get_sideup(self):
        return self.__sideup

coin1 = Coin()
coin2 = Coin()
coin3 = Coin()

print('Вот три монеты, у которых эти стороны обращены вверх:')
print(coin1.get_sideup())
print(coin2.get_sideup())
print(coin3.get_sideup())
print()

print('Подбрасываю все три монеты по 5 раз')
print()
for x in range(5): coin1.toss(), print(coin1.get_sideup())
print()
for x in range(5): coin2.toss(), print(coin2.get_sideup())
print()
for x in range(5): coin3.toss(), print(coin3.get_sideup())

# Вот три монеты, у которых эти стороны обращены вверх:
# Орёл
# Орёл
# Орёл
#
# Подбрасываю все три монеты по 5 раз
#
# Решка
# Орёл
# Решка
# Решка
# Орёл
#
# Орёл
# Решка
# Решка
# Орёл
# Решка
#
# Решка
# Орёл
# Орёл
# Решка
# Решка

# --------------------------------------------------------------

# https://pythonclass.ru/python/klassy-v-python/#init

class Car:
    '''Описание автомобиля'''
    def __init__(self, brand, model, years):
        '''Инициализирует атрибуты'''
        self.brand = brand
        self.model = model
        self.years = years
        self.mileage = 0

    def get_full_name(self):
        '''Автомобиль'''
        name = f'Автомобиль {self.brand} {self.model} {self.years}'
        return name.title()

    def read_mileage(self):
        '''Пробег автомобиля'''
        print(f'Пробег автомобиля {self.mileage} км.')

    def update_mileage(self, new_mileage):
        '''Устанавливает новое значение пробега'''
        self.mileage = new_mileage

    def add_mileage(self, km):
        '''Добавляет пробег'''
        self.mileage += km


car_2 = Car('audi', 'a4', 2019)
print(car_2.get_full_name())    # Автомобиль Audi A4 2019
car_2.read_mileage()            # Пробег автомобиля 0 км.
car_2.update_mileage(17100)
car_2.read_mileage()            # Пробег автомобиля 17100 км.
car_2.add_mileage(14687)
car_2.read_mileage()            # Пробег автомобиля 31787 км.

print()

class ElectricCar(Car):
    '''Описывает электромобиль'''
    def __init__(self, brand, model, years):
        '''Инициализирует атрибуты класса родителя'''
        super().__init__(brand, model, years)
        # атрибут класса-потомка
        self.battery_size = 100

    def battery_power(self):
        '''Выводит мощность аккумулятора авто'''
        print(f'Мощность аккумулятора {self.battery_size} Квт.ч')

# tesla_1 = ElectricCar('tesla', 'model x', 2021)
# print(tesla_1.get_full_name())  # Автомобиль Tesla Model X 2021
# tesla_1.battery_power()  # Мощность аккумулятора 100 Квт.ч

    def get_full_name(self):
        '''Переопределяет метод класса-родителя'''
        # Автомобиль
        name = (f'Автомобиль {self.brand} {self.model} {self.years} '
                f'{self.battery_size}-Квт.ч')
        return name.title()

# При запросе полного названия автомобиля, Python проигнорирует метод
# def get_full_name() в классе-родителе Car и сразу перейдёт к методу
# def get_full_name() в классе ElectricCar.

tesla_1 = ElectricCar('tesla', 'model x', 2021)
print(tesla_1.get_full_name())      # Автомобиль Tesla Model X 2021 100-Квт.Ч

#---------------------------------------------------------
# Класс принмает текст из файла, определяет уникальные слова, считает
# количество повторов каждого уникального слова в тексте, сортирует
# уникальные слова по повторам от бошьшего к меньшему.

class WordCount:
    def __init__(self, FILEIN, FILEOUT):
        self.FILEIN = FILEIN
        self.FILEOUT = FILEOUT

    def set_filein(self, FILEIN):
        self.FILEIN = FILEIN
        text_file = open(FILEIN, 'r')
        text = text_file.read()
        text_file.close()  # Получаем текст из файла
        text = text.rstrip('\n')
        text = text.rstrip('\ufeff')

        self.ls_text = text.split()

        import re

        search = '-'  # Убираем дефис как отдельное слово
        for i in self.ls_text:
            if i == search:
                self.ls_text.remove(i)  # Переводим слова в нижний регистр. Сортируем
        self.ls_text2 = [i.lower() for i in self.ls_text]  # текст по словам.
        self.ls_text2 = [re.sub(r'[.,"?:!;()]', '', i) for i in self.ls_text2]

        self.set_text = {i for i in self.ls_text2}  # Уникальные слова элементами множества.

    def set_fileout(self, FILEOUT):
        import dct_sort
        self.FILEOUT = FILEOUT
        str_stat = f'Всего слов: {len(self.ls_text2)} | Уникальных слов: {len(self.set_text)}'
        str_uniq = '''
        Вот список слов, из которых состоит текст:
        -------------'''
        str_repeat = '''------------
        Вот количество повторов слов по убыванию:
        '''

        dct_repeat = {}
        for let in self.set_text:
            count = 0
            for item in self.ls_text:
                if let == item:  # Создаём словарь повторений
                    count += 1  # Сортируем по убыванию
            dct_repeat[let] = count
        dct_rev = dct_sort.dict_sorted_reverse(dct_repeat)

        word_file = open(FILEOUT, 'w')

        word_file.write(f'{str_stat}\n')
        word_file.write(f'{str_uniq}\n')
        word_file.write(f'{self.set_text}\n')  # Записываем результаты в файл.
        word_file.write(f'{str_repeat}\n')

        for k in dct_rev:
            word_file.write(f'{k} - {dct_rev[k]}\n')

        word_file.close()
        print('Файл записан')


FILEIN = 'strings.txt'
FILEOUT = 'strings_count.txt'

word_count = WordCount(FILEIN, FILEOUT)
word_count.set_filein(FILEIN)
word_count.set_fileout(FILEOUT)

