import json
import mysql.connector
from datetime import datetime

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anbu@2703",
    database="uber_eats"
)

cursor = conn.cursor()

# Read JSON File
with open("orders2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Insert Query
query = """
INSERT IGNORE INTO orders
(order_id, restaurant_name, order_date, order_value, discount_used, payment_method)
VALUES (%s, %s, %s, %s, %s, %s)
"""

count = 0

for row in data:

    # Convert timestamp (milliseconds) to YYYY-MM-DD
    if isinstance(row["order_date"], (int, float)):
        order_date = datetime.fromtimestamp(
            row["order_date"] / 1000
        ).strftime("%Y-%m-%d")
    else:
        order_date = row["order_date"]

    cursor.execute(query, (
        row["order_id"],
        row["restaurant_name"],
        order_date,
        row["order_value"],
        row["discount_used"],
        row["payment_method"]
    ))

    count += cursor.rowcount

conn.commit()

print(f"{count} records inserted successfully!")

cursor.close()
conn.close()

print("JSON data imported into MySQL successfully!")