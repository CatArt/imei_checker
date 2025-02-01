from sqlite3 import connect

# Инициализируем БД и в случае, если в ней отсутствует таблица, создаем ее
def init_db():
    with connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whitelist (
                user_id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()

# Функция добавляет в БД пользователя по UID.
def add_user_to_whitelist(user_id: int):
    with connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO whitelist (user_id) VALUES (?)", (user_id,))
        conn.commit()

# Проверяет пользователя на наличие в Whitelist
def is_user_whitelisted(user_id: int) -> bool:
    with connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM whitelist WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None