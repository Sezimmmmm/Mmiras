import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# SQL-запрос для вставки данных
cursor.execute("""
INSERT INTO cars (brand, model, price, mileage, body_type, image)
VALUES 
('Toyota', 'Camry', 12000000, 50000, 'Седан', 'images/toyota_camry.jpg'),
('Kia', 'Sportage', 15000000, 30000, 'Кроссовер', 'images/kia_sportage.jpg'),
('Hyundai', 'Elantra', 10000000, 20000, 'Седан', 'images/hyundai_elantra.jpg');
""")

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Данные успешно добавлены!")
