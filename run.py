from main import (
    WarehouseManager,
    Warehouse,
    Product
)


""" Манипуляции складами"""
# Добавляет, удаляет, обновляет, показывает (склады)
warehouse_manager = WarehouseManager('db.db')

#* [Добавляет] Создает экземпляр/объект склада и добавляет склад во все склады
    # - 1 аргумент = название склада
    # - 2 арг. имя склада
warehouse_moscow = Warehouse('Склад 1', 'Москва')
warehouse_kazan = Warehouse('Склад 2', 'Казань')

# Добавляем склад в склады 
warehouse_manager.add_warehouse(warehouse_moscow)
warehouse_manager.add_warehouse(warehouse_kazan)

#todo [Показывает] все склады 
print(warehouse_manager.list_warehouses())
#todo [Поиск] Поиск по имени и местоположению

print(warehouse_manager.find_warehouse('Склад 1', 'Москва'))
#? [Обновляет] Склад
    # - 1 аргумент = объект класа
    # - 2 арг. имя склада
    # - 3 арг. местоположение
# warehouse_manager.update_warehouse(warehouse_moscow, 'Склад 2', 'Казань')

#! [Удаление] склада находится внизу файла

""" Манипуляции товаром/продуктами"""
# Создает экземпляр продукта
    # - 1 аргумент=ID продукта будет присвоен автоматически, 
    # поэтому передает None
    # - 2 арг. название продукта
    # - 3 арг. количество
    # - 4 арг. цена
    # - 5 арг. id склада (положит товар в указаный id склада)
product1 = Product(None, "Монитор", 10, 50.0, 1)
product2 = Product(None, "Корзина для фруктов", 10, 2.0, 2)


#* [Добавляет] продукт в склад
warehouse_moscow.add_product(product1)
warehouse_kazan.add_product(product2)


#todo [Показывает] все продукты в указаном складе
print('[MOSCOW]', warehouse_moscow.list_products())
print('[KAZAN]', warehouse_kazan.list_products())


#? [Обновляет] информацию о продукте в складе
# Создание экземпляра продукта с обновленными данными
    # - 1 арг. id товара,
    # - 2, 3, 4, 5 - имя, кол-во, цена, id склада
# updated_product = Product(1, "Новое название", 15, 60.0, 1)
# warehouse_moscow.update_product(updated_product)


#! [Удаляет] продукт со склада - передает id продукта
# warehouse_moscow.remove_product(1)

#! [Удаляет] Склад и все товары которые находились на складе
    # - 1 аргумент = id склада
# warehouse_manager.remove_warehouse(1)