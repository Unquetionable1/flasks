from flask import Flask, render_template, request, redirect, flash, url_for
from sqlite3 import connect

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'

def init_db():
    con = connect('db/sms_database.db')
    cur = con.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    '''
    cur.execute(sql)
    con.commit()
    con.close()

@app.route('/')
def index():
    return redirect(url_for('view_products'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        con = connect('db/sms_database.db')
        cur = con.cursor()
        cur.execute('INSERT INTO products(name, price) VALUES (?, ?)', (name, price))
        con.commit()
        con.close()
        flash('Product added successfully', 'success')
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    con = connect('db/sms_database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        cur.execute('UPDATE products SET name=?, price=? WHERE id=?', (name, price, product_id))
        con.commit()
        con.close()
        flash('Product updated successfully', 'success')
        return redirect(url_for('view_products'))
    return render_template('update_product.html', product={'id': product[0], 'name': product[1], 'price': product[2]})

@app.route('/products')
def view_products():
    con = connect('db/sms_database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    con.close()
    return render_template('view_products.html', products=[{'id': row[0], 'name': row[1], 'price': row[2]} for row in products])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
