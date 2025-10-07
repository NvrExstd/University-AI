from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

import re

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=current_dir)
app.secret_key = 'ЪУдйхйф214'  # Замените на случайный безопасный ключ

DATA_FILE = 'users.data'
KEY_FILE = 'secret.key'

def is_upper_cyrillic(password):
    # Проверяет, что пароль содержит только прописные кириллические буквы А-Я и Ё
    pattern = r'^[А-ЯЁ]+$'
    return re.match(pattern, password) is not None

# Создаем/загружаем ключ шифрования
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return key

key = load_key()
fernet = Fernet(key)

# Загрузка пользователей
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'rb') as f:
        encrypted_data = f.read()
    if not encrypted_data:
        return {}
    try:
        data = fernet.decrypt(encrypted_data).decode()
        return json.loads(data)
    except:
        return {}

# Сохранение пользователей
def save_users(users):
    data = json.dumps(users).encode()
    encrypted_data = fernet.encrypt(data)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted_data)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('resource'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username'].strip()
        if username in users:
            flash("Имя пользователя уже занято.", "danger")
            return redirect(url_for('register'))

        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash("Пароли не совпадают.", "danger")
            return redirect(url_for('register'))

        fullname = request.form['fullname'].strip()
        dob = request.form['dob']
        city = request.form['city'].strip()
        phone = request.form['phone'].strip()

        users[username] = {
            'fullname': fullname,
            'dob': dob,
            'city': city,
            'phone': phone,
            'password_hash': generate_password_hash(password)
        }
        save_users(users)
        flash("Регистрация прошла успешно, теперь войдите.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username'].strip()
        password = request.form['password']
        if username not in users:
            flash("Пользователь не найден.", "danger")
            return redirect(url_for('login'))
        if not check_password_hash(users[username]['password_hash'], password):
            flash("Неверный пароль.", "danger")
            return redirect(url_for('login'))
        session['username'] = username
        flash("Вход выполнен.", "success")
        return redirect(url_for('resource'))

    return render_template('login.html')

def contains_surname(password, surname):
    if not surname:
        return False
    pattern = re.escape(surname)
    return re.search(pattern, password, re.IGNORECASE) is not None

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        flash("Требуется войти.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        users = load_users()
        username = session['username']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_password_confirm = request.form['new_password_confirm']

        if not check_password_hash(users[username]['password_hash'], current_password):
            flash("Текущий пароль неверен.", "danger")
            return redirect(url_for('change_password'))

        if new_password != new_password_confirm:
            flash("Новые пароли не совпадают.", "danger")
            return redirect(url_for('change_password'))

        if len(new_password) < 11:
            flash("Пароль должен содержать не менее 11 символов.", "danger")
            return redirect(url_for('change_password'))

        if not is_upper_cyrillic(new_password):
            flash("Пароль должен содержать только ПРОПИСНЫЕ символы кириллицы.", "danger")
            return redirect(url_for('change_password'))

        fullname = users[username]['fullname']
        surname = fullname.split()[0] if fullname else ''

        if contains_surname(new_password, surname):
            flash("Пароль не должен содержать вашу фамилию.", "danger")
            return redirect(url_for('change_password'))

        users[username]['password_hash'] = generate_password_hash(new_password)
        save_users(users)
        flash("Пароль успешно изменён.", "success")
        return redirect(url_for('resource'))

    return render_template('change_password.html')


@app.route('/resource')
def resource():
    if 'username' not in session:
        flash("Доступ запрещён, требуется вход.", "danger")
        return redirect(url_for('login'))
    return render_template('resource.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
