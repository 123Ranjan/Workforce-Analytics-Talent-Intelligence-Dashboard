import pandas as pd
from database.connection import get_connection

# =====================================================
# DATABASE QUERY
# =====================================================

def run_query(query):
    """Execute SQL query and return results as DataFrame"""
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# =====================================================
# BUILD WHERE CLAUSE - FIXED VERSION
# =====================================================

def build_where_clause(filters=None):
    """
    Build SQL WHERE clause from filters dictionary
    """
    if filters is None:
        filters = {}

    conditions = []

    # Dropdown Filters - Use TRIM and exact match
    mapping = {
        "department": "department",
        "gender": "gender",
        "job_role": "job_role",
        "education_field": "education_field",
        "attrition_status": "attrition_status",
    }

    for key, column in mapping.items():
        value = filters.get(key)
        if value and value != "All" and str(value).strip() != "":
            # Use TRIM and exact match
            conditions.append(f"TRIM({column}) = '{value.strip()}'")

    # Employee ID Search
    search = filters.get("search", "")
    if search and str(search).strip() != "":
        conditions.append(
            f"CAST(employee_id AS TEXT) ILIKE '%{search.strip()}%'"
        )

    # Salary Range Filter
    salary_range = filters.get("salary_range")
    if salary_range and len(salary_range) == 2:
        min_sal, max_sal = salary_range
        if min_sal is not None and max_sal is not None:
            conditions.append(
                f"monthly_income BETWEEN {min_sal} AND {max_sal}"
            )

    # Age Range Filter
    age_range = filters.get("age_range")
    if age_range and len(age_range) == 2:
        min_age, max_age = age_range
        if min_age is not None and max_age is not None:
            conditions.append(
                f"age BETWEEN {min_age} AND {max_age}"
            )

    if conditions:
        return "WHERE " + " AND ".join(conditions)
    
    return ""

# =====================================================
# KPI QUERIES
# =====================================================

def get_total_employees(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT COUNT(*) AS total
    FROM employee_featured
    {where}
    """
    return run_query(query)

def get_attrition_rate(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT
        COALESCE(
            ROUND(
                100.0 * SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) / 
                NULLIF(COUNT(*), 0),
            2),
            0
        ) AS attrition_rate
    FROM employee_featured
    {where}
    """
    return run_query(query)

def get_average_age(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT COALESCE(ROUND(AVG(age), 1), 0) AS average_age
    FROM employee_featured
    {where}
    """
    return run_query(query)

def get_average_salary(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT COALESCE(ROUND(AVG(monthly_income), 2), 0) AS average_salary
    FROM employee_featured
    {where}
    """
    return run_query(query)

# =====================================================
# CHART QUERIES
# =====================================================

def get_department_distribution(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT
        department,
        COUNT(*) AS employee_count
    FROM employee_featured
    {where}
    GROUP BY department
    ORDER BY employee_count DESC
    """
    return run_query(query)

def get_gender_distribution(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT
        gender,
        COUNT(*) AS employee_count
    FROM employee_featured
    {where}
    GROUP BY gender
    ORDER BY employee_count DESC
    """
    return run_query(query)

def get_salary_distribution(filters=None):
    where = build_where_clause(filters)
    query = f"""
    WITH salary_bands AS (
        SELECT
            CASE 
                WHEN monthly_income < 3000 THEN 'Under $3K'
                WHEN monthly_income < 5000 THEN '$3K-$5K'
                WHEN monthly_income < 8000 THEN '$5K-$8K'
                WHEN monthly_income < 12000 THEN '$8K-$12K'
                ELSE 'Over $12K'
            END AS salary_band
        FROM employee_featured
        {where}
    )
    SELECT
        salary_band,
        COUNT(*) AS employee_count
    FROM salary_bands
    GROUP BY salary_band
    ORDER BY 
        CASE salary_band
            WHEN 'Under $3K' THEN 1
            WHEN '$3K-$5K' THEN 2
            WHEN '$5K-$8K' THEN 3
            WHEN '$8K-$12K' THEN 4
            ELSE 5
        END
    """
    return run_query(query)

def get_attrition_by_department(filters=None):
    where = build_where_clause(filters)
    
    if where == "":
        where = "WHERE attrition_status = 'Yes'"
    else:
        where += " AND attrition_status = 'Yes'"
    
    query = f"""
    SELECT
        department,
        COUNT(*) AS attrition_count
    FROM employee_featured
    {where}
    GROUP BY department
    ORDER BY attrition_count DESC
    """
    return run_query(query)

def get_attrition_by_gender(filters=None):
    where = build_where_clause(filters)
    
    if where == "":
        where = "WHERE attrition_status = 'Yes'"
    else:
        where += " AND attrition_status = 'Yes'"
    
    query = f"""
    SELECT
        gender,
        COUNT(*) AS attrition_count
    FROM employee_featured
    {where}
    GROUP BY gender
    ORDER BY attrition_count DESC
    """
    return run_query(query)

# =====================================================
# EMPLOYEE TABLE
# =====================================================

def get_recent_employees(limit=10, filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT
        employee_id,
        department,
        job_role,
        gender,
        age,
        monthly_income AS salary,
        attrition_status
    FROM employee_featured
    {where}
    ORDER BY employee_id
    LIMIT {limit}
    """
    return run_query(query)

# =====================================================
# FILTER OPTIONS - CLEANED VALUES
# =====================================================

def get_departments():
    query = """
    SELECT DISTINCT TRIM(department) AS department
    FROM employee_featured
    WHERE department IS NOT NULL AND TRIM(department) != ''
    ORDER BY department
    """
    return run_query(query)

def get_genders():
    query = """
    SELECT DISTINCT TRIM(gender) AS gender
    FROM employee_featured
    WHERE gender IS NOT NULL AND TRIM(gender) != ''
    ORDER BY gender
    """
    return run_query(query)

def get_job_roles():
    query = """
    SELECT DISTINCT TRIM(job_role) AS job_role
    FROM employee_featured
    WHERE job_role IS NOT NULL AND TRIM(job_role) != ''
    ORDER BY job_role
    """
    return run_query(query)

def get_education_fields():
    query = """
    SELECT DISTINCT TRIM(education_field) AS education_field
    FROM employee_featured
    WHERE education_field IS NOT NULL AND TRIM(education_field) != ''
    ORDER BY education_field
    """
    return run_query(query)

def get_attrition_options():
    query = """
    SELECT DISTINCT TRIM(attrition_status) AS attrition_status
    FROM employee_featured
    WHERE attrition_status IS NOT NULL AND TRIM(attrition_status) != ''
    ORDER BY attrition_status
    """
    return run_query(query)

# =====================================================
# RANGE QUERIES FOR SLIDERS
# =====================================================

def get_salary_range():
    query = """
    SELECT 
        MIN(monthly_income) AS min_salary,
        MAX(monthly_income) AS max_salary
    FROM employee_featured
    """
    return run_query(query)

def get_age_range():
    query = """
    SELECT 
        MIN(age) AS min_age,
        MAX(age) AS max_age
    FROM employee_featured
    """
    return run_query(query)

# =====================================================
# EXPORT QUERIES
# =====================================================

def get_all_employees(filters=None):
    where = build_where_clause(filters)
    query = f"""
    SELECT *
    FROM employee_featured
    {where}
    ORDER BY employee_id
    """
    return run_query(query)

# =====================================================
# DEBUG: Test filter matching
# =====================================================

def test_filter_match(filter_col, filter_value):
    """Test if a filter value matches data in the table"""
    conn = get_connection()
    try:
        query = f"""
        SELECT COUNT(*) as count
        FROM employee_featured
        WHERE TRIM({filter_col}) = '{filter_value.strip()}'
        """
        result = pd.read_sql(query, conn)
        return result['count'][0]
    finally:
        conn.close()