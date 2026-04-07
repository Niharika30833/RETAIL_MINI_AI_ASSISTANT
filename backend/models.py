from database import cursor, conn

def add_product(name, price, stock):
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()

def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()