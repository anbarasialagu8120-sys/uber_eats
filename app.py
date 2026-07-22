import streamlit as st
import pandas as pd

from mysql_connection import get_connection

from business_questions import show_business_questions
from order_business import show_order_analysis


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Uber Eats Bangalore Restaurant Intelligence",
    layout="wide"
)


st.title("🍽️ Uber Eats Bangalore Restaurant Intelligence & Decision Support System")


# --------------------------------------------------
# Navigation
# --------------------------------------------------

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Dashboard",
        "Business Questions",
        "Order Analysis"
    ]
)


# --------------------------------------------------
# MySQL Connection
# --------------------------------------------------

conn = get_connection()



# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":


    st.sidebar.title("Restaurant Filters")


    # ---------------- Location Filter ----------------

    location_query = """
    SELECT DISTINCT location
    FROM restaurants
    ORDER BY location;
    """

    locations = pd.read_sql(
        location_query,
        conn
    )


    selected_location = st.sidebar.selectbox(
        "📍 Select Location",
        locations["location"]
    )



    # ---------------- Cuisine Filter ----------------

    cuisine_query = f"""

    SELECT DISTINCT cuisines

    FROM restaurants

    WHERE location = '{selected_location}'

    ORDER BY cuisines;

    """


    cuisines = pd.read_sql(
        cuisine_query,
        conn
    )


    selected_cuisine = st.sidebar.selectbox(
        "🍜 Select Cuisine",
        cuisines["cuisines"]
    )



    # ---------------- Rating Filter ----------------

    rating_query = f"""

    SELECT

        MIN(rate) AS min_rating,

        MAX(rate) AS max_rating

    FROM restaurants

    WHERE location = '{selected_location}'

    AND cuisines = '{selected_cuisine}';

    """


    rating_range = pd.read_sql(
        rating_query,
        conn
    )


    min_rating = float(
        rating_range["min_rating"].iloc[0]
    )

    max_rating = float(
        rating_range["max_rating"].iloc[0]
    )



    if min_rating == max_rating:

        selected_rating = min_rating

    else:

        selected_rating = st.sidebar.slider(

            "⭐ Minimum Rating",

            min_value=min_rating,

            max_value=max_rating,

            value=min_rating,

            step=0.1

        )



    # ---------------- Restaurant Data ----------------

    query = f"""

    SELECT

        name AS Restaurant_Name,

        cuisines AS Cuisines,

        rate AS Rating


    FROM restaurants


    WHERE location = '{selected_location}'

    AND cuisines = '{selected_cuisine}'

    AND rate >= {selected_rating}


    ORDER BY rate DESC;


    """


    df = pd.read_sql(
        query,
        conn
    )



    # ---------------- Summary Cards ----------------

    summary_query = f"""

    SELECT

        MAX(rate) AS Highest_Rating,

        COUNT(*) AS Total_Restaurants


    FROM restaurants


    WHERE location = '{selected_location}'

    AND cuisines = '{selected_cuisine}'

    AND rate >= {selected_rating};

    """


    summary = pd.read_sql(
        summary_query,
        conn
    )


    col1, col2 = st.columns(2)


    col1.metric(

        "⭐ Highest Rating",

        summary.iloc[0]["Highest_Rating"]

    )


    col2.metric(

        "🍽️ Total Restaurants",

        summary.iloc[0]["Total_Restaurants"]

    )



    # ---------------- Top 10 Restaurants ----------------

    st.subheader(
        "🏆 Top 10 Restaurants by Rating"
    )


    top10 = df.head(10)



    if len(top10) > 0:


        top10_display = top10[

            [

                "Restaurant_Name",

                "Cuisines",

                "Rating"

            ]

        ]


        st.dataframe(

            top10_display,

            use_container_width=True,

            hide_index=True

        )


    else:


        st.warning(
            "No restaurants found"
        )




# ==================================================
# BUSINESS QUESTIONS
# ==================================================

elif page == "Business Questions":


    show_business_questions(conn)




# ==================================================
# ORDER ANALYSIS
# ==================================================

elif page == "Order Analysis":


    show_order_analysis(conn)