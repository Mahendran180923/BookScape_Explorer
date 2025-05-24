import requests 
import pandas as pd 
from pandas import json_normalize 
from sqlalchemy import create_engine 
import streamlit as st 
import json 
import re
import numpy as np

# Load secrets from secrets.json
with open('.vscode/secrets.json') as f:
    secrets = json.load(f)

# Database connection settings
host = 'localhost'
user = 'postgres'
password = 'password'
database = 'mdte16db'

# Create a database engine
engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")



def clean_html(text):
    # Remove HTML tags (e.g., <b>, <i>, etc.)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Replace HTML entities like &nbsp; with a space
    text = re.sub(r'&nbsp;', ' ', text)
    
    # Optionally, normalize multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_data(text):
    # Handle NaN or None safely (for scalar or array-like)
    if isinstance(text, (float, int)) and pd.isna(text):
        return ''
    
    # If it's a list (common for authors, categories), join elements
    if isinstance(text, list):
        text = ', '.join(map(str, text))

    # If it's still something weird like a numpy array
    if isinstance(text, np.ndarray):
        text = ', '.join(map(str, text.tolist()))

    # Now convert to string
    text = str(text)

    # Remove unwanted characters
    text = re.sub(r'[{}\[\]\.]', '', text)

    return text



# Create a function for processing the data extract using googles API
def process_data(df):
    df['volumeInfo.categories'] = df['volumeInfo.categories'].apply(lambda x: x if isinstance(x, list) else [x] if x else [df["volumeInfo.title"]])
    df['volumeInfo.authors'] = df['volumeInfo.authors'].apply(lambda x: x if isinstance(x, list) else [x] if x else ['Unknown Author'])
    books_data = pd.DataFrame({
        "book_id": df["id"],
        "search_key": df.get("searchInfo.textSnippet", pd.Series(index=df.index)).fillna(df["volumeInfo.title"]),
        "book_title": df["volumeInfo.title"].fillna('Unknown Title'),
        "subtitle": df.get("volumeInfo.subtitle", pd.Series(index=df.index)).fillna(df["volumeInfo.title"]),
        "book_authors": df["volumeInfo.authors"].fillna('Not Available').apply(clean_data),
        "book_description": df.get("volumeInfo.description", pd.Series(index=df.index)).fillna(df["volumeInfo.title"]),
        "industry_identifiers": df.get('volumeInfo.industryIdentifiers', pd.Series(index=df.index)).apply(lambda x: x[0]['type'] if isinstance(x, list) and x else None),
        "text_reading_modes": df.get('volumeInfo.readingModes.text', pd.Series(index=df.index)),
        "image_reading_modes": df.get('volumeInfo.readingModes.image', pd.Series(index=df.index)),
        "page_count": df.get("volumeInfo.pageCount", pd.Series(index=df.index)).fillna(0),
        "categories": df["volumeInfo.categories"].fillna(df["volumeInfo.title"]).apply(clean_data),
        "language": df.get("volumeInfo.language", pd.Series(index=df.index)).fillna('Not Available'),
        "image_links": df.get("volumeInfo.imageLinks.smallThumbnail", pd.Series(index=df.index)).fillna('Not Available'),
        "ratings_count": df.get("volumeInfo.ratingsCount", pd.Series(index=df.index)).fillna(0),
        "average_rating": df.get("volumeInfo.averageRating", pd.Series(index=df.index)).fillna(0),
        "country": df.get('accessInfo.country', pd.Series(index=df.index)),
        "saleability": df.get('saleInfo.saleability', pd.Series(index=df.index)),
        "is_ebook": df.get('saleInfo.isEbook', pd.Series(index=df.index)),
        "amount_list_price": df.get('saleInfo.listPrice.amount', pd.Series(index=df.index)).fillna(0),
        "currency_code_list_price": df.get('saleInfo.listPrice.currencyCode', pd.Series(index=df.index)).fillna('Not Available'),
        "amount_retail_price": df.get('saleInfo.retailPrice.amount', pd.Series(index=df.index)).fillna(0),
        "currency_code_retail_price": df.get('saleInfo.retailPrice.currencyCode', pd.Series(index=df.index)).fillna('Not Available'),
        "published_year": df.get('volumeInfo.publishedDate', pd.Series(index=df.index)).fillna('0'),
        "publisher": df.get('volumeInfo.publisher', pd.Series(index=df.index)).fillna('Unknown Publisher'),
        "buy_link": df.get('saleInfo.buyLink', pd.Series(index=df.index)).fillna("Not Available"),
    })
    books_data["discount"] = df.get('saleInfo.listPrice.amount', pd.Series(index=df.index)).fillna(0) - df.get('saleInfo.retailPrice.amount', pd.Series(index=df.index)).fillna(0)
    books_data["discount"] = books_data["discount"].fillna(0)
    books_data["published_year"] = books_data["published_year"].astype(str).str[:4]
    books_data['search_key'] =   books_data['search_key'].apply(clean_html)
    books_data = books_data.drop_duplicates(subset=['book_id'])
    return books_data



def search_books(topic, no_of_books):
    books_data = pd.DataFrame()
    starting_index = 0
    while no_of_books > 0:
        API = secrets['GOOGLE_API']
        link = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "key": API,
            "q": topic,
            "maxResults": min(40, no_of_books),
            "startIndex": starting_index
        }
        data = requests.get(link, params=params).json()
        if 'items' in data:
            new_data = data["items"]
            df = json_normalize(new_data)
            df = process_data(df)
            books_data = pd.concat([books_data, df])
            starting_index += min(40, no_of_books)
            no_of_books -= min(40, no_of_books)
        else:
            st.write(f"No results found for query '{topic}'")
            st.write(data)
            break
    return books_data

# Store the data to the database
def store_in_db(df):
    df.to_sql("books_data", engine, if_exists="append", index=False)
    st.success("The above books are stored in the database.")





# To retreive the data from database using sql query
def fetch_data(query):
    """Fetches data from the database using a provided SQL query."""
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def main():
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'end_search' not in st.session_state:
        st.session_state.end_search = False

    if st.session_state.end_search:
        st.write("Thanks for using our BookScape Explorer!")
    else:
        if st.session_state.search_results is None:
            with st.form("search_form"):
                topic = st.text_input("Enter the topic to find a book: ")
                no_of_books = st.number_input("Enter the number of books you want to find: ", min_value=1)
                submitted = st.form_submit_button("Search")
            if submitted:
                if topic:
                    df = search_books(topic, int(no_of_books))
                    st.session_state.search_results = df
                    st.rerun()
                else:
                    st.error("Please enter the topic to search")
        else:
            st.write(st.session_state.search_results)
            store_in_db_button = st.button("Store in DB")
            if store_in_db_button:
                store_in_db(st.session_state.search_results)
            search_more_books_button = st.button("Search More Books")
            if search_more_books_button:
                st.session_state.search_results = None
                st.rerun()
            end_search_button = st.button("End Search")
            if end_search_button:
                st.session_state.end_search = True
                st.rerun()


if __name__ == "__main__":
    main()
