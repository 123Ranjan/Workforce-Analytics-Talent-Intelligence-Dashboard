import streamlit as st
import pandas as pd
from database.connection import get_connection

st.set_page_config(layout="wide")
st.title("🔍 Data Inspector - See What's Actually in Your Table")

conn = get_connection()

# Show all columns
st.subheader("📊 All Columns in Table")
columns_query = """
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'employee_featured'
ORDER BY ordinal_position
"""
columns_df = pd.read_sql(columns_query, conn)
st.write(columns_df['column_name'].tolist())

# Show ALL unique values in each filter column
st.subheader("🔍 Actual Values in Your Table")

# Department
dept_df = pd.read_sql("SELECT DISTINCT department FROM employee_featured ORDER BY department", conn)
st.write("**Department Values:**")
st.write(dept_df['department'].tolist())

# Gender
gender_df = pd.read_sql("SELECT DISTINCT gender FROM employee_featured ORDER BY gender", conn)
st.write("**Gender Values:**")
st.write(gender_df['gender'].tolist())

# Job Role - THIS IS THE PROBLEM!
job_df = pd.read_sql("SELECT DISTINCT job_role FROM employee_featured ORDER BY job_role", conn)
st.write("**Job Role Values:**")
st.write(job_df['job_role'].tolist())

# Education Field
edu_df = pd.read_sql("SELECT DISTINCT education_field FROM employee_featured ORDER BY education_field", conn)
st.write("**Education Field Values:**")
st.write(edu_df['education_field'].tolist())

# Attrition Status
attrition_df = pd.read_sql("SELECT DISTINCT attrition_status FROM employee_featured ORDER BY attrition_status", conn)
st.write("**Attrition Status Values:**")
st.write(attrition_df['attrition_status'].tolist())

# Show sample rows
st.subheader("📋 Sample Data (First 10 rows)")
sample_df = pd.read_sql("SELECT * FROM employee_featured LIMIT 10", conn)
st.dataframe(sample_df, use_container_width=True)

# Test with the EXACT values from your table
st.subheader("🧪 Test with Actual Values from Your Table")

# Get the first department value
first_dept = dept_df['department'].iloc[0] if not dept_df.empty else "None"
first_gender = gender_df['gender'].iloc[0] if not gender_df.empty else "None"
first_job = job_df['job_role'].iloc[0] if not job_df.empty else "None"

st.write(f"Testing with: Department='{first_dept}', Gender='{first_gender}', Job Role='{first_job}'")

test_query = f"""
SELECT COUNT(*) as count
FROM employee_featured
WHERE department = '{first_dept}'
  AND gender = '{first_gender}'
  AND job_role = '{first_job}'
"""
test_df = pd.read_sql(test_query, conn)
st.write(f"**Matching records:** {test_df['count'][0]}")

if test_df['count'][0] > 0:
    # Show the actual matching data
    data_query = f"""
    SELECT employee_id, department, gender, job_role, age, monthly_income
    FROM employee_featured
    WHERE department = '{first_dept}'
      AND gender = '{first_gender}'
      AND job_role = '{first_job}'
    LIMIT 5
    """
    data_df = pd.read_sql(data_query, conn)
    st.write("**Matching Data:**")
    st.dataframe(data_df)

conn.close()