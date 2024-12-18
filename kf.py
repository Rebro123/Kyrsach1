import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime
from PIL import Image
connection = sqlite3.connect('my_database.db')  #Подключаемся к базе данных
cursor = connection.cursor()
connection.execute("PRAGMA foreign_keys = ON;")
cursor.execute('''
CREATE TABLE IF NOT EXISTS telephone (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
brand TEXT NOT NULL,
IMEI INTEGER NOT NULL,
Date_of_admission DATA NOT NULL,
Date_of_purchase DATA,
Admission_price FLOAT NOT NULL,
Sale_price FLOAT NOT NULL,
processor TEXT NOT NULL,
RAM TEXT NOT NULL,
OS TEXT NOT NULL
)
''')

connection1 = sqlite3.connect('my_database.db')  #Подключаемся к базе данных
cursor1 = connection1.cursor()
cursor1.execute('''
CREATE TABLE IF NOT EXISTS Accessories (
id INTEGER PRIMARY KEY AUTOINCREMENT,
telephone_id INTEGER,
name TEXT NOT NULL,
price FLOAT NOT NULL,
date_of_sale TEXT NOT NULL,
FOREIGN KEY (telephone_id) REFERENCES telephone(id)
)
''')
connection2 = sqlite3.connect('my_database.db')  #Подключаемся к базе данных
cursor5 = connection2.cursor()
cursor5.execute('''
CREATE TABLE IF NOT EXISTS Services (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
price INTEGER NOT NULL,
data_of_sale_services DATA NOT NULL
)
''')
# Функция для обновления Treeview
def show_sold_items():
    # Очищаем текущие записи в Treeview
    for row in tree.get_children():
        tree.delete(row)
    # Подключаемся к базе данных
    try:
        connection = sqlite3.connect("my_database.db")  # Замените на имя вашей базы данных
        cursor = connection.cursor()

        # Выполняем запрос для получения проданных товаров
        cursor.execute("SELECT * FROM telephone WHERE Date_of_purchase IS NOT NULL")
        sold_items = cursor.fetchall()

        # Проверяем, есть ли записи
        if not sold_items:
            messagebox.showinfo("Информация", "Нет проданных товаров с датой покупки.")
            return

        # Вставляем записи в Treeview
        for item in sold_items:
            tree.insert("", "end", values=item)

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", str(e))
    finally:
        if connection:
            connection.close()

def show_sold_items_1():
    # Очищаем текущие записи в Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Подключаемся к базе данных
    try:
        connection = sqlite3.connect("my_database.db")  # Замените на имя вашей базы данных
        cursor = connection.cursor()

        # Выполняем запрос для получения проданных товаров
        cursor.execute("SELECT * FROM telephone WHERE Date_of_purchase IS NULL")
        sold_items = cursor.fetchall()

        # Проверяем, есть ли записи
        if not sold_items:
            messagebox.showinfo("Информация", "Нет купленных товаров.")
            return

        # Вставляем записи в Treeview
        for item in sold_items:
            tree.insert("", "end", values=item)

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", str(e))
    finally:
        if connection:
            connection.close()


def open_date_window():
    add_window_2 = tk.Toplevel(root)
    add_window_2.title("Прибыль за определённый период")
    add_window_2.geometry("800x400")

    global start_date_entry
    start_date_entry = tk.Entry(add_window_2)
    start_date_entry.pack(pady=5, anchor="nw", padx=10)

    global end_date_entry
    end_date_entry = tk.Entry(add_window_2)
    end_date_entry.pack(pady=5, anchor="nw", padx=10)

    label1 = ttk.Label(add_window_2, text="Введите начальную дату", font=("Arial", 10))
    label1.place(x=200, y=15)

    label2 = ttk.Label(add_window_2, text="Введите конечную дату", font=("Arial", 10))
    label2.place(x=200, y=35)

    calculate_button = ttk.Button(add_window_2, text="Посчитать прибыль", command=on_calculate_button_click)
    calculate_button.pack(pady=10, anchor="se")

    # Создание Treeview для отображения записей
    global treeview
    treeview = ttk.Treeview(add_window_2, columns=("Date", "Sale Price", "Admission Price", "Total Profit"),
                            show="headings")
    treeview.heading("Date", text="Дата")
    treeview.heading("Sale Price", text="Цена продажи")
    treeview.heading("Admission Price", text="Цена поступления")
    treeview.heading("Total Profit", text="Итоговая прибыль")
    treeview.pack(pady=20, fill=tk.BOTH, expand=True)


def calculate_profit_and_get_records(start_date, end_date):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    profit_query = """
            SELECT SUM(Sale_price - Admission_price) AS profit
            FROM telephone
            WHERE Date_of_purchase IS NOT NULL AND Date_of_purchase BETWEEN ? AND ?;
        """
    cursor.execute(profit_query, (start_date, end_date))
    profit = cursor.fetchone()[0]  # Здесь profit может быть None, если нет записей

    records_query = """
            SELECT Date_of_admission, Sale_price, Admission_price
            FROM telephone
            WHERE Date_of_admission BETWEEN ? AND ?;
        """
    cursor.execute(records_query, (start_date, end_date))
    records = cursor.fetchall()
    conn.close()

    # Возвращаем profit, даже если он отрицательный, и records
    return profit, records


def on_calculate_button_click():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    if not start_date or not end_date:
        tk.messagebox.showerror("Ошибка", "Пожалуйста, введите обе даты.")
        return

    # Вычисление прибыли и получение записей
    profit, records = calculate_profit_and_get_records(start_date, end_date)

    # Очистка Treeview перед отображением новых данных
    for row in treeview.get_children():
        treeview.delete(row)

    # Добавление записей в Treeview
    for record in records:
        treeview.insert("", tk.END, values=record + (None,))

    # Добавление строки с итоговой прибылью
    total_profit_record = (None, None, None, profit)  # profit может быть отрицательным
    treeview.insert("", tk.END, values=total_profit_record)

def open_add_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавление записи")
    add_window.geometry("500x600")
    entry = ttk.Entry(add_window)
    entry.pack(pady=20, anchor="nw", padx=10)
    combobox = ttk.Combobox(add_window)
    combobox.pack(pady=20, anchor="nw", padx=10)
    entry1 = ttk.Entry(add_window)
    entry1.pack(pady=20, anchor="nw", padx=10)
    date_entry = DateEntry(add_window, width=12, background='darkblue', foreground='white', borderwidth=2, pady=20)
    date_entry.pack(pady=20, anchor="nw", padx=10)
    entry2 = ttk.Entry(add_window)
    entry2.pack(pady=20, anchor="nw", padx=10)
    entry3 = ttk.Entry(add_window)
    entry3.pack(pady=20, anchor="nw", padx=10)
    combobox2 = ttk.Combobox(add_window)
    combobox2.pack(pady=10, anchor="nw", padx=10)
    entry4 = ttk.Entry(add_window)
    entry4.pack(pady=20, anchor="nw", padx=10)
    entry5 = ttk.Entry(add_window)
    entry5.pack(pady=20, anchor="nw", padx=10)
    label = ttk.Label(add_window, text="Введите модель телефона", font=("Arial", 10))
    label.place(x=200,y=15)
    label1 = ttk.Label(add_window, text="Введите или выберите марку телефона", font=("Arial", 10))
    label1.place(x=200, y=75)
    label2 = ttk.Label(add_window, text="Введите IMEI телефона", font=("Arial", 10))
    label2.place(x=200, y=140)
    label3 = ttk.Label(add_window, text="Выберите дату получения телефона", font=("Arial", 10))
    label3.place(x=200, y=200)
    label4 = ttk.Label(add_window, text="Введите цену получения телефона", font=("Arial", 10))
    label4.place(x=200, y=260)
    label5 = ttk.Label(add_window, text="Введите цену продажи телефона", font=("Arial", 10))
    label5.place(x=200, y=320)
    label6 = ttk.Label(add_window, text="Введите или выберите название процессора", font=("Arial", 10))
    label6.place(x=200, y=380)
    label7 = ttk.Label(add_window, text="Введите кол_во оперативной памяти в ГБ", font=("Arial", 10))
    label7.place(x=200, y=430)
    label8 = ttk.Label(add_window, text="Введите название операционной системы", font=("Arial", 10))
    label8.place(x=200, y=485)

    def add_to_db():
        date_admission = date_entry.get_date()  # Получаем объект datetime.date
        date_admission_str = date_admission.strftime('%Y-%m-%d')
        values = [entry.get(), combobox.get(), entry1.get(), date_admission_str, entry2.get(), entry3.get(), combobox2.get(), entry4.get(), entry5.get()]
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO telephone (name, brand, IMEI, Date_of_admission, Admission_price, Sale_price, processor, RAM, OS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (*values,))
        conn.commit()
        conn.close()

        entry.delete(0, tk.END)  # Очистка поля ввода
        combobox.delete(0, tk.END)
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
        entry4.delete(0, tk.END)
        entry5.delete(0, tk.END)
        combobox2.delete(0,tk.END)

        combobox.set('')  # Сброс выбора в Combobox
        print("Данные добавлены в базу данных")

    button1 = ttk.Button(add_window, text="Добавить", command=add_to_db)
    button1.pack(pady=20, padx=20, anchor="se")

    def fetch_1_data_from_db(prefix):
        # Подключаемся к базе данных
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        # Выполняем SQL-запрос с LIKE для поиска по первым буквам
        cursor.execute("SELECT DISTINCT processor FROM telephone WHERE processor LIKE ?",
                       (prefix + '%',))
        rowss = cursor.fetchall()

        # Закрываем соединение с базой данных
        connection.close()

        # Возвращаем уникальные значения в виде списка
        return [row[0] for row in rowss]

    def tree_populate_combobox1():
        values = fetch_1_data_from_db("")
        combobox2['values'] = values

    def tree_on_combobox_changed(event):
        current1_text = combobox2.get()
        if current1_text:
            values = get_data_from_db(current1_text)
            combobox['values'] = values
            if values:
                combobox2.focus_set()  # Устанавливаем фокус обратно на combobox
                combobox2.event_generate('<Down>')  # Открываем выпадающий список

    def fetch_data_from_db(prefix):
        # Подключаемся к базе данных
        connection = sqlite3.connect('my_database.db')  # Замените на ваше имя базы данных
        cursor = connection.cursor()

        # Выполняем SQL-запрос с LIKE для поиска по первым буквам
        cursor.execute("SELECT DISTINCT brand FROM telephone WHERE brand LIKE ?",
                       (prefix + '%',))
        rowss = cursor.fetchall()

        # Закрываем соединение с базой данных
        connection.close()

        # Возвращаем уникальные значения в виде списка
        return [row[0] for row in rowss]

    def get_data_from_db(prefix):
        # Подключаемся к базе данных
        connection = sqlite3.connect('my_database.db')  # Замените на ваше имя базы данных
        cursor = connection.cursor()

        # Выполняем SQL-запрос с LIKE для поиска по первым буквам
        cursor.execute("SELECT DISTINCT name FROM telephone WHERE name LIKE ?",
                       (prefix + '%',))  # Замените your_column и your_table на ваши названия
        rows = cursor.fetchall()

        # Закрываем соединение с базой данных
        connection.close()

        # Возвращаем уникальные значения в виде списка
        return [row[0] for row in rows]

    def populate_combobox():
        # Функция первоначального заполнения
        values = fetch_data_from_db("")  # Получаем все значения для начального заполнения
        combobox['values'] = values

    def two_populate_combobox1():
        values = get_data_from_db("")
        combobox1['values'] = values

    def two_on_combobox_changed(event):
        current1_text = combobox1.get()
        if current1_text:
            values = get_data_from_db(current1_text)
            combobox['values'] = values
            if values:
                combobox1.focus_set()  # Устанавливаем фокус обратно на combobox
                combobox1.event_generate('<Down>')  # Открываем выпадающий список

    def on_combobox_changed(event):
        # Получаем текущее значение ввода из Combobox
        current_text = combobox.get()
        if current_text:
            # Получаем обновленные значения из базы данных
            values = fetch_data_from_db(current_text)
            combobox['values'] = values
            # Открываем выпадающий список, чтобы пользователь мог выбрать из новых значений
            if values:
                combobox.focus_set()  # Устанавливаем фокус обратно на combobox
                combobox.event_generate('<Down>')  # Открываем выпадающий список

    combobox.bind("<KeyRelease>", on_combobox_changed)
    #combobox1.bind("<KeyRelease>", two_on_combobox_changed)
    combobox2.bind("<KeyRelease>", tree_on_combobox_changed)
    populate_combobox()
    #two_populate_combobox1()
    tree_populate_combobox1()

def fetch_data():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Получение данных из таблицы
    cursor.execute("SELECT * FROM telephone")
    rows = cursor.fetchall()

    # Очищаем таблицу перед загрузкой новых данных
    for row in tree.get_children():
        tree.delete(row)

    # Заполнение таблицы данными
    for row in rows:
        tree.insert("", "end", values=row)

    # Закрытие соединения
    conn.close()

# Прописываем названия колонок для каждой таблицы
columns_mapping = {
    "telephone": ["ID", "Модель", "Брэнд", "IMEI", "Дата приёма", "Дата продажи", "Цена приёма", "Цена продажи", "Процессор", "Оперативная память", "Операционная система"],
    "Services": ["ID", "Название услуги", "Цена", "Дата продажи"],
    "Accessories": ["ID", "id_Телефона", "name", "price", "date_of_sale"]
}
def fetch_data(table_names):
    # Соединяемся с базой данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Получаем данные из выбранной таблицы
    cursor.execute(f"SELECT * FROM {table_names}")
    data = cursor.fetchall()
    conn.close()
    return data


def on_combobox_select(event):
    # Удаляем старый Treeview, если он существует
    for widget in treeview_frame.winfo_children():
        widget.destroy()

    # Получаем выбранную таблицу
    selected_table = combobox.get()

    # Извлекаем данные и названия столбцов
    data = fetch_data(selected_table)
    columns = columns_mapping[selected_table]  # Используем словарь для названий столбцов

    # Создаем новый Treeview
    global tree
    tree = ttk.Treeview(treeview_frame, show="headings")
    tree["columns"] = columns

    # Установка заголовков столбцов
    for col in columns:
        tree.heading(col, text=col)

    # Заполнение Treeview данными
    for item in data:
        tree.insert("", tk.END, values=item)

    # Установка ширины столбцов
    for col in columns:
        tree.column(col, width=100)  # Установите ширину по желанию

    # Размещение нового Treeview
    tree.pack(fill=tk.BOTH, expand=True)

    # Добавление вертикальной полосы прокрутки
    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# Подключаемся к базе данных и извлекаем названия таблиц
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = [row[0] for row in cursor.fetchall()]
conn.close()

# Функция для извлечения данных из базы данных
def fetch_telephones():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, IMEI FROM telephone')
    rows = cursor.fetchall()

    connection.close()
    return rows


def insert_accessory(telephone_id, name, price, date_of_sale):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Accessories (telephone_id, name, price, date_of_sale)
        VALUES (?, ?, ?, ?)
    ''', (telephone_id, name, price, date_of_sale))

    connection.commit()
    connection.close()


def add_accessory():
    telephone_id = selected_telephone_id.get()
    name = name_entry.get()
    price = price_entry.get()
    date_of_sale = date_entry.get()

    # Проверка на заполненность полей
    if not all([telephone_id, name, price, date_of_sale]):
        messagebox.showwarning("Ввод данных", "Пожалуйста, заполните все поля.")
        return

    insert_accessory(telephone_id, name, price, date_of_sale)
    messagebox.showinfo("Успех", "Аксессуар успешно добавлен!")
    accessory_window.destroy()


def on_double_click(event):
    selected = telephone_listbox.curselection()
    if selected:
        index = selected[0]
        selected_item = telephone_listbox.get(index)
        telephone_id = selected_item.split(" - ")[0]  # Получаем только id
        selected_telephone_id.set(telephone_id)


def open_accessory_window():
    global accessory_window, name_entry, price_entry, date_entry, selected_telephone_id, telephone_listbox

    accessory_window = tk.Toplevel(root)
    accessory_window.title("Добавить аксессуар")

    tk.Label(accessory_window, text="Выберите телефон:").grid(row=0, column=0, padx=10, pady=10)

    selected_telephone_id = tk.StringVar()

    telephone_listbox = tk.Listbox(accessory_window, width=50)
    telephone_listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Заполнение списка телефонами
    for id, name in fetch_telephones():
        telephone_listbox.insert(tk.END, f"{id} - {name}")

    telephone_listbox.bind("<Double-1>", on_double_click)  # Привязываем двойной клик

    tk.Label(accessory_window, text="Название:").grid(row=2, column=0, padx=10, pady=10)
    name_entry = tk.Entry(accessory_window)
    name_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(accessory_window, text="Цена:").grid(row=3, column=0, padx=10, pady=10)
    price_entry = tk.Entry(accessory_window)
    price_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(accessory_window, text="Дата продажи:").grid(row=4, column=0, padx=10, pady=10)
    date_entry = tk.Entry(accessory_window)
    date_entry.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(accessory_window, text="Добавить", command=add_accessory).grid(row=5, column=0, columnspan=2, pady=20)


def load_data(tree, filter_brand="", filter_model="", filter_imei=""):
    for item in tree.get_children():
        tree.delete(item)
    connection = sqlite3.connect('my_database.db')
    cursor2 = connection.cursor()
    query = """
        SELECT brand, name, IMEI, Date_of_purchase 
        FROM telephone 
        WHERE brand LIKE ? AND name LIKE ? AND IMEI LIKE ? 
        ORDER BY brand, name, IMEI
    """
    cursor2.execute(query, (f"%{filter_brand}%", f"%{filter_model}%", f"%{filter_imei}%"))
    for row in cursor2.fetchall():
        tree.insert("", tk.END, values=row)
    connection.close()


def on_item_select(event, tree, date_entry):
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item[0], 'values')
        date_entry.delete(0, tk.END)
        date_entry.insert(0, item_values[3])  # Вставляем дату покупки в поле


def update_purchase_date(tree, date_entry):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Выбор записи", "Пожалуйста, выберите запись для обновления.")
        return
    new_date = date_entry.get()
    item_values = tree.item(selected_item[0], 'values')
    imei = item_values[2]
    connection1 = sqlite3.connect('my_database.db')
    cursor1 = connection1.cursor()
    cursor1.execute("UPDATE telephone SET Date_of_purchase = ? WHERE IMEI = ?", (new_date, imei))
    connection1.commit()
    connection1.close()
    load_data(tree)  # Обновляем данные в дереве


def load_combobox_data():
    connection3 = sqlite3.connect('my_database.db')
    cursor3 = connection3.cursor()

    cursor3.execute("SELECT DISTINCT brand FROM telephone")
    brands = [row[0] for row in cursor3.fetchall()]

    cursor3.execute("SELECT DISTINCT name FROM telephone")
    models = [row[0] for row in cursor3.fetchall()]

    cursor3.execute("SELECT DISTINCT IMEI FROM telephone")
    imeis = [row[0] for row in cursor3.fetchall()]

    connection3.close()

    return brands, models, imeis


def filter_data(tree, brand_combobox, model_combobox, imei_combobox):
    filter_brand = brand_combobox.get()
    filter_model = model_combobox.get()
    filter_imei = imei_combobox.get()
    load_data(tree, filter_brand, filter_model, filter_imei)

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Управление устройствами")
    global tree
    tree = ttk.Treeview(new_window, columns=("Brand", "Model", "IMEI", "Date of Purchase"), show='headings')
    tree.heading("Brand", text="Марка")
    tree.heading("Model", text="Модель")
    tree.heading("IMEI", text="IMEI")
    tree.heading("Date of Purchase", text="Дата продажи")
    tree.pack(fill=tk.BOTH, expand=True)

    load_data(tree)

    # Загружаем данные для комбобоксов
    brands, models, imeis = load_combobox_data()

    brand_label = ttk.Label(new_window, text="Марка:")
    brand_label.pack()
    brand_combobox = ttk.Combobox(new_window, values=brands)
    brand_combobox.pack()

    model_label = ttk.Label(new_window, text="Модель:")
    model_label.pack()
    model_combobox = ttk.Combobox(new_window, values=models)
    model_combobox.pack()

    imei_label = ttk.Label(new_window, text="IMEI:")
    imei_label.pack()
    imei_combobox = ttk.Combobox(new_window, values=imeis)
    imei_combobox.pack()

    filter_button = tk.Button(new_window, text="Применить фильтр", command=lambda: filter_data(tree, brand_combobox, model_combobox, imei_combobox))
    filter_button.pack(pady=5)

    date_entry = DateEntry(new_window, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
    date_entry.pack(pady=5)

    update_button = tk.Button(new_window, text="Обновить дату покупки", command=lambda: update_purchase_date(tree, date_entry))
    update_button.pack(pady=5)

    tree.bind("<Double-1>", lambda event: on_item_select(event, tree, date_entry))


def open_add_service_window():
    # Создаем новое окно
    window = Toplevel(root)
    window.title("Добавление услуги")
    window.geometry("220x250")

    # Поле для ввода названия услуги
    tk.Label(window, text="Название услуги:").pack(pady=5)
    service_name_entry = tk.Entry(window)
    service_name_entry.pack(pady=5)

    # Поле для ввода цены услуги
    tk.Label(window, text="Цена услуги:").pack(pady=5)
    service_price_entry = tk.Entry(window)
    service_price_entry.pack(pady=5)

    # Выбор даты
    tk.Label(window, text="Дата продажи:").pack(pady=5)
    sale_date_entry = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=2, pady=20)
    sale_date_entry.pack(pady=5)
    #sale_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))  # Устанавливаем текущую дату по умолчанию

    def save_service():
        service_name = service_name_entry.get()
        service_price = service_price_entry.get()
        sale_date = sale_date_entry.get()

        if service_name and service_price and sale_date:
            try:
                service_price = float(service_price)
                connections = sqlite3.connect('my_database.db')
                cursor = connections.cursor()
                # Сохраняем запись в базу данных
                cursor.execute('INSERT INTO Services (name, price, data_of_sale_services) VALUES (?, ?, ?)',
                               (service_name, service_price, sale_date))
                connections.commit()
                connection.close()
                messagebox.showinfo("Успешно", "Запись успешно добавлена!")
                window.destroy()  # Закрываем окно после сохранения
            except ValueError:
                messagebox.showwarning("Ошибка", "Цена должна быть числом!")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля!")

    # Кнопка для сохранения услуги
    save_button = tk.Button(window, text="Сохранить", command=save_service)
    save_button.pack(pady=10)

# Создаем основное окно
root = tk.Tk()
root.title("База данных магазина")
root.geometry("1540x900")
root.resizable(False, False)
# Создаем Combobox для выбора таблиц
combobox = ttk.Combobox(root, values=table_names)
combobox.bind("<<ComboboxSelected>>", on_combobox_select)
combobox.pack(pady=10, anchor="n")


# Кнопка для добавления аксессуаров
add_accessory_button = ttk.Button(root, text="Добавить аксессуар", command=open_accessory_window)
add_accessory_button.pack(padx=10, anchor="nw")
#Создаём кнопку для подсчета прибыли
btn4 = ttk.Button(text="Прибыль по телефонам", command=open_date_window)
btn4.pack(anchor='nw', padx=10)
#Кнопка для добавления услуги
add_service_btn = ttk.Button(root, text="Оказать услугу", command=open_add_service_window)
add_service_btn.pack(padx=10, anchor="nw")
#Cоздаём button
btn = ttk.Button(text="Добавить", command=open_add_window)
btn.pack(anchor="se", pady=10)
#Создаём кнопку продажи телефона
open_window_button = ttk.Button(root, text="Продать телефон", command=open_new_window)
open_window_button.pack(pady=10, anchor="se")
#Создаём кнопку фильтра
btn2 = ttk.Button(text="Не проданные", command=show_sold_items_1)
btn2.pack(anchor="se", pady=10)
#Cоздаём вторую кнопку фильтра
btn3 = ttk.Button(text="Проданные", command=show_sold_items)
btn3.pack(anchor="se", pady=10)
# Создаем фрейм для размещения Treeview
treeview_frame = tk.Frame(root)
treeview_frame.pack(fill=tk.BOTH, expand=True)
# Кнопка для получения данных
#fetch_button = tk.Button(root, text="Загрузить данные", command=fetch_data)
#fetch_button.pack(pady=5)
root.mainloop()


