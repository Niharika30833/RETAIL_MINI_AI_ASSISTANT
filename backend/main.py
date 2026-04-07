from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import add_product, get_products
from chatbot import chatbot_response
from database import cursor

app = FastAPI()

# ✅ CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ HOME ROUTE
@app.get("/")
def home():
    return {"message": "Retail Chatbot Running"}


# ✅ CHATBOT ROUTE
@app.get("/chat/")
def chat(query: str):
    return {"response": chatbot_response(query)}


# ✅ GET ALL PRODUCTS (Inventory)
@app.get("/products/")
def products():
    return get_products()


# ✅ SALES SUMMARY (TOTAL)
@app.get("/sales/")
def sales():
    cursor.execute("SELECT SUM(revenue) FROM sales")
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(quantity_sold) FROM sales")
    items = cursor.fetchone()[0] or 0

    return {
        "total_revenue": total,
        "items_sold": items
    }


# ✅ SALES BY YEAR (FOR GRAPH 📊)
@app.get("/sales-by-year/")
def sales_by_year(year: int):
    cursor.execute("""
    SELECT product_name, revenue 
    FROM sales 
    WHERE year=?
    """, (year,))

    data = cursor.fetchall()

    return data


# ✅ PRODUCT ANALYSIS (BEST PRODUCT)
@app.get("/analysis/")
def analysis():
    cursor.execute("""
    SELECT product_name, SUM(revenue) as total
    FROM sales
    GROUP BY product_name
    ORDER BY total DESC
    """)

    data = cursor.fetchall()
    return data