import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database/zomato.db")

#  Page switch
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Q&A"])

# DASHBOARD 
if page == "Dashboard":

    st.title("🍔 Zomato Restaurant Explorer✔✔")

    # Filters
    search = st.text_input("Search Restaurant")
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.0)

    locations = pd.read_sql("SELECT DISTINCT location FROM restaurants", conn)
    location_list = ["All"] + sorted(locations["location"].dropna().tolist())

    location = st.selectbox("Select Location", location_list)

    # SQL Query
    query = "SELECT name, rate, location FROM restaurants WHERE 1=1"

    if search:
        query += f" AND name LIKE '%{search}%'"

    query += f" AND rate >= {min_rating}"

    if location != "All":
        query += f" AND location = '{location}'"

    filtered_df = pd.read_sql(query, conn)

    st.subheader("Filtered Results")
    st.dataframe(filtered_df)

# question
if page == "Q&A":

    st.title("📊 Business Q&A Insights")

       #Highest avg rating locations

    if st.button("Top Rated Locations"):
        query = """
        SELECT location, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY location
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        result = pd.read_sql(query, conn)
        st.dataframe(result)

        #Over-saturated locations

    if st.button("Over-Saturated Locations"):
        query = """
        SELECT location, COUNT(*) as total_restaurants
        FROM restaurants
        GROUP BY location
        ORDER BY total_restaurants DESC
        LIMIT 10
        """
        result = pd.read_sql(query, conn)
        st.dataframe(result)
        
        #Online ordering impact


    if st.button("Online Order Impact"):
        query = """
        SELECT online_order, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY online_order
        """
        st.dataframe(pd.read_sql(query, conn))

       #Table booking impact


    if st.button("Table Booking Impact"):
        query = """
        SELECT book_table, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY book_table
        """
        st.dataframe(pd.read_sql(query, conn))

       #Best price range


    if st.button("Best Price Range"):
        query = """
        SELECT name, approx_cost_for_two, rate
        FROM restaurants
        WHERE approx_cost_for_two IN (
            SELECT approx_cost_for_two
            FROM restaurants
            GROUP BY approx_cost_for_two
            ORDER BY AVG(rate) DESC
            LIMIT 5
        )
        ORDER BY approx_cost_for_two, rate DESC
        """
        st.dataframe(pd.read_sql(query, conn))

       #Price segment performance (low/mid/high)


    if st.button("Price Segment Performance"):
        query = """
        SELECT 
           CASE 
              WHEN approx_cost_for_two < 500 THEN 'Low'
              WHEN approx_cost_for_two BETWEEN 500 AND 1500 THEN 'Mid'
              ELSE 'High'
            END as price_category,
            AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY price_category
        """
        st.dataframe(pd.read_sql(query, conn))

       #Most common cuisines


    if st.button("Most Common Cuisines"):
        query = """
        SELECT cuisines, COUNT(*) as count
        FROM restaurants
        GROUP BY cuisines
        ORDER BY count DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, conn))

       #Highest rated cuisines


    if st.button("Top Rated Cuisines"):
        query = """
        SELECT cuisines, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY cuisines
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, conn))

       #Niche cuisines (less count but good rating)


    if st.button("Niche High-Performing Cuisines"):
        query = """
        SELECT cuisines, COUNT(*) as total, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY cuisines
        HAVING total < 50
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, conn))

       #Cost vs rating relation


    if st.button("Cost vs Rating"):
        query = """
        SELECT approx_cost_for_two, AVG(rate) as avg_rating
        FROM restaurants
        GROUP BY approx_cost_for_two
        ORDER BY approx_cost_for_two
        """
        st.dataframe(pd.read_sql(query, conn))

conn.close()