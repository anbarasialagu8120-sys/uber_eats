import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="#######",
        database="uber_eats"
    )
    return conn

if __name__ == "__main__":
    conn = get_connection()
    print("MySQL Connected Successfully!")
    conn.close()