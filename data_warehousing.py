import requests
import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine
import streamlit as st

# Database connection settings
host = 'localhost'
user = 'postgres'
password = 'password'
database = 'mdte16db'

# Create a database engine
engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")


starting_index = 0
topic = ""
balance_books = 0
books_data = {}

def get_user_input():
    topic = st.text_input("Enter the topic to find a book: ", key="topic_1")
    no_of_books = st.number_input("Enter the number of books you want to find: ", min_value=1, key="no_of_books_1")

    
    if st.button("Search"):
        starting_index = 0
        balance_books = no_of_books
        
        while balance_books > 0:
            fetch_data(topic, starting_index, min(40, balance_books))
            starting_index += min(40, balance_books)
            balance_books -= min(40, balance_books)
        
        st.success("Books data has been stored.")
        
        add_more_books = st.selectbox("Do you want to add more books?", ["Yes", "No"])

    
        add_more_books = st.selectbox("Do you want to add more books?", ["Yes", "No"])
    
        if add_more_books == "Yes":
            new_topic = st.text_input("Enter the new topic to find a book: ", key="topic_2")
            new_no_of_books = st.number_input("Enter the new number of books you want to find: ", min_value=1, key="no_of_books_2")

            
            if st.button("Search again"):
                starting_index = 0
                balance_books = no_of_books
                
                while balance_books > 0:
                    fetch_data(topic, starting_index, min(40, balance_books))
                    starting_index += min(40, balance_books)
                    balance_books -= min(40, balance_books)
                
                st.success("Books data has been stored.")
        else:
            st.write("Thank you for using the book finder!")


        

def fetch_data(topic, starting_index, num_books):
    global books_data, engine
    books_data = {} 
    API = "AIzaSyAEFyM1Iywsy7GDU2eUQwX24bMhjRMkj7k"
    link = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "key": API,
        "q": topic,
        "maxResults": num_books,
        "startIndex": starting_index
    }

    data = requests.get(link, params=params).json()
    
    new_data = data["items"]
    df = json_normalize(new_data)

    books_data["book_id"] = df["id"]
    books_data["search_key"] = df["searchInfo.textSnippet"]
    books_data["book_title"] = df["volumeInfo.title"].fillna('Unknown Title')
    books_data["subtitle"] = df["volumeInfo.subtitle"]
    books_data["book_authors"] = df["volumeInfo.authors"].fillna('Unknown Author')
    # books_data['book_authors'] = books_data['book_authors'].str.replace('"', '').str.replace('{', '').str.replace('}', '')
    books_data["book_description"] = df["volumeInfo.description"]
    books_data["industry_identifiers"] = df['volumeInfo.industryIdentifiers'].apply(lambda x: x[0]['type'] if isinstance(x, list) and x else None)
    books_data["text_reading_modes"] = df['volumeInfo.readingModes.text']
    books_data["image_reading_modes"] = df['volumeInfo.readingModes.image']
    books_data["page_count"] = df["volumeInfo.pageCount"].fillna(0)
    books_data["categories"] = df["volumeInfo.categories"].fillna('Unknown Categories')
    # books_data['categories'] = books_data['categories'].str.replace('"', '').str.replace('{', '').str.replace('}', '')
    books_data["language"] = df["volumeInfo.language"]
    books_data["image_links"] = df["volumeInfo.imageLinks.smallThumbnail"]
    books_data["ratings_count"] = df["volumeInfo.ratingsCount"].fillna(0)
    books_data["average_rating"] = df["volumeInfo.averageRating"].fillna(0)
    books_data["country"] = df['accessInfo.country']
    books_data["saleability"] = df['saleInfo.saleability']
    books_data["is_ebook"] = df['saleInfo.isEbook']
    books_data["amount_list_price"] = df['saleInfo.listPrice.amount'].fillna(0)
    books_data["currency_code_list_price"] = df['saleInfo.listPrice.currencyCode'].fillna(0)
    books_data["amount_retail_price"] = df['saleInfo.retailPrice.amount'].fillna(0)
    books_data["currency_code_retail_price"] = df['saleInfo.retailPrice.currencyCode'].fillna(0)
    books_data["published_year"] = df['volumeInfo.publishedDate'].fillna(0)
    books_data["publisher"] = df['volumeInfo.publisher'].fillna('Unknown Publisher')
    books_data["buy_link"] = df['saleInfo.buyLink']
    books_data =  pd.DataFrame(books_data)
    books_data["discount"] = df['saleInfo.listPrice.amount'] - df['saleInfo.retailPrice.amount']
    books_data["discount"] = books_data["discount"].fillna(0)

    books_data["published_year"] = pd.Series(books_data["published_year"]).str[:4]


    # books_data["discount"] = df['saleInfo.listPrice.amount'] - df['saleInfo.retailPrice.amount']
    # books_data["year"] = pd.Series(books_data["year"]).str[:4]

    books_data =  pd.DataFrame(books_data)
    print(books_data)

    books_data.to_sql("books_data", engine, if_exists="append", index=True)
    
    
    

get_user_input()

