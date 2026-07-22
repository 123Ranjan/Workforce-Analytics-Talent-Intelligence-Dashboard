import streamlit as st
import pandas as pd
from database.connection import get_connection

st.set_page_config(layout="wide")
st.title("🧪 Test Dashboard - Hardcoded Filters")

# Get connection
conn = get_connection()

# =====================================================
# HARDCODED FILTERS - Change these to test
# =====================================================

# Test with specific filters
test_department = "Human Resources"  # Change this to test
test_gender = "Female"              # Change this to test
test_job_role = "Healthcare Representative"  # Change this to test

# =====================================================
# QUERY WITH HARDCODED FILTERS
# =====================================================

# 1. Total Employees with filters
query_total = f"""
SELECT COUNT(*) as total
FROM employee_featured
WHERE department = '{test_department}'
  AND gender = '{test_gender}'
  AND job_role = '{test_job_role}'
"""

total_df = pd.read_sql(query_total, conn)
total = total_df['total'][0]

# 2. Attrition Rate
query_attrition = f"""
SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0),
    2) as attrition_rate
FROM employee_featured
WHERE department = '{test_department}'
  AND gender = '{test_gender}'
  AND job_role = '{test_job_role}'
"""

attrition_df = pd.read_sql(query_attrition, conn)
attrition = attrition_df['attrition_rate'][0] if attrition_df['attrition_rate'][0] is not None else 0

# 3. Average Age
query_age = f"""
SELECT ROUND(AVG(age), 1) as avg_age
FROM employee_featured
WHERE department = '{test_department}'
  AND gender = '{test_gender}'
  AND job_role = '{test_job_role}'
"""

age_df = pd.read_sql(query_age, conn)
avg_age = age_df['avg_age'][0] if age_df['avg_age'][0] is not None else 0

# 4. Average Salary
query_salary = f"""
SELECT ROUND(AVG(monthly_income), 2) as avg_salary
FROM employee_featured
WHERE department = '{test_department}'
  AND gender = '{test_gender}'
  AND job_role = '{test_job_role}'
"""

salary_df = pd.read_sql(query_salary, conn)
avg_salary = salary_df['avg_salary'][0] if salary_df['avg_salary'][0] is not None else 0

# =====================================================
# DISPLAY RESULTS
# =====================================================

st.subheader("📊 Test Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", f"{total:,}")

with col2:
    st.metric("Attrition Rate", f"{attrition}%")

with col3:
    st.metric("Average Age", f"{avg_age:.1f}")

with col4:
    st.metric("Average Salary", f"${avg_salary:,.0f}")

# Show the actual data
st.subheader("📋 Sample Data with These Filters")

query_sample = f"""
SELECT employee_id, department, gender, job_role, age, monthly_income, attrition_status
FROM employee_featured
WHERE department = '{test_department}'
  AND gender = '{test_gender}'
  AND job_role = '{test_job_role}'
LIMIT 10
"""

sample_df = pd.read_sql(query_sample, conn)
st.dataframe(sample_df, use_container_width=True)

# Show the queries used
st.subheader("🔍 SQL Queries Used")
st.code(query_total, language="sql")

conn.close()