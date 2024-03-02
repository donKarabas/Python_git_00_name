
import tkinter as tk
from tkinter import ttk     # модуль расширения, который имеет виджет treeview
import sqlite3      # Импортируем модуль sqlite для создания БД

class Main(tk.Frame):   # Frame - объект библиотеки tkinter, от которого наследуется класс главного окна
    def __init__(self, root):   # Конструктор класса
        super().__init__(root)  # Метод super() отыскивает базовый класс у класса Main() и возвращает его
        self.init_main()    # Вызываем функцию из конструктора класса.
        self.db = db    # созданный экземпляр класса подаём в конструктор класса Main
        self.view_records() # при запуске программы в первый раз вызываем из конструктора класса Main

    def init_main(self):    # будем хранить и инициализировать все объекты графического интерфейса
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)  # Создаём панель инструментов.
        toolbar.pack(side=tk.TOP, fill=tk.X)    # панель в верхней части окна, растянет панель по горизонтали

        self.add_img = tk.PhotoImage(file='add3.png')   # Вызываем класс, который умеет читать изображения.
        btn_open_dialog = tk.Button(toolbar, text="Добавить позицию", command=self.open_dialog, bg='#d7d8e0', bd=2,
                                    compound=tk.TOP, image=self.add_img)    # код кнопки, её атрибуты
        btn_open_dialog.pack(side=tk.LEFT)

        # Добавляем кнопку "Редактировать" в тулбар главного окна программы.
        self.update_img = tk.PhotoImage(file='update2.png')    # Укажем класс для переменной и укажем путь к иконке.
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка, которая будет вызывать функцию delete_records.
        self.delete_img = tk.PhotoImage(file='delete2.png')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка "Поиск"
        self.search_img = tk.PhotoImage(file='search2.png')     # Добавим кнопку в toolbar, вызывающую окно поиска.
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка "Обновить", которая будет вызывать функцию view_records.
        self.refresh_img = tk.PhotoImage(file='refresh2.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                    compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавим виджет treeview на главное окно программы.
        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')

        # Добавим параметры колонкам, которые указали в кортеже.
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=250, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        # Даём привычное название колонкам.
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='доход/расход')
        self.tree.heading('total', text='Сумма')

        # Чтобы виджеты treeview отображались в главном окне, применим метод pack.
        self.tree.pack(side=tk.LEFT)    # Выравнивание слева для добавления полосы прокрутки.

        # Создание полосы прокрутки виджетом scrollbar.
        scroll = tk.Scrollbar(self, command=self.tree.yview)    # Позволяет прокрутить содержимое.
        scroll.pack(side=tk.LEFT, fill=tk.Y)    # Растягивание по оси Y, т.е. по вертикали.
        self.tree.configure(yscrollcommand=scroll.set)  # Конфигурация. Связывание перемещения с виджетом Treeview,
                                                                                        # движение самого scrollbar.
    # Промежуточная функция records, которая будет служить в качестве вызова двух других функций
    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)  # Вызовем из функции records функцию insert_data класса DB.
        self.view_records() # после каждого добавления поля мы выполняем функцию для отображения в виджете Treeview

    # Функция, которая будет выполнять действие по редактированию или обновлению записей в базе данных finance.
    def update_record(self, description, costs, total):
        #SQL-запрос, который отвечает за обновление полей таблицы базы данных finance.
        self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
                          (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()     # Чтобы отобразить в таблице главного окна обновлённую информацию в базе.

    # Функция, чтобы отобразить информацию из базы данных в виджете treeview главного окна программы.
    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')  # SELECT запрос из таблицы finance.
        # Генератор списка, цикл получения строк и их последующего удаления.
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Генератор списка, чтобы отобразить содержимое базы данных.
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Функция, чтобы из таблицы виджета Treeview мы могли удалять записи.
    def delete_records(self):
        # Цикл, чтобы удалять по несколько выделенных записей одновременно.
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM finance WHERE id=?''', (self.tree.set(selection_item,
                                                                                   '#1'),))
        self.db.conn.commit()   # Сохраняем изменения.
        self.view_records()     # Чтобы отобразить в таблице главного окна обновлённую информацию БД.

    # Реализация функции поиска по наименованию в БД.
    def search_records(self, description):  # Определим функцию, передадим на вход переменную.
        description = ('%' + description + '%',) # Заключаем искомое слово из окна поиска в подстановочные символы.
        self.db.c.execute('''SELECT * FROM finance WHERE description LIKE ?''', description)    # SQL-запрос
        # Отображаем данные поиска в виджете Treeview.
        [self.tree.delete(i) for i in self.tree.get_children()]   #  очистим содержимое виджета
            # отображаем результаты поиска
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):  # отвечает за вызов дочернего окна
        Child()

    def open_update_dialog(self):   # Будет выполняться по нажатию кнопки "Редактировать" и вызывать класс Update.
        Update()

    def open_search_dialog(self):   # Будет вызывать окно поиска по нажатию кнопки с главного окна программы.
        Search()


class Child(tk.Toplevel):   # Создаём класс дочернего окна, наследуемся от объекта Toplevel.
    def __init__(self):     # Создаём конструктор класса, прописываем метод super
        super().__init__(root)
        self.init_child()   # вызов функции init_child()
        self.view = app    # передадим класс Main в класс Child

    def init_child(self):   # Пишем функцию, в которой будем инициализировать обекты и виджеты окна.
        self.title('Добавить расходы/доходы')
        self.geometry('500x220+400+300')
        self.resizable(False, False)

        # Подписываем поля ввода с помощью виджета Label.
        label_description = tk.Label(self, text='Наименование: ')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья д./р.: ')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма: ')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)    # Виджет для организации полей ввода доходов или затрат
        self.entry_description.place(x=200, y=50)   # координаты места расположения виджета

        self.entry_many = ttk.Entry(self)       # Поле для ввода суммы денег.
        self.entry_many.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])    # выпадающий список
        self.combobox.current(0)    # отображение по умолчанию
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy) # Кнопка закрытия дочернего окна
        btn_cancel.place(x=310, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')  # Кнопка добавления введённых данных
        self.btn_ok.place(x=200, y=170)
        # Укажем, чтобы кнопка срабатывала по нажатию левой кнопки мыши.
        # С помощью метода get получаем значение из виджетов и сразу же передаём в функцию records
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_many.get()))

        self.grab_set()     # перехватывает все события, происходящие в приложении (не работает)
        self.focus_set()    # захватывает и удерживает фокус (не работает)


# Реализуем отдельную форму ввода данных корректировки.
class Update(Child):        # Создадим класс Update, который будет наследоваться от класса Child.
    def __init__(self):     # Создаём конструктор класса.
        super().__init__()  # Прописываем метод super.
        # Чтобы изменения в графическом интерфейсе отобразились пользователю,
        self.init_edit()    # вызовем функцию init_edit из конструктора класса Update.
        # Чтобы обращаться к функциям из класса Main, передадим его в тот же конструктор класса Update.
        self.view = app
        self.db = db        # Чтобы из класса Update обращаться в класс DB, передадим его в данный класс.
        self.default_data()     # Вызовем функцию в конструкторе класса.

    def init_edit(self):    # Изменим графическую часть окна.
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=170, y=170)
        # По нажатию кнопки "Редактировать" необходимо передать в функцию update_record данные из полей ввода.
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_many.get()))
        self.btn_ok.destroy()   # Чтобы убрать кнопку "ок" используем метод destroy.

    # Извлекает из БД запись, которая в данный момент выделена в таблице основного окна,
    # и помещает информацию в соответствующие поля.
    def default_data(self):
        # Выполним SQL-запрос, который вернёт нам значение из выделенной строки в таблице.
        self.db.c.execute('''SELECT * FROM finance WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()  # В переменной будем сохранять значение полей результата запроса.
        self.entry_description.insert(0, row[1])   # В названия полей ввода ставим значения, полученные из БД.
        # Условная конструкция, для сравнения полученного из кортежа значения с индексом 2 со словом "доход".
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_many.insert(0, row[3])   # По подобию поля entry_description.


class Search(tk.Toplevel):   # Класс для поиска в БД. Наследуется от объекта Toplevel.
    def __init__(self):     # Конструктор класса.
        super().__init__()    # Прописываем метод super.
        self.init_search()    # Вызываем функцию через конструктор класса.
        self.view = app     # Передаём класс Main в класс Search.

    def init_search(self):  # Функция, которой будем инициализировать все графические объекты интерфейса.
        self.title('Поиск')     # Имя окна
        self.geometry('500x200+400+300')    # Размер
        self.resizable(False, False)    # Запрет изменения размера.

        label_search = tk.Label(self, text='Поиск')     # Добавим виджет label с надписью "Поиск".
        label_search.place(x=120, y=50)

        self.entry_search = ttk.Entry(self)     # Добавим поле ввода данных для поиска.
        self.entry_search.place(x=180, y=50, width=200)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)     # Кнопка закрытия окна.
        btn_cancel.place(x=290, y=100)

        btn_search = ttk.Button(self, text='Поиск')     # Кнопка поиска
        btn_search.place(x=180, y=100)
        # Добавим вызов функции search_records в кнопку поиска в том же окне поиска.
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        # Чтобы после нажатия кнопки "Поиск" окно автоматически закрывалось, добавим ещё один метод.
        # Параметр add, позволит вешать на одну кнопку вызов нескольких функций.
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:       # Реализуем класс, который будет отвечать за работу с БД.
    def __init__(self):     # конструктор класса
        self.conn = sqlite3.connect('finance.db')   # Создадим соединение с БД методом connect
        self.c = self.conn.cursor()     # Создание объекта cursor для взаимодействия с БД.
        self.c.execute('''CREATE TABLE IF NOT EXISTS finance
                        (id INTEGER PRIMARY KEY,
                        description TEXT,
                        costs TEXT,
                        total REAL)''')     # Создание таблицы БД.
        self.conn.commit()      # Сохраняем изменения в БД методом commit.

    def insert_data(self, description, costs, total):   # функция, на вход значения из трёх переменных
        self.c.execute('''INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)''',
                       (description, costs, total))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()      # Инструкция создаёт корневое окно программы
    db = DB()  # Экземпляр класса DB для того, чтобы обращаться к функциям класса DB из класса Main
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry('765x450+300+200')    # Размеры окна и точку, где оно будет появляться
    root.resizable(False, False)
    root.mainloop()