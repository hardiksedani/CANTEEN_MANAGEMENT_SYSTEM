-- ============================================
-- CANTEEN MANAGEMENT SYSTEM - DATABASE SETUP
-- Import this in phpMyAdmin (XAMPP)
-- ============================================

CREATE DATABASE IF NOT EXISTS canteen_db;
USE canteen_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student','staff','manager') DEFAULT 'student',
    student_id VARCHAR(20),
    phone VARCHAR(15),
    wallet_balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    description TEXT,
    is_available TINYINT(1) DEFAULT 1,
    image_emoji VARCHAR(10) DEFAULT '🍽️',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    customer_name VARCHAR(100),
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash','wallet') DEFAULT 'cash',
    status ENUM('pending','preparing','ready','delivered','cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(8,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- Sample Users (password: password123)
INSERT INTO users (name, email, password, role, student_id, wallet_balance) VALUES
('Manager Admin', 'manager@canteen.com', 'password123', 'manager', NULL, 0),
('Staff Member', 'staff@canteen.com', 'password123', 'staff', NULL, 0),
('Aarav Sharma', 'student@canteen.com', 'password123', 'student', 'STU001', 500.00),
('Priya Patel', 'priya@canteen.com', 'password123', 'student', 'STU002', 250.00);

-- Sample Menu Items
INSERT INTO menu_items (name, category, price, description, image_emoji) VALUES
('Masala Dosa', 'South Indian', 45.00, 'Crispy dosa with spicy potato filling and chutney', '🫓'),
('Idli Sambar', 'South Indian', 30.00, '3 soft idlis with hot sambar and coconut chutney', '🍚'),
('Vada Pav', 'Snacks', 20.00, 'Mumbai style vada pav with green chutney', '🍔'),
('Pav Bhaji', 'Snacks', 55.00, 'Spicy bhaji with butter pav', '🫕'),
('Paneer Rice', 'Main Course', 80.00, 'Fragrant rice with paneer curry', '🍛'),
('Dal Rice', 'Main Course', 60.00, 'Yellow dal with steamed rice and pickle', '🍲'),
('Chapati Sabzi', 'Main Course', 50.00, '3 chapatis with seasonal vegetable curry', '🫓'),
('Samosa (2 pcs)', 'Snacks', 25.00, 'Crispy samosas with green chutney', '🥟'),
('Cold Coffee', 'Beverages', 35.00, 'Chilled coffee with milk', '☕'),
('Masala Chai', 'Beverages', 15.00, 'Hot spiced tea', '🍵'),
('Fresh Lime Soda', 'Beverages', 25.00, 'Refreshing lime soda', '🥤'),
('Fruit Salad', 'Healthy', 40.00, 'Mixed seasonal fruits with honey', '🥗'),
('Gulab Jamun (2)', 'Desserts', 30.00, 'Soft gulab jamun in sugar syrup', '🍮'),
('Ice Cream', 'Desserts', 40.00, 'Vanilla / Chocolate / Strawberry', '🍨'),
('Sandwich', 'Snacks', 40.00, 'Grilled veg sandwich with cheese', '🥪');
