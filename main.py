import time
import mysql.connector
from few_shot_learning import (
    load_few_shots,
    save_few_shot,
    get_sql_fuzzy,
    generate_sql,
    generate_natural_response
)

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root",
    "database": "product_inventory",
    "auth_plugin": "caching_sha2_password"
}

def execute_query(sql):
    db = None
    cursor = None
    try:
        start_time = time.time()
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        elapsed_time = time.time() - start_time
        print(f"\n⏱️ Query Execution Time: {elapsed_time:.2f} seconds")
        return {"status": "success", "data": results, "sql": sql}
    except Exception as e:
        return {"status": "error", "message": str(e), "sql": sql}
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

if __name__ == "__main__":
    print("Inventory Q&A Assistant. Type 'quit' to exit.")
    few_shots = load_few_shots()

    while True:
        question = input("\nAsk a question: ").strip()
        if question.lower() == "quit":
            break

        start_time = time.time()
        sql = get_sql_fuzzy(question, few_shots)

        if sql:
            print("\n✅ Found cached SQL:")
        else:
            print("\n🧠 Asking assistant to generate SQL...")
            sql = generate_sql(question)
            if sql:
                save_few_shot(question, sql)
                few_shots = load_few_shots()
            else:
                print("⚠️ Could not generate SQL. Skipping execution.")
                continue

        print("\n⚡ Executing SQL query:")
        print(sql)

        if not sql.lower().strip().startswith("select"):
            print("⚠️ Skipping non-SELECT SQL for safety.")
            continue

        result = execute_query(sql)

        if result["status"] == "success":
            print("\n📊 Results:")
            if result["data"]:
                for row in result["data"]:
                    print(" -", row)
                print("\n🗣️ Explanation:")
                print(generate_natural_response(question, result["data"]))
            else:
                print("No results found.")
        else:
            print(f"\n❌ Error: {result['message']}")

        total_elapsed_time = time.time() - start_time
        print(f"\n⏱️ Total Time for this request: {total_elapsed_time:.2f} seconds")
