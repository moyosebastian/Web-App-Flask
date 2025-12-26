

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'TUD'   

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_sales'
}

def get_db():
    return mysql.connector.connect(**db_config)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/welcome_page')
def welcome_page():
    return render_template('welcome.html', username=session.get('user'))


@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user'] = username
        return "success"
    else:
        return "Fail"


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        flash("Account created! Please login.")
    except Exception as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('login'))


@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session['user'])


@app.route('/cars')
def cars():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cars.html', cars=cars)


@app.route('/add_car', methods=['POST'])
def add_car():
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    damage = request.form['damage']
    price = request.form['price']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO cars (brand, model, year, damage, price) VALUES (%s,%s,%s,%s,%s)",
                   (brand, model, year, damage, price))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('cars'))


@app.route('/delete_car/<int:id>')
def delete_car(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('cars'))


@app.route('/update_car/<int:id>', methods=['POST'])
def update_car(id):
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    damage = request.form['damage']
    price = request.form['price']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cars SET brand=%s, model=%s, year=%s, damage=%s, price=%s WHERE id=%s",
                   (brand, model, year, damage, price, id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('cars'))


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/get_stats', methods=['GET'])
def get_stats():

    db = get_db() 
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cars")
    cars_data = cursor.fetchall()
    cursor.close() 
    db.close()

    df = pd.DataFrame(cars_data, columns=['id', 'brand', 'model', 'year', 'damage', 'price'])


    avg_price = float(np.round(df['price'].mean(), 2)) if not df.empty else 0

    count_cars = len(df)

    return {
        "avg_price": avg_price,
        "cars_count": count_cars
    }


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)



    
    




