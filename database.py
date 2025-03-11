import sqlite3

def create_items_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Items (
            item_id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER,
            stock INTEGER
        )''')
    conn.commit()
    conn.close()
create_items_table()

def create_employees_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contact_no INTEGER UNIQUE,
            nic TEXT UNIQUE,
            role TEXT,
            user_name TEXT,
            password TEXT
        )''')
    conn.commit()
    conn.close()
create_employees_table()

def create_shops_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Shops (
            shop_id INTEGER PRIMARY KEY,
            name TEXT,
            contact_num INTEGER,
            address TEXT,
            worker_id TEXT UNIQUE,
            FOREIGN KEY (worker_id) REFERENCES Employees(id)
        )''')
    conn.commit()
    conn.close()
create_shops_table()

def create_orders_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            shop_name TEXT,
            item_id INTEGER,
            item_name VARCHAR,
            total_price INTEGER,
            net_total INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY (shop_name) REFERENCES Shops(name),
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        )
    ''')
    conn.commit()
    conn.close()
create_orders_table()

def create_bills_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bills (
            id INTEGER PRIMARY KEY,
            bill_id INTEGER,
            shop_name TEXT,
            customer_name TEXT,
            customer_mobile_number INTEGER,
            bill_date TEXT,
            bill_time TEXT,
            billing_emp_name TEXT,
            item_id INTEGER,
            item_name TEXT,
            item_price INTEGER,
            quantity INTEGER,
            total_price INTEGER,
            net_total INTEGER,
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        )
    ''')
    conn.commit()
    conn.close()
create_bills_table()