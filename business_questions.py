import streamlit as st
import pandas as pd

def show_business_questions(conn):

    st.header("📊 Business Questions")

    question = st.selectbox(
        "Select a Business Question",
        [
            "Q1 - Highest Average Restaurant Ratings by Location",
            "Q2 - Over-Saturated Locations",
            "Q3 - Does Online Ordering Improve Ratings?",
            "Q4 - Does Table Booking Improve Ratings?",
            "Q5 - Best Price Range by Customer Satisfaction",
            "Q6 - Most Common Cuisines",
            "Q7 - Highest Rated Cuisines",
            "Q8 - Restaurants with Highest Votes",
            "Q9 - Locations with Highest Number of Restaurants",
            "Q10 - Online Ordering Availability"
        ]
    )

    if question == "Q1 - Highest Average Restaurant Ratings by Location":

        query = """
        SELECT
            location,
            ROUND(AVG(rate),2) AS average_rating,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY location
        HAVING COUNT(*) >= 5
        ORDER BY average_rating DESC;
        """

    elif question == "Q2 - Over-Saturated Locations":

        query = """
        SELECT
            location,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY location
        ORDER BY total_restaurants DESC;
        """

    elif question == "Q3 - Does Online Ordering Improve Ratings?":

        query = """
        SELECT
            online_order,
            ROUND(AVG(rate),2) AS average_rating,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY online_order
        ORDER BY average_rating DESC;
        """

    elif question == "Q4 - Does Table Booking Improve Ratings?":

        query = """
        SELECT
            book_table,
            ROUND(AVG(rate),2) AS average_rating,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY book_table
        ORDER BY average_rating DESC;
        """

    elif question == "Q5 - Best Price Range by Customer Satisfaction":

        query = """
        SELECT
            CASE
                WHEN approx_cost_for_two < 500 THEN 'Low Price'
                WHEN approx_cost_for_two BETWEEN 500 AND 1000 THEN 'Mid Price'
                ELSE 'Premium'
            END AS price_range,
            ROUND(AVG(rate),2) AS average_rating,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY price_range
        ORDER BY average_rating DESC;
        """

    elif question == "Q6 - Most Common Cuisines":

        query = """
        SELECT
            cuisines,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY cuisines
        ORDER BY total_restaurants DESC
        LIMIT 10;
        """

    elif question == "Q7 - Highest Rated Cuisines":

        query = """
        SELECT
            cuisines,
            ROUND(AVG(rate),2) AS average_rating,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY cuisines
        HAVING COUNT(*) >= 5
        ORDER BY average_rating DESC
        LIMIT 10;
        """

    elif question == "Q8 - Restaurants with Highest Votes":

        query = """
        SELECT
            name,
            votes,
            cuisines,
            location
        FROM restaurants
        ORDER BY votes DESC
        LIMIT 10;
        """

    elif question == "Q9 - Locations with Highest Number of Restaurants":

        query = """
        SELECT
            location,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY location
        ORDER BY total_restaurants DESC
        LIMIT 10;
        """

    elif question == "Q10 - Online Ordering Availability":

        query = """
        SELECT
            online_order,
            COUNT(*) AS total_restaurants
        FROM restaurants
        GROUP BY online_order;
        """

    df = pd.read_sql(query, conn)

    st.dataframe(df, use_container_width=True)