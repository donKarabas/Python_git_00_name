
# GUI, пример message = StringVar, METANIT.COM

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

message = StringVar()

label = ttk.Label(textvariable=message)     # строка над вводом
label.pack(anchor=NW, padx=6, pady=6)

entry = ttk.Entry(textvariable=message)     # Поле для ввода
entry.pack(anchor=NW, padx=6, pady=6)

button = ttk.Button(textvariable=message)           # Кнопка
button.pack(side=LEFT, anchor=N, padx=6, pady=6)

root.mainloop()

#------------------------------------------------
# События Enter и пробел в работе с однострочным текстовым полем
# https://dzen.ru/a/Xt5wuLkz1xX6BfhA?experiment=919795

from tkinter import *

root = Tk()
root.title('My first GUI')
root.geometry('350x250')

def get(event):     # Срабатывает, когда нажимаем Enter
    a = en_1.get()  # Записываем введённый текст в переменную "а"
    print(a)

def insert(event):      # Срабатывает, когда нажимаем пробел
    en_1.insert(0, ' World ')   # Вставляет текст в текстовое поле

en_1 = Entry(font='Hack 12')
en_1.bind('<Return>', get)      # Обработчик событий нажатия Enter
en_1.bind('<space>', insert)    # Обработчик событий нажатия пробел
en_1.pack()
root.mainloop()

#---
# Код событий Enter и пробел, оформленный в класс

from tkinter import *

class MyFirstGui:
    def __init__(self):
        self.root = Tk()
        self.root.title('My first GUI')
        self.root.geometry('350x250')

        self.en_1 = Entry(font='Hack 12')
        self.en_1.pack()

        self.get_event = None       # Без этих двух строчек код
        self.insert_event = None    # тоже работает нормально

        self.root.bind('<Return>', self.get)
        self.root.bind('<space>', self.insert)

    def get(self, event):
        a = self.en_1.get()
        print(a)

    def insert(self, event):
        self.en_1.insert(0, ' World ')


if __name__ == '__main__':
    my_first_gui = MyFirstGui()
    my_first_gui.root.mainloop()

#------------------------------------------
# Автоматическое обновление функции методом after()
# https://issues.su/obnovit-okno-tkinter-v-python/

from tkinter import *

def update_window():
    label.config(text="Новый текст")
    root.after(5000, update_window)  # Обновление каждые 5 секунд

root = Tk()
label = Label(root, text="Исходный текст")
label.pack()

root.after(5000, update_window)  # Запуск первого обновления

root.mainloop()

#---
# Более верный код для запуска автоматического обновления, где tk.after()
# переменная, а не повторяющаяся функция.
# https://stackoverflow.com/questions/25702094/tkinter-after-cancel-in-python

from tkinter import *

root = Tk()
def update_window():
    label.config(text="Новый текст")
    print('обновление')
    up_text = root.after(2000, update_window)   # Обновление каждые 5 секунд

up_text = root.after(2000, update_window)   # Запуск первого обновления

label = Label(root, text="Исходный текст")
label.pack()

root.mainloop()

#---
# Старт и остановка методом after_cancel() безконечного цикла
# автоматического обновления. Код оформлен в class Update:

from tkinter import *

class Update:
    def __init__(self):
        self.root = Tk()
        self.label = Label(self.root, text="Исходный текст")
        self.label.pack()

        self.start_button = Button(self.root, text="Начать обновление", command=self.update_window)
        self.start_button.pack()

        self.stop_button = Button(self.root, text="Остановить обновление", command=self.stop_update)
        self.stop_button.pack()

    def update_window(self):
        self.label.config(text="Новый текст")
        self.up_text = self.root.after(2000, self.update_window)  # Обновление каждые 2 секунды
        print('start')

    def stop_update(self):
        self.root.after_cancel(self.up_text)  # Остановка обновлений
        print('stop')


if __name__ == '__main__':
    myupdate = Update()
    myupdate.root.mainloop()

#---
# События bind. Левая кнопка мыши (<Button-1>)
# https://stackoverflow.com/questions/25702094/tkinter-after-cancel-in-python

from tkinter import *
import random

tk = Tk()
canvas = Canvas(tk, width=1920, height=1080, background="grey")
canvas.pack()

def xy(event):
    xm, ym = event.x, event.y

def task():
    w=random.randint(1,1000)
    h=random.randint(1,1000)
    canvas.create_rectangle(w,h,w+150,h+150)
    def callback(event):
        if True:
            print("clicked2")
            # 'solve' is used here to stop the after... methods.
            tk.after_cancel(solve)
    canvas.bind("<Button-1>",callback)   # <Button-1> - клик левой кнопкой мыши
    solve = tk.after(1000, task)
# above and below tk.after is set to 'solve' a variable.
solve = tk.after(1000, task)

tk.mainloop()

#------------------------------------------
# Модуль datetime. Автоматическое определение дня недели.
# https://pythonworld.ru/moduli/modul-datetime.html
# https://pythonru.com/primery/kak-ispolzovat-modul-datetime-v-python

import datetime
class WorkMonth:
    __MS = ['Январь', 'Февраль', 'Март', 'Апрель',
                'Май', 'Июнь', 'Июль', 'Август',
                'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    __WS = ['пн', 'вт', 'ср', 'чт',
                'пт', 'сб', 'вс']

    def __init__(self):
        self.data_method()

    def data_method(self):
        d_c = int(input('Введите число: '))
        monts_choice = input('Введите месяц: ')
        year_choice = int(input('Введите год: '))

        date1 = datetime.datetime(year_choice, self.__MS.index(monts_choice) + 1, d_c)
        date = datetime.date.today()
        ind = (date1.weekday())
        dayweek = self.__WS[ind]

        print(date)     # сегодняшняя - (2024-02-27)
        print(date1)    # введённая - 2024-01-29 00:00:00
        print(ind)      # индекс дня недели (0-6) - 0
        print(dayweek)  # день недели - пн


day1 = WorkMonth()

# Введите число: 29
# Введите месяц: Январь
# Введите год: 2024
