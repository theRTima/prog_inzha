import psycopg2

def test_direct():
    try:
        # Прямое подключение через psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="restaurant_db", 
            user="restaurant_user",
            password="restaurant_pass"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        print(f"✓ Прямое подключение работает: {cursor.fetchone()}")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Ошибка прямого подключения: {e}")
        return False

if __name__ == "__main__":
    test_direct()