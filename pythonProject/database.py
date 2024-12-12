import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def calculate_profit(start_date, end_date):
    # Соединяемся с базой данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # SQL-запрос для вычисления прибыли
    query = """
    SELECT SUM(CASE WHEN Date_of_purchase IS NOT NULL THEN Sale_price - Admission_price ELSE 0 END) 
    FROM telephone 
    WHERE Date_of_admission BETWEEN ? AND ?
    """

    cursor.execute(query, (start_date, end_date))
    profit = cursor.fetchone()[0]
    conn.close()

    return profit if profit is not None else 0


def on_calculate_button_click():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Проверка на корректность введенных данных
    if not start_date or not end_date:
        messagebox.showerror("Ошибка", "Пожалуйста, введите обе даты.")
        return

    # Вычисление прибыли
    profit = calculate_profit(start_date, end_date)
    messagebox.showinfo("Прибыль", f"Прибыль с {start_date} по {end_date}: {profit}")


def open_date_window():
    # Создаем новое окно
    date_window = tk.Toplevel(root)
    date_window.title("Ввод дат")

    # Поля для ввода дат
    tk.Label(date_window, text="Дата приема (YYYY-MM-DD):").pack(pady=5)
    global start_date_entry
    start_date_entry = tk.Entry(date_window)
    start_date_entry.pack(pady=5)

    tk.Label(date_window, text="Дата продажи (YYYY-MM-DD):").pack(pady=5)
    global end_date_entry
    end_date_entry = tk.Entry(date_window)
    end_date_entry.pack(pady=5)

    # Кнопка для расчета
    calculate_button = tk.Button(date_window, text="Посчитать прибыль", command=on_calculate_button_click)
    calculate_button.pack(pady=10)


# Создаем главное окно
root = tk.Tk()
root.title("Database Viewer")

# Кнопка для открытия окна выбора дат
open_dates_button = tk.Button(root, text="Выбрать даты", command=open_date_window)
open_dates_button.pack(pady=10)

# Запуск главного цикла приложения
root.mainloop()