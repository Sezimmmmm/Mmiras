import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу cars
cursor.execute('''
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    price INTEGER,
    mileage INTEGER,
    body_type TEXT,
    image TEXT
)
''')

# Вставляем данные
cursor.executemany('''
INSERT INTO cars (brand, model, price, mileage, body_type, image)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('Toyota', 'Camry', 12000000, 50000, 'Седан', 'images/toyota_camry.jpg'),
    ('Kia', 'Sportage', 15000000, 30000, 'Кроссовер', 'images/kia_sportage.jpg'),
    ('Hyundai', 'Elantra', 10000000, 20000, 'Седан', 'images/hyundai_elantra.jpg')
])

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных успешно создана и данные добавлены!")
