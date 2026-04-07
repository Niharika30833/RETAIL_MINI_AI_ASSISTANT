import sqlite3

# Connection
conn = sqlite3.connect("retail.db", check_same_thread=False)
cursor = conn.cursor()

# PRODUCTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock INTEGER,
    sold INTEGER DEFAULT 0
)
""")

# SALES TABLE (NEW)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    year INTEGER,
    quantity_sold INTEGER,
    revenue REAL
)
""")

conn.commit()


# ✅ INSERT SALES DATA (ADD HERE)
def insert_sales_data():
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        data = [
            ("Laptop", 2023, 5, 250000),
            ("Laptop", 2024, 8, 400000),
            ("Mobile", 2023, 10, 200000),
            ("Mobile", 2024, 15, 300000),
            ("Headphones", 2023, 20, 40000),
            ("Headphones", 2024, 30, 60000),
        ]

        cursor.executemany(
            "INSERT INTO sales (product_name, year, quantity_sold, revenue) VALUES (?, ?, ?, ?)",
            data
        )
        conn.commit()


# ✅ CALL FUNCTION (VERY IMPORTANT)
insert_sales_data()