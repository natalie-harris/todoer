import mysql.connector
import os
from dotenv import load_dotenv

def init_db():
    load_dotenv()
    address = os.getenv("DB_ADDRESS")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    table = os.getenv("DB_TABLE", "todos")

    conn = mysql.connector.connect(host=address, password=password, user=username, database=database)
    cursor = conn.cursor()

    try:
        conn = mysql.connector.connect(
            host=address, 
            password=password, 
            user=username, 
            database=database
        )
        cursor = conn.cursor()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            description VARCHAR(255) NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            finished TINYINT(1) DEFAULT 0
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Таблица '{table}' успешно создана или уже существует.")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()