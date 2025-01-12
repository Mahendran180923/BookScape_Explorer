import streamlit as st
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
from data_visualisation import queries
# from data_warehousing import fetch_data

# Create a Streamlit app
st.markdown("# <center>BookScape Explorer</center>", unsafe_allow_html=True)


# Create a navigation menu
page = st.sidebar.selectbox("Select a page", ["Data Visualisation", "Data Warehousing"])


if page == "Data Visualisation":
# Data Visualisation page
    col1, col2 = st.columns(2)
    with col1:
        selected_query = st.selectbox("Select a query", list(queries.keys()))
    with col2:
        if selected_query:
            try:
                connection = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='password',
                    database='mdte16db'
                )
                mediator = connection.cursor()
                mediator.execute(queries[selected_query]["query"])
                results = mediator.fetchall()
                df = pd.DataFrame(results, columns=queries[selected_query]["columns"])
                
                if queries[selected_query]['visualisation'] == "table":
                    st.table(df)
                elif queries[selected_query]['visualisation'] == "line_chart":
                    st.line_chart(df)
                elif queries[selected_query]['visualisation'] == "bar_chart":
                    st.bar_chart(df)
                    
                connection.close()
            except psycopg2.Error as e:
                st.write("Error:", e)
    if st.button('Back'):
        st.session_state.page = 'home'

# Data Warehousing page
elif page == "Data Warehousing":
    exec(open("data_warehousing.py").read())







