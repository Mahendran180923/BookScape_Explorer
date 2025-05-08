# BookScape Explorer 📚

**BookScape Explorer** is a powerful and interactive application built with Streamlit that allows users to search for books on any topic using the Google Books API, store and manage the results in a PostgreSQL database, and visualize insightful trends and statistics from the collected data.

---

## 🚀 **Features**
- **Book Search**: Search for books based on a topic and retrieve information from the Google Books API.
- **Database Storage**: Store searched books into a PostgreSQL database for easy retrieval and analysis.
- **Data Visualization**: Perform complex SQL-based analysis and view results in tables, bar charts, and line charts.
- **Interactive UI**: Smooth navigation with tabs for "Search Books" and "Available Books Data Analysis".
- **Login Option**: Choose to log in with credentials or continue without login.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – For interactive frontend.
- **PostgreSQL** – As the database backend.
- **SQLAlchemy** – For database connection and ORM.
- **Google Books API** – To fetch book data.
- **Pandas** – For data manipulation.


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

Open your browser and navigate to [http://localhost:8501](http://localhost:8501).

---

## 📂 Project Structure

```
BookScape_Explorer/
│
├── app.py                   # Main application logic
│
├── data_warehousing.py      # Handles book search and database storage
│
├── data_visualisation.py    # SQL queries and visualizations
│
├── requirements.txt         # Python dependencies
│
├── README.md                # Project documentation
│
└── .vscode/
    └── secrets.json         # API keys (not included in version control)
```

---

## 📊 Results

- ✅ Populated SQL database with over 1000 book records
- ✅ Fully functional Streamlit interface for querying and visualization
- ✅ Efficient SQL queries for in-depth book data analysis

---


---

## 🌟 **Future Enhancements**
- [ ] Add user registration and authentication.
- [ ] Improve data visualization with interactive charts.
- [ ] Integrate Elasticsearch for faster book search.
- [ ] Enable multi-language search capability.

---


## 📎 References

- [Google Books API Docs](https://developers.google.com/books/docs/v1/reference)
- [Streamlit Documentation](https://docs.streamlit.io/library/api-reference)

---
