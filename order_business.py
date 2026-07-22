import streamlit as st
import pandas as pd


def show_order_analysis(conn):

    st.header("📦 Order JSON Analysis")

    question = st.selectbox(
        "Select Order Business Question",
        [
            "Total Orders",
            "Total Revenue",
            "Average Order Value",
            "Payment Method Wise Orders",
            "Discount Usage",
            "Top 10 Revenue Restaurants",
            "Top 10 Ordered Restaurants"
        ]
    )


    # 1 Total Orders
    if question == "Total Orders":

        query = """
        SELECT COUNT(*) AS total_orders
        FROM orders;
        """

        df = pd.read_sql(query, conn)

        st.metric(
            "Total Orders",
            df.iloc[0]["total_orders"]
        )


    # 2 Total Revenue
    elif question == "Total Revenue":

        query = """
        SELECT SUM(order_value) AS total_revenue
        FROM orders;
        """

        df = pd.read_sql(query, conn)

        st.metric(
            "Total Revenue",
            df.iloc[0]["total_revenue"]
        )


    # 3 Average Order Value
    elif question == "Average Order Value":

        query = """
        SELECT AVG(order_value) AS average_order_value
        FROM orders;
        """

        df = pd.read_sql(query, conn)

        st.metric(
            "Average Order Value",
            round(df.iloc[0]["average_order_value"],2)
        )


    # 4 Payment Method Wise Orders
    elif question == "Payment Method Wise Orders":

        query = """
        SELECT 
            payment_method,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY payment_method;
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        st.bar_chart(
            df.set_index("payment_method")
        )


    # 5 Discount Usage
    elif question == "Discount Usage":

        query = """
        SELECT
            discount_used,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY discount_used;
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)


    # 6 Top Revenue Restaurants
    elif question == "Top 10 Revenue Restaurants":

        query = """
        SELECT
            restaurant_name,
            SUM(order_value) AS total_revenue
        FROM orders
        GROUP BY restaurant_name
        ORDER BY total_revenue DESC
        LIMIT 10;
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        st.bar_chart(
            df.set_index("restaurant_name")
        )


    # 7 Top Ordered Restaurants
    elif question == "Top 10 Ordered Restaurants":

        query = """
        SELECT
            restaurant_name,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY restaurant_name
        ORDER BY total_orders DESC
        LIMIT 10;
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        st.bar_chart(
            df.set_index("restaurant_name")
        )