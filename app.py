from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure key

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stockDB"]
collection = db["stocks"]
admin_collection = db["admins"]

# Authentication check
def is_logged_in():
    return 'admin' in session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = admin_collection.find_one({'username': username})
        if admin and check_password_hash(admin['password'], password):
            session['admin'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    query = {}
    # ... your query logic ...

    stocks = list(collection.find(query))
    stock_names = [s['name'] for s in stocks]
    stock_quantities = [s['quantity'] for s in stocks]
    stock_prices = [s['price'] for s in stocks]

    return render_template('index.html', stocks=stocks,
                           stock_names=stock_names,
                           stock_quantities=stock_quantities,
                           stock_prices=stock_prices,
                           logged_in=is_logged_in())

@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        collection.insert_one({'name': name, 'quantity': quantity, 'price': price})
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<stock_id>', methods=['GET', 'POST'])
def update_stock(stock_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    stock = collection.find_one({'_id': ObjectId(stock_id)})
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        collection.update_one({'_id': ObjectId(stock_id)}, {'$set': {
            'name': name, 'quantity': quantity, 'price': price
        }})
        return redirect(url_for('index'))
    return render_template('update.html', stock=stock)

@app.route('/delete/<stock_id>', methods=['POST'])
def delete_stock(stock_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    collection.delete_one({'_id': ObjectId(stock_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
