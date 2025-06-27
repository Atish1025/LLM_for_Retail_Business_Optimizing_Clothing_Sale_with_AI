import os
import re
import subprocess
import time
from difflib import get_close_matches

FEW_SHOT_FILE = "few_shot_examples.txt"

def load_few_shots():
    if os.path.exists(FEW_SHOT_FILE):
        with open(FEW_SHOT_FILE, "r", encoding="utf-8") as f:
            data = f.read()
            examples = re.findall(r'QUESTION:\s*(.*?)\s*SQL:\s*(.*?)\s*(?===|$)', data, re.DOTALL)
            return {q.strip(): s.strip() for q, s in examples}
    return {}

def save_few_shot(question, sql):
    existing = load_few_shots()
    if question not in existing:
        with open(FEW_SHOT_FILE, "a", encoding="utf-8") as f:
            f.write(f"===\nQUESTION: {question}\nSQL:\n{sql}\n===\n\n")

def get_sql_fuzzy(question, few_shots):
    matches = get_close_matches(question, few_shots.keys(), n=1, cutoff=0.75)
    return few_shots.get(matches[0]) if matches else None

def generate_sql(question):
    prompt = f"""You are a helpful MySQL expert assistant. For the following question,
           provide the SQL query inside a markdown code block labeled 'sql'.

QUESTION: "{question}"

TABLE:
- tshirt_info(product_id, name, category, price, stock_quantity, sale_date, quantity, revenue)

RULES:
1. Only use the columns from the tshirt_info table.
2. Format dates as 'YYYY-MM-DD'.
3. Return only a single SQL query in a code block.

Example output:

SQL:
```sql
SELECT ...
```"""

    start_time = time.time()
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    elapsed_time = time.time() - start_time
    print(f"\n⏱️ LLM Generation Time: {elapsed_time:.2f} seconds")

    raw_output = result.stdout.strip()

    # Save prompt and response
    os.makedirs("logs", exist_ok=True)
    with open("logs/latest_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    with open("logs/latest_output.sql", "w", encoding="utf-8") as f:
        f.write(raw_output)

    # Extract SQL
    sql_match = re.search(r'```sql(.*?)```', raw_output, re.DOTALL | re.IGNORECASE)
    sql_query = sql_match.group(1).strip() if sql_match else ""

    if not sql_query:
        with open("logs/error_no_sql_match.txt", "w", encoding="utf-8") as f:
            f.write("No SQL code block found in output:\n\n" + raw_output)

    return sql_query

def generate_natural_response(question, data):
    """
    Generate human-readable explanation of the query result.
    """
    if not data:
        return "There were no matching results."

    preview = "\n".join(str(row) for row in data[:3])  # Use top 3 rows
    prompt = f"""You are a helpful assistant. The user asked: "{question}".
Based on the result: {preview}, provide a natural language summary."""

    result = subprocess.run(
        ["ollama", "run", "deepseek-r1", prompt],
        capture_output=True,
        text=True
    )

    return result.stdout.strip() if result.returncode == 0 else "⚠️ Could not generate explanation."
