from database import cursor
import re

def chatbot_response(user_input):
    user_input = user_input.lower()

    # 🔍 Extract year (like 2023, 2024)
    year_match = re.search(r'\b(20\d{2})\b', user_input)
    year = int(year_match.group()) if year_match else None

    # 🔍 Detect product
    product = None
    if "laptop" in user_input:
        product = "Laptop"
    elif "mobile" in user_input:
        product = "Mobile"
    elif "headphones" in user_input:
        product = "Headphones"

    # ✅ CASE 1: SALES BY YEAR (NO PRODUCT)
    if "sales" in user_input and year and not product:
        cursor.execute("SELECT SUM(revenue) FROM sales WHERE year=?", (year,))
        total = cursor.fetchone()[0]

        if total:
            return f"Total sales in {year} = ₹{total}"
        else:
            return f"No sales data found for {year}"

    # ✅ CASE 2: SALES BY PRODUCT + YEAR
    if "sales" in user_input and product and year:
        cursor.execute(
            "SELECT revenue FROM sales WHERE product_name=? AND year=?",
            (product, year)
        )
        result = cursor.fetchone()

        if result:
            return f"{product} sales in {year} = ₹{result[0]}"
        else:
            return f"No data found for {product} in {year}"

    # ✅ CASE 3: TOTAL SALES
    if "total sales" in user_input:
        cursor.execute("SELECT SUM(revenue) FROM sales")
        total = cursor.fetchone()[0]
        return f"Total sales = ₹{total}"

    # ✅ CASE 4: BEST PRODUCT
    if "best" in user_input:
        cursor.execute("""
        SELECT product_name, SUM(revenue) as total
        FROM sales
        GROUP BY product_name
        ORDER BY total DESC LIMIT 1
        """)
        result = cursor.fetchone()
        return f"Best selling product is {result[0]} with ₹{result[1]} sales"

    # ✅ GREETING
    if "hi" in user_input or "hello" in user_input:
        return "Hello! Ask me about sales, products, or analytics 📊"

    return "Try asking like: 'sales in 2024' or 'laptop sales 2024'"