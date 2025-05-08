import pandas as pd
import streamlit as st
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from data_warehousing import fetch_data



# Define a dictionary that maps each query to its question name, visualization, and column settings
queries = {
  # Check Availability of eBooks vs Physical Books
  'Check Availability of eBooks vs Physical Books': {'query':"""SELECT CASE
  WHEN is_ebook = true then 'E_Books'
  ELSE 'Physical Books'
  END as book_type, 
  COUNT(*) AS number_of_books
  FROM books_data
  group by is_ebook""", 'visualisation': 'table', 'columns':['Book_type','Number_of_books']}, 

  # Find the Publisher with the Most Books Published
  'Find the Publisher with the Most Books Published':
  {'query':"""select publisher, 
  count(*) as books_published from books_data
  WHERE publisher != 'Unknown Publisher' group by publisher
  order by books_published desc
  limit 10 """, 'visualisation': 'table', 'columns':['Publisher','Number_of_books']},

  # Identify the Publisher with the Highest Average Rating
  'Identify the Publisher with the Highest Average Rating':
  {'query':"""select publisher, round(average_rating::numeric,2) as highest_rating from books_data
  where publisher != 'Unknown Publisher' and average_rating = 5
  group by publisher, average_rating
  order by highest_rating desc""",'visualisation': 'table', 'columns':['Publisher','highest_rating']},

  # Get the Top 5 Most Expensive Books by Retail Price
  'Get the Top 5 Most Expensive Books by Retail Price':
  {'query': """select book_title, round(amount_retail_price::numeric,0) from books_data
  order by amount_retail_price desc
  limit 5""", 'visualisation': 'table', 'columns':['Book','Retail Price']},

  # Find Books Published After 2010 with at Least 500 Pages
  'Find Books Published After 2010 with at Least 500 Pages':
  {'query': """select book_title, round(published_year::numeric,0), page_count from books_data  
  where published_year >= 2010 and page_count >= 500
  order by page_count desc""", 'visualisation': 'table', 'columns':['Book','Year', 'Number of Pages']},

  # List Books with Discounts Greater than 20% 
  'List Books with Discounts Greater than 20%':
   {'query': """SELECT book_title,
  round(NULLIF((discount / NULLIF(amount_list_price, 0) * 100), 0)::numeric, 2) AS discount_percentage FROM books_data
  WHERE NULLIF((discount / NULLIF(amount_list_price, 0) * 100), 0) >= 20
  order by discount_percentage desc""", 'visualisation': 'table', 'columns':['Book','Discount %']},

  # Find the Average Page Count for eBooks vs Physical Books 
  'Find the Average Page Count for eBooks vs Physical Books':
  {'query': """SELECT  CASE
  WHEN is_ebook = true THEN 'E_Books'
  ELSE 'Physical Books'
  END as book_type,
  round(AVG(page_count)::numeric, 0)
  FROM books_data
  GROUP BY is_ebook""", 'visualisation': 'table', 'columns':['Book Type','Number of Pages']},

  # Find the Top 3 Authors with the Most Books 
  'Find the Top 3 Authors with the Most Books':
  {'query': """SELECT book_authors, COUNT(*) AS books_count FROM books_data
  WHERE book_authors != 'Unknown Author'
  GROUP BY book_authors
  ORDER BY books_count DESC
  LIMIT 3""", 'visualisation': 'table', 'columns':['Authors Name','Number of Books']},

  # List Publishers with More than 10 Books
  'List Publishers with More than 10 Books':
  {'query': """select publisher, count(book_title) as books_count from books_data
  where publisher != 'Unknown Publisher'
  group by publisher
  having count(book_title) > 10
  order by books_count desc
  """, 'visualisation': 'table', 'columns':['Publisher','Number of Books']},

  # Find the Average Page Count for Each Category
  'Find the Average Page Count for Each Category':
  {'query': """select categories, round(avg(page_count)::numeric, 0) as avg_page_count from books_data
  where categories != 'Unknown Categories'
  group by categories
  having round(avg(page_count)::numeric, 0) > 1
  order by avg_page_count desc""", 'visualisation': 'table', 'columns':['Category','Average Page Count']},

  # Retrieve Books with More than 3 Authors
  'Retrieve Books with More than 3 Authors':
  {'query': """SELECT book_title, book_authors
  FROM books_data
  WHERE array_length(string_to_array(book_authors,','),1)>3""", 'visualisation': 'table', 'columns':['Book Title','Authors']},

  # Books with Ratings Count Greater Than the Average
  'Books with Ratings Count Greater Than the Average':
  {'query': """WITH avg_rating AS (
  SELECT round(AVG(ratings_count)::numeric,2) as average
  FROM books_data)
  SELECT book_title, ratings_count
  FROM books_data
  WHERE ratings_count > (SELECT average FROM avg_rating)
  ORDER BY ratings_count desc""", 'visualisation': 'table', 'columns':['Book Title','Ratings Count']}, 

  # Books with the Same Author Published in the Same Year
  'Books with the Same Author Published in the Same Year':
  {'query': """SELECT book_title, book_authors, round(published_year::numeric,0)
  FROM books_data
  WHERE (book_authors, published_year) IN (
  SELECT book_authors, published_year
  FROM books_data
  where book_authors != 'Unknown Author'
  GROUP BY book_authors, published_year
  HAVING COUNT(book_authors) > 1)
  order by book_authors""", 'visualisation': 'table', 'columns':['Book Title','Authors','Year']}, 

  # Books with a Specific Keyword in the Title
  'Books with a Specific Keyword in the Title':
  {'query': """SELECT book_title, search_key
  FROM books_data
  WHERE lower(book_description) LIKE LOWER('%' || search_key || '%')""", 
  'visualisation': 'table', 'columns':['Book Title','Search Key']}, 

  # Year with the Highest Average Book Price
  'Year with the Highest Average Book Price':
  {'query': """SELECT round(published_year::numeric,0), round(avg(amount_retail_price)::numeric, 0) as avg_price from books_data
  where published_year > 1
  group by published_year
  having round(avg(amount_retail_price)::numeric, 0) > 0
  order by avg(amount_retail_price) desc""", 
  'visualisation': 'table', 'columns':['Year','Average Price']}, 

  # Count Authors Who Published 3 Consecutive Years
  'Count Authors Who Published 3 Consecutive Years':
  {'query': """SELECT a1.book_authors, a1.published_year, a2.published_year AS year2, a3.published_year AS year3
  FROM books_data AS a1
  JOIN books_data AS a2
  ON a1.book_authors = a2.book_authors AND a1.published_year + 1 = a2.published_year
  JOIN books_data AS a3
  ON a2.book_authors = a3.book_authors AND a2.published_year + 1 = a3.published_year
  WHERE a1.book_authors != 'Unknown Author'
  AND a2.book_authors != 'Unknown Author'
  AND a3.book_authors != 'Unknown Author'""", 
  'visualisation': 'table', 'columns':['Author Name','Year 1', 'Year 2', 'Year 3']},

  # Authors who have published books in the same year but under different publishers
  'Authors who have published books in the same year but under different publishers':
  {'query': """SELECT book_authors,
  round(published_year::numeric,0) AS year,
  STRING_AGG(DISTINCT publisher, ', ') AS publishers,
  COUNT(DISTINCT publisher) AS count
  FROM books_data
  WHERE book_authors != 'Unknown Author'
  GROUP BY book_authors, published_year
  HAVING COUNT(DISTINCT publisher)> 1""", 
  'visualisation': 'table', 'columns':['Author Name','Year', 'Publisher', 'Number of Books']},

  # Find the average amount_retailPrice of eBooks and physical books
  'Find the average amount_retailPrice of eBooks and physical books':
  {'query': """select coalesce(round(avg(case when is_ebook = 'true'then amount_retail_price end)::numeric,2),0)
  as avg_ebook_price,
  coalesce(avg(case when is_ebook = 'false'then amount_retail_price end),0)
  as avg_physical_book_price
  from books_data""", 
  'visualisation': 'table', 'columns':['avg_ebook_price','avg_physical_book_price']},

  # Identify books that have an averageRating that is more than two standard deviations away from the average rating of all books
  'Identify books that have an averageRating that is more than two standard deviations away from the average rating of all books':
  {'query': """WITH stats AS (SELECT round(AVG(average_rating)::numeric,2) AS avg_rating,
  round(STDDEV(average_rating)::numeric,0) AS stddev_rating FROM books_data)
  SELECT book_title, round(average_rating::numeric,0), round(ratings_count::numeric,0)
  FROM books_data
  CROSS JOIN stats
  WHERE average_rating > stats.avg_rating + 2 * stats.stddev_rating
  OR average_rating < stats.avg_rating - 2 * stats.stddev_rating""", 
  'visualisation': 'table', 'columns':['Book Title','Average Rating', 'Ratings Count']},

  # Determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books
  'Determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books':
  {'query': """select publisher, round(avg(average_rating)::numeric,2) as avg_rating, count(*) as num_books
  from books_data
  where publisher != 'Unknown Publisher'
  group by publisher
  having count(*) >10
  order by avg_rating desc""", 
  'visualisation': 'table', 'columns':['Publisher','Average Rating', 'Number of Books']}
  }







