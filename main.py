import sqlite3


# Создан для обработки ситуации,
# когда пытается быть добавлен склад,
# который уже существует в базе данны
class WarehouseExistsError(Exception):
    pass

class WarehouseManager:
    # Устанавливает соединение с базой данных
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouses (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                location TEXT
                              )''')
        self.connection.commit()
    
    # Возвращает список всех складов из БД
    def list_warehouses(self):
        self.cursor.execute("SELECT * FROM warehouses")
        return self.cursor.fetchall()
    
    # Добавляет новый склад в базу данных
    # Перед добавлением выполняет проверку, 
    # существует ли уже склад с таким именем и местоположением 
    # Если да, вызывает исключение WarehouseExistsError
    def add_warehouse(self, warehouse):
        existing_warehouse = self.find_warehouse(warehouse.name, warehouse.location)
        if existing_warehouse:
            raise WarehouseExistsError("Warehouse already exists.")
        else:
            self.cursor.execute("INSERT INTO warehouses (name, location) VALUES (?, ?)",
                                (warehouse.name, warehouse.location))
            self.connection.commit()

    # Обновляет информацию о складе
    def update_warehouse(self, warehouse, new_name, new_location):
        self.cursor.execute("UPDATE warehouses SET name=?, location=? WHERE id=?",
                        (new_name, new_location, warehouse.id))
        self.connection.commit()

    # Удаляет все товары из указанного склада
    def remove_products_from_warehouse(self, warehouse_id):
        self.cursor.execute("DELETE FROM products WHERE warehouse_id=?", (warehouse_id,))
        self.connection.commit()

    # Удаляет склад
    # Для этого сначала удаляет все товары из этого склада, 
    # затем сам склад
    def remove_warehouse(self, warehouse_id):
        # Удаление товаров из склада
        self.remove_products_from_warehouse(warehouse_id)
        # Удаление склада
        self.cursor.execute("DELETE FROM warehouses WHERE id=?", (warehouse_id,))
        self.connection.commit()
    
    # Ищет склад по имени и местоположению в БД
    # и возвращает его, если он существует
    def find_warehouse(self, name, location):
        self.cursor.execute("SELECT * FROM warehouses WHERE name=? AND location=?", (name, location))
        return self.cursor.fetchone()

class Warehouse:
    # Отслеживания последнего присвоенного идентификатора склада
    last_id = 0

    def __init__(self, name, location):
        # id увеличивается с каждым новым созданным складом
        Warehouse.last_id += 1
        self.id = Warehouse.last_id
        self.name = name
        self.location = location
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            amount INTEGER,
                            price REAL,
                            warehouse_id INTEGER,
                            FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                          )''')
        self.connection.commit()

    # Получает список всех товаров, связанных с этим складом, из БД
    def list_products(self):
        self.cursor.execute("SELECT * FROM products WHERE warehouse_id=?", (self.id,))
        return self.cursor.fetchall()
    
    # Добавляет новый продукт на склад в БД
    def add_product(self, product):
        self.cursor.execute("INSERT INTO products (name, amount, price, warehouse_id) VALUES (?, ?, ?, ?)",
                            (product.name, product.amount, product.price, self.id))
        self.connection.commit()

    # Обновляет информацию о продукте на складе
    def update_product(self, product):
        self.cursor.execute("UPDATE products SET name=?, amount=?, price=? WHERE id=?",
                            (product.name, product.amount, product.price, product.id))
        self.connection.commit()

    # Удаляет указанный продукт со склада
    def remove_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.connection.commit()

class Product:
    def __init__(self, id, name, amount, price, warehouse_id) -> None:
        self.id = id
        self.name = name
        self.amount = amount
        self.price = price
        self.warehouse_id = warehouse_id
