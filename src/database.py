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
    Execute a read-only SQL query on the 'employees' table.

    Use this tool to fetch employee details like department, manager, leave balance, etc.

    Table schema: employees
    Columns: employee_id, full_name, department, grade_level, hire_date,
             annual_leave_days, leave_taken, leave_balance, remote_model,
             manager, performance_rating, training_budget, employment_status

    IMPORTANT: For text filtering (like names or departments), ALWAYS use the 'LIKE' operator
    with wildcards to ensure matches (e.g., WHERE full_name LIKE '%Khalid%').
    """
    if not sql_query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Capture column names to make results clear for the LLM
        columns = [description[0] for description in cursor.description]
        conn.close()

        if not results:
            return "No matching records found in the database."

        formatted_results = [dict(zip(columns, row)) for row in results]
        return str(formatted_results)
    except sqlite3.Error as e:
        return f"SQL Execution Error: {e}"
