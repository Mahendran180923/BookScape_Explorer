# BookScape Explorer 📚

**BookScape Explorer** is a powerful and interactive application built with Streamlit that allows users to search for books on any topic using the Google Books API, store and manage the results in a PostgreSQL database, and visualize insightful trends and statistics from the collected data.

---

## 🔍 Features

- 📖 Search and retrieve books using custom topics and Google Books API.
- 🗄️ Store structured book metadata in a PostgreSQL data warehouse.
- 📊 Visualize key data insights such as publication trends, rating distribution, and discounts.
- 🧮 Interactive UI built with Streamlit for a user-friendly experience.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – For interactive frontend.
- **PostgreSQL** – As the database backend.
- **SQLAlchemy** – For database connection and ORM.
- **Google Books API** – To fetch book data.
- **Pandas** – For data manipulation.
- **Plotly & Matplotlib** – For data visualization.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mahendran180923/BookScape_Explorer
cd bookscape-explorer
```

### 2. Create and Activate a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧾 Setup

### 1. Set Up PostgreSQL Database

Make sure PostgreSQL is installed and running. Create a database and update the credentials in `data_warehousing.py`.

```python
host = 'localhost'
user = 'your_username'
password = 'your_password'
database = 'yourdb'
```

### 2. Add Google API Key

Create a `.vscode/secrets.json` file and insert your Google Books API key as:

```json
{
    "GOOGLE_API": "your_google_books_api_key"
}
```

---

## 🚀 Run the App

To launch the Streamlit app:

```bash
streamlit run app.py
```

This will open a browser window where you can start exploring books and visualizations!

---

## 📂 Project Structure

```
├── app.py                  # Main Streamlit app with UI
├── data_visualisation.py   # Visualization functions using Matplotlib and Plotly
├── data_warehousing.py     # Fetch and store book data in PostgreSQL
├── requirements.txt        # Python dependencies
└── .vscode/secrets.json    # API keys and secrets (not to be committed)
```

---

## 📊 Results

- ✅ Populated SQL database with over 1000 book records
- ✅ Fully functional Streamlit interface for querying and visualization
- ✅ Efficient SQL queries for in-depth book data analysis

---

## 📎 References

- [Google Books API Docs](https://developers.google.com/books/docs/v1/reference)
- [Streamlit Documentation](https://docs.streamlit.io/library/api-reference)

---
