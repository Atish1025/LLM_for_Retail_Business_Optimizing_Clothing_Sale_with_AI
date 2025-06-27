import streamlit as st
import time
from few_shot_learning import (
    load_few_shots,
    save_few_shot,
    get_sql_fuzzy,
    generate_sql
)
from main import execute_query

# Set up the page
st.set_page_config(page_title="Inventory Q&A Assistant", layout="centered")
st.title("🛒 Inventory Q&A Assistant")

# Load few-shot examples
few_shots = load_few_shots()

# Form for user input
with st.form("query_form"):
    question = st.text_input("Ask a question about inventory:")
    show_sql = st.checkbox("Show generated SQL query", value=True)
    submitted = st.form_submit_button("Submit")

# Handle submission
if submitted and question.strip():
    start_time = time.time()

    with st.spinner("⏳ Processing your question..."):
        sql = get_sql_fuzzy(question, few_shots)

        if not sql:
            sql = generate_sql(question)
            if sql:
                save_few_shot(question, sql)
                few_shots = load_few_shots()
            else:
                st.error("⚠️ Could not generate SQL. Please rephrase.")
                st.stop()

        if not sql.lower().strip().startswith("select"):
            st.error("⚠️ Only SELECT queries are allowed.")
            st.stop()

        result = execute_query(sql)

        if result["status"] != "success":
            st.error(f"❌ SQL Error: {result['message']}")
            st.stop()

        result_data = result["data"]

    # Show SQL if checkbox is enabled
    if show_sql:
        st.code(sql, language="sql")

    # Show results heading always
    st.subheader("📊 Results:")

    # Show table if data is returned
    if result_data is not None and len(result_data) > 0:
        st.table(result_data)
    elif result_data == 0:
        st.table(result_data)
    else:
        st.info("No results found.")

    total_time = time.time() - start_time
    st.caption(f"⏱️ Total time: {total_time:.2f} seconds")
