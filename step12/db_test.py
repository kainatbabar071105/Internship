import psycopg2
from psycopg2.extras import RealDictCursor

# Your PostgreSQL configuration
DB_CONFIG = {
    "dbname": "db",
    "user": "postgres",
    "password": "xeven",
    "host": "localhost",
    "port": "5432"
}

def run_db_operations():
    try:
        # 1. Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        # 2. Insert one record into the table
        insert_query = "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING *;"
        cursor.execute(insert_query, ("Wireless Mouse", 25.99))
        
        # Commit the transaction to save changes in PostgreSQL
        conn.commit()
        print("Record inserted successfully!")

        # 3. Fetch all records using the cursor
        cursor.execute("SELECT * FROM items;")
        records = cursor.fetchall()

        # 4. Print the result in the terminal
        print("\n--- Current Database Records ---")
        for row in records:
            print(dict(row))

        # Close cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    run_db_operations()