import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('user_lists.db')
        print("Подключение к SQLite успешно")
        return conn
    except Error as e:
        print(f"Ошибка подключения: {e}")
    return conn

def init_db():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_lists (
                user_id INTEGER PRIMARY KEY,
                items TEXT  
            )
        ''')
            conn.commit()
            print("Таблица создана")
        except Error as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            conn.close()
    
def save_user_list(user_id: int, items: list):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            items_str = ", ".join(items)
            cursor.execute(
                "REPLACE INTO user_lists (user_id, items) VALUES (?, ?)",
                (user_id, items_str)
            )
            conn.commit()
            print(f"Список для user_id={user_id} сохранён")
        except Error as e:
            print(f"Ошибка при сохранении: {e}")
        finally:
            conn.close()

def get_user_list(user_id: int) -> list:
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT items FROM user_lists WHERE user_id = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return result[0].split(", ")
            return []
        except Error as e:
            print(f"Ошибка при чтении: {e}")
            return []
        finally:
            conn.close()

init_db()