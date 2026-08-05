from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="FastAPI + PostgreSQL Integration")

# Database connection details (Update password/database name if needed)
DB_CONFIG = {
    "dbname": "db",
    "user": "postgres",
    "password": "xeven",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

class Item(BaseModel):
    name: str
    price: float

@app.on_event("startup")
def startup_db():
    """Automatically creates the items table on app startup if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is connected to PostgreSQL!"}

@app.get("/items")
def get_all_items():
    """Fetches all items stored in PostgreSQL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items;")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

@app.post("/items")
def create_item(item: Item):
    """Inserts a new item into PostgreSQL and returns the created record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING *;",
        (item.name, item.price)
    )
    new_item = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return new_item