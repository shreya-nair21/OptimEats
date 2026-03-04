import sqlite3
import os

db_path = os.path.join('instance', 'optimEat.db')
if not os.path.exists(db_path):
    print("DB not found")
    exit()

def migrate():
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add google_id to Business
        try:
            cursor.execute("ALTER TABLE business ADD COLUMN google_id TEXT UNIQUE")
            print("Successfully added 'google_id' column to Business table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("'google_id' already exists in Business table.")
            else:
                print(f"Error adding to Business: {e}")

        # Add google_id to User
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN google_id TEXT UNIQUE")
            print("Successfully added 'google_id' column to User table.")
        except sqlite3.OperationalError as e:
             if "duplicate column name" in str(e).lower():
                print("'google_id' already exists in User table.")
             else:
                print(f"Error adding to User: {e}")

        conn.commit()
    except Exception as e:
        print(f"Fatal Error during migration: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    migrate()
