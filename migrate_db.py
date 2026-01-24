import sqlite3
import os

db_path = os.path.join('instance', 'optimEat.db')
if not os.path.exists(db_path):
    print("DB not found")
    exit()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE business ADD COLUMN needs TEXT")
    conn.commit()
    print("Successfully added 'needs' column to Business table.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
