## 🧠 LLM for Retail Business(Optimizing Clothing with AI)

### 📌 Project Overview

**LLM for Retail Business 2** is an interactive, AI-powered assistant that allows users to ask natural language questions about their retail inventory data and receive accurate answers through dynamically generated SQL queries. This tool leverages **Large Language Models (LLMs)** with few-shot learning to convert user queries into SQL and retrieve data from a MySQL database, making business insights accessible to non-technical users.

---

### 🛍️ Key Features

* **Natural Language Interface**: Ask inventory-related questions in plain English.
* **Few-Shot Learning Memory**: Remembers and reuses previously generated SQL queries for faster performance.
* **Dynamic SQL Generation**: Uses `deepseek-r1` via `ollama` to generate new SQL queries when needed.
* **Streamlit UI**: Clean, simple web interface for interaction.
* **MySQL Database Integration**: Executes queries securely against a `product_inventory` database.
* **Explainable Results** *(optional)*: Can generate human-readable summaries of query results.

---

### 🏗️ Architecture

* **Frontend**: Streamlit-based UI (`app.py`)
* **Backend Logic**: Query generation and execution (`few_shot_learning.py`, `main.py`)
* **Database**: MySQL with a table named `tshirt_info` containing inventory data
* **LLM Runtime**: Runs `ollama` with DeepSeek-R1 to translate user questions into SQL

---

### 🔧 Technologies Used

* Python
* Streamlit
* LangChain
* SQL
* MySQL Connector
* `ollama` (with DeepSeek-R1 model)
* Regular expressions, subprocesses, fuzzy matching

---

### 📦 Example Use Cases

* “How many T-shirts were sold last month?”
* “Which products generated the highest revenue?”
* “Show stock quantity for all black t-shirts.”

---

### 📁 Project Structure

```
├── app.py                  # Streamlit app entry point
├── few_shot_learning.py   # LLM prompt logic & example caching
├── main.py                # CLI interface and DB connection
├── few_shot_examples.txt  # Cached examples for faster querying
├── logs/                  # Stores LLM prompt/response logs
└── README.md              # Project description
```

---

### ⚙️ How It Works

1. User enters a question like: `"What is the total revenue this month?"`
2. The app checks for a similar question in `few_shot_examples.txt`
3. If not found, it asks `ollama` (DeepSeek-R1) to generate a SQL query
4. Executes the SQL on MySQL database
5. Displays result in a table (and optionally, natural language)

---

### 🚀 Getting Started

**Prerequisites:**

* MySQL running with `product_inventory` database and `tshirt_info` table
* Python 3.10+
* `ollama` with DeepSeek-R1 model installed

**Run the app:**

```bash
streamlit run app.py
```

**Run via CLI (optional):**

```bash
python main.py
```

---

### 🔒 Safety Measures

* Only allows **SELECT** queries to prevent destructive SQL
* Automatically logs prompts and responses for debugging
* Uses fuzzy matching to avoid redundant LLM calls

---

### 🌱 Future Enhancements

* Add user authentication
* Support for non-SQL databases (e.g., MongoDB)
* More advanced summarization and visualization of results
* Batch export options for data

---

Let me know if you want a **short summary version**, or want this exported directly as a `README.md` file.
