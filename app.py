import os
from flask import Flask, render_template, request, redirect, jsonify, session, flash
from werkzeug.utils import secure_filename
import sqlite3
import requests
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

VIN_API_URL = 'https://api.vindecoder.eu/3.2'  # Замените на реальный URL API
VIN_API_KEY = '7aea53a4aef8'  # Замените на ваш API-ключ

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создаём таблицу test_drive_requests, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_drive_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            car_id INTEGER NOT NULL,
            FOREIGN KEY (car_id) REFERENCES cars (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog', endpoint='catalog')
def catalog():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return render_template('catalog.html', cars=cars)

@app.route('/car/<int:car_id>', endpoint='car_details')
def car_details(car_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    car = cursor.fetchone()
    conn.close()
    return render_template('car_details.html', car=car)

@app.route('/compare', methods=['GET'], endpoint='compare')
def compare():
    car_ids = request.args.getlist('car_ids')  # Получаем список ID автомобилей из параметров запроса
    if not car_ids:
        return render_template('compare.html', cars=[])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM cars WHERE id IN ({','.join('?' for _ in car_ids)})"
    cursor.execute(query, car_ids)
    cars = cursor.fetchall()
    conn.close()
    return render_template('compare.html', cars=cars)

@app.route('/credit_calc', methods=['GET', 'POST'], endpoint='credit_calc')
def credit_calc():
    monthly_payment = None
    if request.method == 'POST':
        price = float(request.form['price'])
        down_payment = float(request.form['down_payment'])
        term = int(request.form['term'])
        loan_amount = price - down_payment
        interest_rate = 0.1  # 10% годовых
        monthly_payment = (loan_amount * (interest_rate / 12)) / (1 - (1 + interest_rate / 12) ** -term)
    return render_template('credit_calc.html', monthly_payment=monthly_payment)

@app.route('/trade_in', methods=['GET', 'POST'], endpoint='trade_in')
def trade_in():
    estimated_price = None
    vin_data = None
    if request.method == 'POST':
        vin = request.form['vin']
        mileage = int(request.form['mileage'])
        
        # Запрос к VIN API
        try:
            response = requests.get(
                f"{VIN_API_URL}/{vin}",
                headers={'Authorization': f'Bearer {VIN_API_KEY}'},
                params={'secret': '1706897c5d'}  # Добавляем секретный ключ
            )
            if response.status_code == 200:
                vin_data = response.json()
                base_price = vin_data.get('base_price', 1000000)  # Используем базовую цену из API
                depreciation = mileage * 10  # Уменьшение стоимости за пробег
                estimated_price = max(base_price - depreciation, 0)
            else:
                flash('Не удалось получить данные по VIN. Проверьте правильность VIN.', 'danger')
        except requests.exceptions.RequestException:
            flash('Ошибка при подключении к VIN API.', 'danger')
    
    return render_template('trade_in.html', estimated_price=estimated_price, vin_data=vin_data)

@app.route('/api/cars', methods=['GET'], endpoint='api_cars')
def api_cars():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()
    cars_list = [
        {
            "id": car[0],
            "brand": car[1],
            "model": car[2],
            "price": car[3],
            "mileage": car[4],
            "body_type": car[5],
            "image": car[6]
        }
        for car in cars
    ]
    return jsonify(cars_list)

@app.route('/test_drive', methods=['GET', 'POST'], endpoint='test_drive')
def test_drive():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        car_id = request.form['car_id']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO test_drive_requests (name, phone, car_id) VALUES (?, ?, ?)", (name, phone, car_id))
        conn.commit()
        conn.close()
        
        # Сообщение об успешной записи
        flash('Вы успешно записались на тест-драйв!', 'success')
        return redirect('/catalog')  # Перенаправление после успешной записи
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, brand, model FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return render_template('test_drive.html', cars=cars)

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Регистрация успешна! Войдите в систему.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Имя пользователя уже занято.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Вы успешно вошли в систему.', 'success')
            return redirect('/')
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html')

@app.route('/logout', endpoint='logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'info')
    return redirect('/')

@app.route('/update_database', methods=['POST'], endpoint='update_database')
def update_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Обновляем данные для Toyota Camry
    cursor.execute("UPDATE cars SET brand = 'Toyota', model = 'Camry 80' WHERE id = 1")

    # Обновляем данные для Hyundai Elantra
    cursor.execute("UPDATE cars SET brand = 'Hyundai', model = 'Elantra 70' WHERE id = 2")

    # Добавляем новую запись для Kia Optima
    cursor.execute("INSERT INTO cars (id, brand, model, price, mileage, body_type, image) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (5, 'Kia', 'Optima', 0, 0, 'Sedan', 'kia_optima.png'))

    # Добавляем новую запись для Hyundai Sonata
    cursor.execute("INSERT INTO cars (id, brand, model, price, mileage, body_type, image) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (6, 'Hyundai', 'Sonata', 0, 0, 'Sedan', 'hyundai_sonata.png'))

    conn.commit()
    conn.close()
    return "Database updated successfully!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
