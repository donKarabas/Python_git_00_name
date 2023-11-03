
# Python, Tkinter и SQL: разрабатываем приложение для создания словарей и запоминания
# иностранных слов.
# https://github.com/natkaida/wordmatch/blob/main/word_match.py

# Часть 1. Скрипт для создания пользовательского словаря.
# Создаёт dictionary_my.db

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"dictionary_my.db"
    # описание столбцов словаря - id номер, слово и значение
    sql_create_dictionary_table = """ CREATE TABLE IF NOT EXISTS dictionary (
                                        id integer PRIMARY KEY,
                                        word text,
                                        meaning text
                                    ); """


    # подключение к базе
    conn = create_connection(database)

    # создание таблицы dictionary
    if conn is not None:
        create_table(conn, sql_create_dictionary_table)
    else:
        print("Ошибка: не удалось подключиться к базе.")


if __name__ == '__main__':
    main()


#---
# Часть 2. GUI интерфейс и набор CRUD операций для добавления, редактирования и
# удаления записей в словаре.

from tkinter import ttk
from tkinter import *
import sqlite3


class Dictionary:
    db_name = 'dictionary_my.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Редактирование словаря')

        # создание элементов для ввода слов и значений
        frame = LabelFrame(self.wind, text='Введите новое слово')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frame, text='Слово: ').grid(row=1, column=0)
        self.word = Entry(frame)
        self.word.focus()
        self.word.grid(row=1, column=1)
        Label(frame, text='Значение: ').grid(row=2, column=0)
        self.meaning = Entry(frame)
        self.meaning.grid(row=2, column=1)
        ttk.Button(frame, text='Сохранить', command=self.add_word).grid(row=3, columnspan=2, sticky=W + E)
        self.message = Label(text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
        # таблица слов и значений
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Слово', anchor=CENTER)
        self.tree.heading('#1', text='Значение', anchor=CENTER)

        # кнопки редактирования записей
        ttk.Button(text='Удалить', command=self.delete_word).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='Изменить', command=self.edit_word).grid(row=5, column=1, sticky=W + E)

        # заполнение таблицы
        self.get_words()

    # подключение и запрос к базе
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # заполнение таблицы словами и их значениями
    def get_words(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM dictionary ORDER BY word DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    # валидация ввода
    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0

    # добавление нового слова
    def add_word(self):
        if self.validation():
            query = 'INSERT INTO dictionary VALUES(NULL, ?, ?)'
            parameters = (self.word.get(), self.meaning.get())
            self.run_query(query, parameters)
            self.message['text'] = 'слово {} добавлено в словарь'.format(self.word.get())
            self.word.delete(0, END)
            self.meaning.delete(0, END)
        else:
            self.message['text'] = 'введите слово и значение'
        self.get_words()

    # удаление слова
    def delete_word(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите слово, которое нужно удалить'
            return
        self.message['text'] = ''
        word = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM dictionary WHERE word = ?'
        self.run_query(query, (word,))
        self.message['text'] = 'Слово {} успешно удалено'.format(word)
        self.get_words()

    # рeдактирование слова и/или значения
    def edit_word(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите слово для изменения'
            return
        word = self.tree.item(self.tree.selection())['text']
        old_meaning = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Изменить слово'

        Label(self.edit_wind, text='Прежнее слово:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=word), state='readonly').grid(row=0,
                                                                                                         column=2)

        Label(self.edit_wind, text='Новое слово:').grid(row=1, column=1)
        # предзаполнение поля
        new_word = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=word))
        new_word.grid(row=1, column=2)

        Label(self.edit_wind, text='Прежнее значение:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_meaning), state='readonly').grid(row=2,
                                                                                                                column=2)

        Label(self.edit_wind, text='Новое значение:').grid(row=3, column=1)
        # предзаполнение поля
        new_meaning = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_meaning))
        new_meaning.grid(row=3, column=2)

        Button(self.edit_wind, text='Изменить',
               command=lambda: self.edit_records(new_word.get(), word, new_meaning.get(), old_meaning)).grid(row=4,
                                                                                                             column=2,
                                                                                                             sticky=W)
        self.edit_wind.mainloop()

    # внесение изменений в базу
    def edit_records(self, new_word, word, new_meaning, old_meaning):
        query = 'UPDATE dictionary SET word = ?, meaning = ? WHERE word = ? AND meaning = ?'
        parameters = (new_word, new_meaning, word, old_meaning)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()


if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()


#---
# Часть 3. GUI интерфейс и скрипт для проверки правильности сопоставления иностранных
# слов и значений, выведенных в случайном порядке.

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import random, os
import sqlite3


class Match:
    db_name = 'dictionary_my.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Учим слова')
        self.eng, self.trans = str(), str()
        self.message = Label(text='', fg='red')
        self.message.grid(row=1, column=0, columnspan=2, sticky=W + E)
        # правая и левая колонки
        self.left = Listbox(height=12, exportselection=False, activestyle='none')
        self.left.grid(row=2, column=0)
        self.right = Listbox(height=12, activestyle='none')
        self.right.grid(row=2, column=1)
        self.right.bind("<<ListboxSelect>>", self.callback_right)
        self.left.bind("<<ListboxSelect>>", self.callback_left)
        # назначение команд кнопкам программы и х-кнопке окна
        ttk.Button(text="Начать сначала", command=self.restart_program).grid(row=4, column=1, sticky=W + E)
        ttk.Button(text="Редактировать", command=self.run_edit).grid(row=4, column=0, sticky=W + E)
        self.wind.protocol("WM_DELETE_WINDOW", self.on_exit)
        # заполняем колонки словами
        self.get_words()

    #  закрытие программы по клику на кнопке х
    def on_exit(self):
        if messagebox.askyesno("Выйти", "Закрыть программу?"):
            self.wind.destroy()

    #  подключение к базе и передача запроса
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # запрос на извлечение всех существующих записей из базы в алфавитном порядке
    def get_words(self):
        query = 'SELECT * FROM dictionary ORDER BY word DESC'
        db_rows = self.run_query(query)
        # формирование словаря из перемешанных в случайном порядке слов и их значений
        lst_left, lst_right = [], []
        for row in db_rows:
            lst_left.append(row[1])
            lst_right.append(row[2])
        random.shuffle(lst_left)
        random.shuffle(lst_right)
        dic = dict(zip(lst_left, lst_right))
        # заполнение правой и левой колонок
        for k, v in dic.items():
            self.left.insert(END, k)
            self.right.insert(END, v)

    # обработка клика по словам в левой колонке
    def callback_left(self, event):
        self.message['text'] = ''
        if not event.widget.curselection():
            return
        # извлечение из базы значения выделенного слова
        w = event.widget
        idx = int(w.curselection()[0])
        self.eng = w.get(idx)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            sqlite_select_query = 'SELECT * from dictionary WHERE word = ?'
            cursor.execute(sqlite_select_query, (self.eng,))
            record = cursor.fetchone()
            self.trans = record[2]

    # обработка клика в правой колонке
    def callback_right(self, event1):
        self.message['text'] = ''
        if not event1.widget.curselection():
            return

        w = event1.widget
        idx = int(w.curselection()[0])
        click = w.get(idx)
        # если выбранное слово является правильным переводом, удаляем и оригинал, и значение
        if click == self.trans:
            self.right.delete(ANCHOR)
            self.left.delete(ANCHOR)
        # сообщаем о неверном значении
        else:
            self.message['text'] = 'Неправильно'
            self.right.selection_clear(0, END)

    # загружаем окно и скрипт редактирования словаря
    def run_edit(self):
        os.system('edit_dictionary.py')

    # перезапуск программы
    def restart_program(self):
        self.message['text'] = ''
        self.left.delete(0, END)
        self.right.delete(0, END)
        self.get_words()


if __name__ == '__main__':
    window = Tk()
    window.geometry('250x245+350+200')
    application = Match(window)
    window.mainloop()

