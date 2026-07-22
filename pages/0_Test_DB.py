import streamlit as st
from database.queries import run_query

st.title("🗄 Database Test")

query = """
SELECT *
FROM employee_featured
LIMIT 5;
"""

df = run_query(query)

st.dataframe(df)