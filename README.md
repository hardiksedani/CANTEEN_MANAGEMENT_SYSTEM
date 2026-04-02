# 🍴 College Canteen Management System
## Full Stack: Python Flask + Tailwind CSS + MySQL (XAMPP)

---

## 📁 Project Structure

```
canteen_system/
├── backend/
│   ├── app.py              ← Flask API server
│   └── requirements.txt    ← Python packages
├── frontend/
│   ├── login.html          ← Login & Register
│   ├── student.html        ← Student: Menu + Cart + Orders
│   ├── staff.html          ← Staff: View & Deliver Orders
│   └── manager.html        ← Manager: Dashboard + Full Control
├── canteen_db.sql          ← Database setup
└── README.md
```

---

## ✅ STEP-BY-STEP SETUP

### STEP 1 — Start XAMPP
1. Open **XAMPP Control Panel**
2. Start **Apache** ✅
3. Start **MySQL** ✅

> ⚠️ If MySQL won't start:
> - Open Task Manager → find any `mysqld.exe` → End Task
> - Go to `C:\xampp\mysql\data\` → delete any `.err` files and `ibdata1.lock`
> - Start MySQL again

---

### STEP 2 — Create the Database
1. Open your browser → go to: **http://localhost/phpmyadmin**
2. Click **Import** tab (top menu)
3. Click **Choose File** → select `canteen_db.sql` from this project
4. Click **Go** at the bottom

✅ Database `canteen_db` with all tables and sample data is now ready.

---

### STEP 3 — Install Python Packages
Open VS Code terminal (Ctrl + `) and run:

```bash
cd backend
pip install flask flask-cors mysql-connector-python
```

---

### STEP 4 — Start the Flask Backend
In VS Code terminal:

```bash
cd backend
python app.py
```

You should see:
```
🚀 Canteen System Backend running at http://localhost:5000
```

Keep this terminal running!

---

### STEP 5 — Open the Website
Open the `frontend` folder in VS Code.

Install the **Live Server** extension in VS Code if you don't have it.

Right-click on `login.html` → **Open with Live Server**

OR just open `frontend/login.html` directly in your browser.

---

## 🔐 Login Accounts

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Manager | manager@canteen.com    | password123 |
| Staff   | staff@canteen.com      | password123 |
| Student | student@canteen.com    | password123 |

---

## 👤 What Each Role Can Do

### 🎓 Student
- Browse full menu with categories & search
- Add items to cart, change quantity
- Place orders (cash / wallet)
- Add special instructions
- Track order status in real-time

### 👨‍🍳 Staff
- See all active incoming orders (live, auto-refreshes every 15 sec)
- Move orders: Pending → Preparing → Ready → Delivered
- Cancel orders
- Filter by status

### 👨‍💼 Manager
- Full dashboard with stats (orders, revenue, students, menu items)
- See ALL orders with full history table
- Update any order status
- Add / Edit / Delete menu items
- Toggle item availability

---

## 🔧 Troubleshooting

### "Cannot connect to server" error on login page
→ Make sure `python app.py` is running in the backend folder

### MySQL connection error in Flask
→ Check XAMPP MySQL is started
→ Open `backend/app.py` and confirm:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',     # empty by default in XAMPP
    'database': 'canteen_db',
}
```

### Database not found error
→ Go to phpMyAdmin and re-import `canteen_db.sql`

### Port already in use
→ Change port in `app.py`: `app.run(debug=True, port=5001)`
→ Then update `const API = 'http://localhost:5001/api'` in all HTML files

---

## 🌐 Share on College WiFi

1. Find your IP: Open CMD → type `ipconfig` → note IPv4 address (e.g. `192.168.1.5`)
2. In `backend/app.py` change last line to: `app.run(debug=True, host='0.0.0.0', port=5000)`
3. Update `const API` in all 3 HTML files to: `http://192.168.1.5:5000/api`
4. Share `http://192.168.1.5/canteen/login.html` (put frontend in htdocs)

---

Built with ❤️ using Python Flask + Tailwind CSS + MySQL
