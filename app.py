import streamlit as st
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
from data_visualisation import queries
from data_warehousing import search_books, store_in_db, fetch_data

def login_page():
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login")
        with col2:
            without_login = st.form_submit_button("Continue without login")
    if submitted or without_login:
        return True
    return False

def data_warehousing_page():
    st.markdown("# <center>Search Books</center>", unsafe_allow_html=True)
    exec(open("data_warehousing.py").read())


def data_visualisation_page():
    st.markdown("# <center>Available Books Data Analysis</center>", unsafe_allow_html=True)
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

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        tab1 = st.tabs(["Login"])
        with tab1[0]:
            st.title("BookScape Explorer")
            if login_page():
                st.session_state.logged_in = True
                st.rerun()
    else:
        tab1, tab2 = st.tabs(["Search Books", "Available Books Data Analysis"])
        with tab1:
            data_warehousing_page()
        with tab2:
            data_visualisation_page()
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()







