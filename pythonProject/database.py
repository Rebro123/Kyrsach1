import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import io

# Создаем или подключаемся к базе данных
conn = sqlite3.connect('images_database.db')
cursor = conn.cursor()

# Создаем таблицу, если ее еще нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    image BLOB NOT NULL
)
''')
conn.commit()


def upload_image():
    # Функция для загрузки изображения
    file_path = tk.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        with open(file_path, 'rb') as file:
            img_data = file.read()
            description = description_entry.get()
            cursor.execute('INSERT INTO images (description, image) VALUES (?, ?)', (description, img_data))
            conn.commit()
            messagebox.showinfo("Успешно", "Изображение успешно загружено!")
            description_entry.delete(0, tk.END)
            load_images()


def load_images():
    # Функция для загрузки изображений в Treeview
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute('SELECT id, description FROM images')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)


def view_image(event):
    # Функция для отображения изображения в отдельном окне
    selected_item = tree.selection()
    if not selected_item:
        return
    item = tree.item(selected_item)
    image_id = item['values'][0]

    cursor.execute('SELECT image FROM images WHERE id = ?', (image_id,))
    img_data = cursor.fetchone()[0]

    # Oткрываем изображение с использованием PIL
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((400, 400))  # Изменяем размер для отображения
    img_tk = ImageTk.PhotoImage(img)

    view_window = Toplevel(root)
    view_window.title("Просмотр изображения")

    img_label = tk.Label(view_window, image=img_tk)
    img_label.image = img_tk  # Сохраняем ссылку на изображение
    img_label.pack()


# Создаем основное окно
root = tk.Tk()
root.title("Управление изображениями")

# Поле для описания изображения
description_entry = tk.Entry(root, width=40)
description_entry.pack(pady=10)

# Кнопка для загрузки изображения
upload_button = tk.Button(root, text="Загрузить изображение", command=upload_image)
upload_button.pack(pady=10)

# Treeview для отображения загруженных изображений
tree = ttk.Treeview(root, columns=('ID', 'Описание'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Описание', text='Описание')
tree.pack(pady=10)

tree.bind('<<TreeviewSelect>>', view_image)  # Обработчик события выбора

load_images()  # Загружаем изображения при запуске

# Запускаем основной цикл
root.mainloop()

# Закрываем соединение с базой данных перед выходом
conn.close()