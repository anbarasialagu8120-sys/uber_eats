import streamlit as st

def show_business_questions(conn):

    st.header("📊 Business Analysis")

    query = """
    SELECT restaurant_name,
    COUNT(order_id) AS total_orders
    FROM orders
    GROUP BY restaurant_name
    ORDER BY total_orders DESC
    LIMIT 10;
    """

    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()

    st.table(data)