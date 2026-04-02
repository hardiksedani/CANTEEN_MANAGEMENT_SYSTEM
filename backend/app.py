from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import random
import string

app = Flask(__name__)
app.secret_key = 'canteen_secret_key_2024'
CORS(app, supports_credentials=True)

# ─── DB CONFIG (XAMPP defaults) ───────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',        # XAMPP default: empty
    'database': 'canteen_db',
    'port': 3306
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def gen_order_number():
    return 'ORD' + ''.join(random.choices(string.digits, k=6))

# ─── AUTH ROUTES ──────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    db.close()
    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        return jsonify({'success': True, 'user': {
            'id': user['id'], 'name': user['name'],
            'email': user['email'], 'role': user['role'],
            'wallet_balance': float(user['wallet_balance'] or 0)
        }})
    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email=%s", (data['email'],))
    if cur.fetchone():
        db.close()
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    cur.execute(
        "INSERT INTO users (name, email, password, role, student_id, phone) VALUES (%s,%s,%s,'student',%s,%s)",
        (data['name'], data['email'], data['password'], data.get('student_id',''), data.get('phone',''))
    )
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Account created successfully!'})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ─── MENU ROUTES ──────────────────────────────────────

@app.route('/api/menu', methods=['GET'])
def get_menu():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM menu_items WHERE is_available=1 ORDER BY category, name")
    items = cur.fetchall()
    db.close()
    for item in items:
        item['price'] = float(item['price'])
    return jsonify({'success': True, 'items': items})

@app.route('/api/menu/all', methods=['GET'])
def get_menu_all():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM menu_items ORDER BY category, name")
    items = cur.fetchall()
    db.close()
    for item in items:
        item['price'] = float(item['price'])
    return jsonify({'success': True, 'items': items})

@app.route('/api/menu/add', methods=['POST'])
def add_menu_item():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO menu_items (name, category, price, description, image_emoji) VALUES (%s,%s,%s,%s,%s)",
        (data['name'], data['category'], data['price'], data.get('description',''), data.get('image_emoji','🍽️'))
    )
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Item added!'})

@app.route('/api/menu/update/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE menu_items SET name=%s, category=%s, price=%s, description=%s, is_available=%s WHERE id=%s",
        (data['name'], data['category'], data['price'], data.get('description',''), data.get('is_available',1), item_id)
    )
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Item updated!'})

@app.route('/api/menu/delete/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Item deleted!'})

# ─── ORDER ROUTES ─────────────────────────────────────

@app.route('/api/orders/place', methods=['POST'])
def place_order():
    data = request.json
    user_id = data['user_id']
    items = data['items']   # [{menu_item_id, quantity, unit_price, item_name}]
    total = sum(i['unit_price'] * i['quantity'] for i in items)
    order_num = gen_order_number()
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "INSERT INTO orders (order_number, user_id, customer_name, total_amount, payment_method, notes) VALUES (%s,%s,%s,%s,%s,%s)",
        (order_num, user_id, data.get('customer_name',''), total, data.get('payment_method','cash'), data.get('notes',''))
    )
    order_id = cur.lastrowid
    for item in items:
        subtotal = item['unit_price'] * item['quantity']
        cur.execute(
            "INSERT INTO order_items (order_id, menu_item_id, item_name, quantity, unit_price, subtotal) VALUES (%s,%s,%s,%s,%s,%s)",
            (order_id, item['menu_item_id'], item['item_name'], item['quantity'], item['unit_price'], subtotal)
        )
    db.commit()
    db.close()
    return jsonify({'success': True, 'order_number': order_num, 'order_id': order_id})

@app.route('/api/orders/my/<int:user_id>', methods=['GET'])
def my_orders(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM orders WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    orders = cur.fetchall()
    for o in orders:
        o['total_amount'] = float(o['total_amount'])
        o['created_at'] = str(o['created_at'])
        o['updated_at'] = str(o['updated_at'])
        cur.execute("SELECT * FROM order_items WHERE order_id=%s", (o['id'],))
        items = cur.fetchall()
        for it in items:
            it['unit_price'] = float(it['unit_price'])
            it['subtotal'] = float(it['subtotal'])
        o['items'] = items
    db.close()
    return jsonify({'success': True, 'orders': orders})

@app.route('/api/orders/all', methods=['GET'])
def all_orders():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT o.*, u.name as student_name, u.student_id
        FROM orders o LEFT JOIN users u ON o.user_id=u.id
        ORDER BY o.created_at DESC
    """)
    orders = cur.fetchall()
    for o in orders:
        o['total_amount'] = float(o['total_amount'])
        o['created_at'] = str(o['created_at'])
        o['updated_at'] = str(o['updated_at'])
        cur.execute("SELECT * FROM order_items WHERE order_id=%s", (o['id'],))
        items = cur.fetchall()
        for it in items:
            it['unit_price'] = float(it['unit_price'])
            it['subtotal'] = float(it['subtotal'])
        o['items'] = items
    db.close()
    return jsonify({'success': True, 'orders': orders})

@app.route('/api/orders/active', methods=['GET'])
def active_orders():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT o.*, u.name as student_name, u.student_id
        FROM orders o LEFT JOIN users u ON o.user_id=u.id
        WHERE o.status NOT IN ('delivered','cancelled')
        ORDER BY o.created_at ASC
    """)
    orders = cur.fetchall()
    for o in orders:
        o['total_amount'] = float(o['total_amount'])
        o['created_at'] = str(o['created_at'])
        o['updated_at'] = str(o['updated_at'])
        cur.execute("SELECT * FROM order_items WHERE order_id=%s", (o['id'],))
        items = cur.fetchall()
        for it in items:
            it['unit_price'] = float(it['unit_price'])
            it['subtotal'] = float(it['subtotal'])
        o['items'] = items
    db.close()
    return jsonify({'success': True, 'orders': orders})

@app.route('/api/orders/status/<int:order_id>', methods=['PUT'])
def update_status(order_id):
    data = request.json
    status = data.get('status')
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': f'Order marked as {status}'})

# ─── DASHBOARD STATS ──────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as total FROM orders")
    total_orders = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM orders WHERE status='delivered'")
    delivered = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM orders WHERE status NOT IN ('delivered','cancelled')")
    active = cur.fetchone()['total']
    cur.execute("SELECT COALESCE(SUM(total_amount),0) as revenue FROM orders WHERE status='delivered'")
    revenue = float(cur.fetchone()['revenue'])
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='student'")
    students = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM menu_items WHERE is_available=1")
    menu_count = cur.fetchone()['total']
    db.close()
    return jsonify({'success': True, 'stats': {
        'total_orders': total_orders,
        'delivered': delivered,
        'active': active,
        'revenue': revenue,
        'students': students,
        'menu_count': menu_count
    }})

if __name__ == '__main__':
    print("🚀 Canteen System Backend running at http://localhost:5000")
    app.run(debug=True, port=5000)
