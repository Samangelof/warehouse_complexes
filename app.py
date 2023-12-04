import tkinter as tk
import sqlite3
import tkinter.messagebox as messagebox


class WarehouseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Manager")

        # Создает соединение с базой данных
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

        # Размеры окна
        self.root.geometry("800x500")

        # Создаем метку для отображения текста 
        self.warehouses_label = tk.Label(self.root, text="Все склады:")
        self.warehouses_label.pack()

        # Создает список складов (с большей шириной)
        self.warehouse_listbox = tk.Listbox(self.root, width=50)
        self.warehouse_listbox.pack(padx=10, pady=10)

        # Получает и отображает список складов
        self.show_warehouses()

        # Кнопка для добавления нового склада
        self.add_button = tk.Button(self.root, text="Добавить склад", command=self.add_warehouse)
        self.add_button.pack(pady=5)

        # Кнопка для удаления выбранного склада
        self.remove_button = tk.Button(self.root, text="Удалить склад", command=self.remove_warehouse)
        self.remove_button.pack(pady=5)

        self.warehouse_listbox.bind('<<ListboxSelect>>', self.show_products)


    def show_products(self, event):
        selected_warehouse = self.warehouse_listbox.curselection()
        if selected_warehouse:
            warehouse_info = self.warehouse_listbox.get(selected_warehouse)
            warehouse_id = int(warehouse_info.split('-')[0].strip())

            if not hasattr(self, 'products_window') or not self.products_window:
                self.products_window = tk.Toplevel(self.root)
                self.products_window.title("Товары в складе")

                self.new_product_frame = tk.Frame(self.products_window)
                self.new_product_frame.pack(padx=10, pady=10)

                # Создание полей для ввода информации о новом продукте
                self.name_label = tk.Label(self.new_product_frame, text="Название:")
                self.name_label.grid(row=0, column=0)
                self.name_entry = tk.Entry(self.new_product_frame)
                self.name_entry.grid(row=0, column=1)

                self.amount_label = tk.Label(self.new_product_frame, text="Количество:")
                self.amount_label.grid(row=1, column=0)
                self.amount_entry = tk.Entry(self.new_product_frame)
                self.amount_entry.grid(row=1, column=1)

                self.price_label = tk.Label(self.new_product_frame, text="Цена:")
                self.price_label.grid(row=2, column=0)
                self.price_entry = tk.Entry(self.new_product_frame)
                self.price_entry.grid(row=2, column=1)

                # Кнопка для добавления нового продукта
                self.add_product_button = tk.Button(
                    self.new_product_frame, text="Добавить", command=lambda: self.save_product(warehouse_id)
                )
                self.add_product_button.grid(row=3, columnspan=2, pady=5)

                # Создаем список для отображения товаров
                self.products_listbox = tk.Listbox(self.products_window)
                self.products_listbox.pack(padx=10, pady=10)

                # Получаем товары для выбранного склада из базы данных
                self.cursor.execute("SELECT * FROM products WHERE warehouse_id=?", (warehouse_id,))
                products = self.cursor.fetchall()
                for product in products:
                    self.products_listbox.insert(
                        tk.END, f"{product[0]} - {product[1]} - {product[2]} - {product[3]}"
                    )

                # Устанавливаем обработчик закрытия окна с продуктами
                self.products_window.protocol("WM_DELETE_WINDOW", self.on_products_window_close)
    
    def save_warehouse(self):
        # Получает данные из полей ввода
        name = self.name_entry.get()
        location = self.location_entry.get()

        # Проверяет, что поля не пустые
        if not name or not location:
            # Ругается, если поля пустые
            messagebox.showerror("Ошибка", "Поля не могут быть пустыми")
            
            # Закрывает окно добавления склада, если оно открыто
            if hasattr(self, 'add_window') and self.add_window:
                self.add_window.destroy()
                self.add_window = None
            return

        # Добавляет новый склад в БД
        self.cursor.execute("INSERT INTO warehouses (name, location) VALUES (?, ?)", (name, location))
        self.connection.commit()

        # Закрывает окно добавления склада
        if hasattr(self, 'add_window') and self.add_window:
            self.add_window.destroy()
            self.add_window = None
            
        # Обновляет список складов после добавления нового склада
        self.show_warehouses()

    def save_product(self, warehouse_id):
        # Получает данные из полей ввода
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        price = self.price_entry.get()

        # Проверяет, что поля не пустые
        if not name or not amount or not price:
            # Ругается, если поля пустые
            messagebox.showerror("Ошибка", "Поля не могут быть пустыми")
            
            # Закрывает окно с продуктами, если оно открыто
            if hasattr(self, 'products_window') and self.products_window:
                self.products_window.destroy()
                self.products_window = None
            return

        # Добавляем новый продукт в базу данных
        self.cursor.execute(
            "INSERT INTO products (name, amount, price, warehouse_id) VALUES (?, ?, ?, ?)",
            (name, amount, price, warehouse_id)
        )
        self.connection.commit()

        # Получаем ID последнего добавленного продукта
        self.cursor.execute("SELECT last_insert_rowid()")
        product_id = self.cursor.fetchone()[0]

        # Обновляем отображение списка товаров
        self.products_listbox.insert(tk.END, f"{product_id} - {name} - {amount} - {price}")
        self.clear_entries()

    # Функция для очистки полей ввода
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    # Функция, вызываемая при закрытии окна с продуктами
    def on_products_window_close(self):
        self.products_window.destroy()
        self.products_window = None

    def show_warehouses(self):
        # Очищает список складов перед обновлением
        self.warehouse_listbox.delete(0, tk.END)

        # Получает склады из БД и отображаем их
        self.cursor.execute("SELECT * FROM warehouses")
        warehouses = self.cursor.fetchall()
        for warehouse in warehouses:
            self.warehouse_listbox.insert(tk.END, f"{warehouse[0]} - {warehouse[1]} - {warehouse[2]}")

    def add_warehouse(self):
        if not hasattr(self, 'add_window') or not self.add_window:
            self.add_window = tk.Toplevel(self.root)
            self.add_window.title("Добавить склад")
            self.add_window.geometry("300x200")

            self.name_label = tk.Label(self.add_window, text="Название склада:")
            self.name_label.pack()

            self.name_entry = tk.Entry(self.add_window)
            self.name_entry.pack(pady=5)

            self.location_label = tk.Label(self.add_window, text="Местоположение:")
            self.location_label.pack()

            self.location_entry = tk.Entry(self.add_window)
            self.location_entry.pack(pady=5)

            self.add_warehouse_button = tk.Button(self.add_window, text="Добавить", command=self.save_warehouse)
            self.add_warehouse_button.pack(pady=5)

    def remove_warehouse(self):
        # Получаем выбранный склад из Listbox
        selected_warehouse = self.warehouse_listbox.curselection()
        if selected_warehouse:
            warehouse_info = self.warehouse_listbox.get(selected_warehouse)
            warehouse_id = int(warehouse_info.split('-')[0].strip())  # Получаем ID склада
            
            # Удаляем все товары, связанные с этим складом
            self.cursor.execute("DELETE FROM products WHERE warehouse_id=?", (warehouse_id,))
            self.connection.commit()

            # Удаляем сам склад
            self.cursor.execute("DELETE FROM warehouses WHERE id=?", (warehouse_id,))
            self.connection.commit()
            
            self.show_warehouses()  # Обновляем список складов после удаления


    def on_products_window_close(self):
        if hasattr(self, 'products_window') and self.products_window:
            self.products_window.destroy()
            self.products_window = None
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)

# Создаем и запускаем приложение
root = tk.Tk()
root.title("Warehouse Manager")

app = WarehouseManagerApp(root)
root.mainloop()