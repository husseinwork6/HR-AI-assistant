import sqlite3
import pandas as pd
from langchain_core.tools import tool
from src.config import CSV_PATH, DB_PATH

def initialize_db():
    """Converts the employee CSV into a local SQLite database if it doesn't exist."""
    if not DB_PATH.exists():
        print("Initializing SQLite database from CSV...")
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("employees", conn, if_exists="replace", index=False)
        conn.close()
        print("Database initialized successfully.")

initialize_db()

@tool
def query_employee_db(sql_query: str) -> str:
    """
    Queries the employee SQLite database.
    The database contains one table named 'employees'.
    Columns: employee_id, name, leave_balances, department, hire_date, remote_model, performance_rating, training_budget.

    Input MUST be a valid, read-only SQL SELECT query.
    """
    if not sql_query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()

        if not results:
            return "No matching records found in the database."
        return str(results)
    except sqlite3.Error as e:
        return f"SQL Execution Error: {e}"
