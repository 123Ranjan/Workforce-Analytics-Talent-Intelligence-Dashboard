import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.styles.theme import load_theme
from database.connection import get_connection

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Workforce Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load theme
load_theme()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    .css-1v0mbdj p, .css-1v0mbdj label {
        color: inherit !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        padding: 1.2rem !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }
    
    .dashboard-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0 !important;
    }
    
    .dashboard-subtitle {
        color: #94A3B8 !important;
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
    }
    
    .section-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(59, 130, 246, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPER FUNCTIONS - FIXED
# =====================================================

def get_departments(conn):
    """Get all departments"""
    query = """
    SELECT DISTINCT TRIM(department) as department
    FROM employee_featured 
    ORDER BY TRIM(department)
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['department'].tolist()

def get_job_roles(conn, department=None):
    """Get job roles filtered by department"""
    if department and department != 'All':
        query = f"""
        SELECT DISTINCT TRIM(job_role) as job_role
        FROM employee_featured 
        WHERE TRIM(department) = '{department}'
        ORDER BY TRIM(job_role)
        """
    else:
        query = """
        SELECT DISTINCT TRIM(job_role) as job_role
        FROM employee_featured 
        ORDER BY TRIM(job_role)
        """
    df = pd.read_sql(query, conn)
    return ['All'] + df['job_role'].tolist()

def get_education_fields(conn, department=None, job_role=None):
    """Get education fields filtered by department and job role"""
    conditions = []
    if department and department != 'All':
        conditions.append(f"TRIM(department) = '{department}'")
    if job_role and job_role != 'All':
        conditions.append(f"TRIM(job_role) = '{job_role}'")
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT DISTINCT TRIM(education_field) as education_field
    FROM employee_featured 
    {where}
    ORDER BY TRIM(education_field)
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['education_field'].tolist()

def get_genders(conn, department=None, job_role=None, education=None):
    """Get genders filtered by selections"""
    conditions = []
    if department and department != 'All':
        conditions.append(f"TRIM(department) = '{department}'")
    if job_role and job_role != 'All':
        conditions.append(f"TRIM(job_role) = '{job_role}'")
    if education and education != 'All':
        conditions.append(f"TRIM(education_field) = '{education}'")
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT DISTINCT TRIM(gender) as gender
    FROM employee_featured 
    {where}
    ORDER BY TRIM(gender)
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['gender'].tolist()

def get_attrition_options(conn, department=None, job_role=None, education=None, gender=None):
    """Get attrition status filtered by selections"""
    conditions = []
    if department and department != 'All':
        conditions.append(f"TRIM(department) = '{department}'")
    if job_role and job_role != 'All':
        conditions.append(f"TRIM(job_role) = '{job_role}'")
    if education and education != 'All':
        conditions.append(f"TRIM(education_field) = '{education}'")
    if gender and gender != 'All':
        conditions.append(f"TRIM(gender) = '{gender}'")
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT DISTINCT TRIM(attrition_status) as attrition_status
    FROM employee_featured 
    {where}
    ORDER BY TRIM(attrition_status)
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['attrition_status'].tolist()

# =====================================================
# SIDEBAR FILTERS - CASCADING
# =====================================================

with st.sidebar:
    st.markdown("### 🤖 AI Workforce Analytics")
    st.markdown("---")
    
    conn = get_connection()
    
    # Initialize session state
    if 'dept' not in st.session_state:
        st.session_state.dept = 'All'
    if 'job' not in st.session_state:
        st.session_state.job = 'All'
    if 'edu' not in st.session_state:
        st.session_state.edu = 'All'
    if 'gender' not in st.session_state:
        st.session_state.gender = 'All'
    if 'attrition' not in st.session_state:
        st.session_state.attrition = 'All'
    
    st.markdown("### 🔍 Filters")
    st.caption("Filters are dynamically updated based on your selections")
    
    # 1. Department Filter
    departments = get_departments(conn)
    selected_department = st.selectbox(
        "🏢 Department",
        departments,
        index=departments.index(st.session_state.dept) if st.session_state.dept in departments else 0,
        key="dept_select"
    )
    st.session_state.dept = selected_department
    
    # 2. Job Role Filter (Filtered by Department)
    job_roles = get_job_roles(conn, selected_department if selected_department != 'All' else None)
    selected_job_role = st.selectbox(
        "💼 Job Role",
        job_roles,
        index=job_roles.index(st.session_state.job) if st.session_state.job in job_roles else 0,
        key="job_select"
    )
    st.session_state.job = selected_job_role
    
    # 3. Education Field Filter (Filtered by Department and Job Role)
    edu_fields = get_education_fields(
        conn, 
        selected_department if selected_department != 'All' else None,
        selected_job_role if selected_job_role != 'All' else None
    )
    selected_education = st.selectbox(
        "🎓 Education Field",
        edu_fields,
        index=edu_fields.index(st.session_state.edu) if st.session_state.edu in edu_fields else 0,
        key="edu_select"
    )
    st.session_state.edu = selected_education
    
    # 4. Gender Filter (Filtered by Department, Job Role, Education)
    genders = get_genders(
        conn,
        selected_department if selected_department != 'All' else None,
        selected_job_role if selected_job_role != 'All' else None,
        selected_education if selected_education != 'All' else None
    )
    selected_gender = st.selectbox(
        "👤 Gender",
        genders,
        index=genders.index(st.session_state.gender) if st.session_state.gender in genders else 0,
        key="gender_select"
    )
    st.session_state.gender = selected_gender
    
    # 5. Attrition Filter (Filtered by all previous selections)
    attrition_options = get_attrition_options(
        conn,
        selected_department if selected_department != 'All' else None,
        selected_job_role if selected_job_role != 'All' else None,
        selected_education if selected_education != 'All' else None,
        selected_gender if selected_gender != 'All' else None
    )
    selected_attrition = st.selectbox(
        "📊 Attrition Status",
        attrition_options,
        index=attrition_options.index(st.session_state.attrition) if st.session_state.attrition in attrition_options else 0,
        key="attrition_select"
    )
    st.session_state.attrition = selected_attrition
    
    # Show what's being filtered
    st.markdown("---")
    st.markdown("### 📊 Active Selections")
    
    active_count = 0
    if selected_department != 'All':
        st.write(f"✅ Department: {selected_department}")
        active_count += 1
    if selected_job_role != 'All':
        st.write(f"✅ Job Role: {selected_job_role}")
        active_count += 1
    if selected_education != 'All':
        st.write(f"✅ Education: {selected_education}")
        active_count += 1
    if selected_gender != 'All':
        st.write(f"✅ Gender: {selected_gender}")
        active_count += 1
    if selected_attrition != 'All':
        st.write(f"✅ Attrition: {selected_attrition}")
        active_count += 1
    
    if active_count == 0:
        st.write("📌 All filters are set to 'All'")
    
    st.markdown("---")
    
    # Employee Search
    st.markdown("### 🔍 Search Employee")
    search_employee = st.text_input("Employee ID", placeholder="Enter employee ID...", key="search_employee")
    
    st.markdown("---")
    
    # Get salary and age ranges
    salary_range_data = pd.read_sql("SELECT MIN(monthly_income) as min_sal, MAX(monthly_income) as max_sal FROM employee_featured", conn)
    min_salary = int(salary_range_data['min_sal'][0])
    max_salary = int(salary_range_data['max_sal'][0])
    
    age_range_data = pd.read_sql("SELECT MIN(age) as min_age, MAX(age) as max_age FROM employee_featured", conn)
    min_age = int(age_range_data['min_age'][0])
    max_age = int(age_range_data['max_age'][0])
    
    # Salary Range Slider
    st.markdown("### 💰 Salary Range")
    salary_range = st.slider(
        "Monthly Income",
        min_value=min_salary,
        max_value=max_salary,
        value=(min_salary, max_salary),
        step=500,
        format="$%d",
        key="salary_slider"
    )
    
    st.markdown("---")
    
    # Age Range Slider
    st.markdown("### 🎂 Age Range")
    age_range = st.slider(
        "Age",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        step=1,
        key="age_slider"
    )
    
    st.markdown("---")
    st.markdown("### 📈 Insights")
    st.caption("Select filters to analyze workforce trends")
    
    conn.close()

# =====================================================
# BUILD FILTERS
# =====================================================

filters = {
    "department": selected_department,
    "gender": selected_gender,
    "job_role": selected_job_role,
    "education_field": selected_education,
    "attrition_status": selected_attrition,
    "search": search_employee,
    "salary_range": salary_range,
    "age_range": age_range,
}

def build_where(filters):
    conditions = []
    
    if filters['department'] and filters['department'] != 'All':
        conditions.append(f"TRIM(department) = '{filters['department']}'")
    if filters['gender'] and filters['gender'] != 'All':
        conditions.append(f"TRIM(gender) = '{filters['gender']}'")
    if filters['job_role'] and filters['job_role'] != 'All':
        conditions.append(f"TRIM(job_role) = '{filters['job_role']}'")
    if filters['education_field'] and filters['education_field'] != 'All':
        conditions.append(f"TRIM(education_field) = '{filters['education_field']}'")
    if filters['attrition_status'] and filters['attrition_status'] != 'All':
        conditions.append(f"TRIM(attrition_status) = '{filters['attrition_status']}'")
    
    # Employee search
    if filters.get('search') and str(filters['search']).strip() != "":
        conditions.append(f"CAST(employee_id AS TEXT) ILIKE '%{filters['search'].strip()}%'")
    
    # Salary range
    salary_range = filters.get('salary_range')
    if salary_range and len(salary_range) == 2:
        min_sal, max_sal = salary_range
        if min_sal is not None and max_sal is not None:
            conditions.append(f"monthly_income BETWEEN {min_sal} AND {max_sal}")
    
    # Age range
    age_range = filters.get('age_range')
    if age_range and len(age_range) == 2:
        min_age, max_age = age_range
        if min_age is not None and max_age is not None:
            conditions.append(f"age BETWEEN {min_age} AND {max_age}")
    
    if conditions:
        return "WHERE " + " AND ".join(conditions)
    return ""

where = build_where(filters)

# =====================================================
# QUERY DATA
# =====================================================

conn = get_connection()

try:
    # Total Employees
    total_query = f"SELECT COUNT(*) as total FROM employee_featured {where}"
    total = pd.read_sql(total_query, conn)['total'][0]
    
    # Attrition Rate
    attrition_query = f"""
    SELECT COALESCE(
        ROUND(
            100.0 * SUM(CASE WHEN attrition_status = 'Yes' THEN 1 ELSE 0 END) / 
            NULLIF(COUNT(*), 0),
        2),
        0
    ) as attrition_rate
    FROM employee_featured {where}
    """
    attrition = pd.read_sql(attrition_query, conn)['attrition_rate'][0]
    
    # Average Age
    age_query = f"SELECT COALESCE(ROUND(AVG(age), 1), 0) as avg_age FROM employee_featured {where}"
    avg_age = pd.read_sql(age_query, conn)['avg_age'][0]
    
    # Average Salary
    salary_query = f"SELECT COALESCE(ROUND(AVG(monthly_income), 2), 0) as avg_salary FROM employee_featured {where}"
    avg_salary = pd.read_sql(salary_query, conn)['avg_salary'][0]
    
    # Department Distribution
    dept_query = f"""
    SELECT department, COUNT(*) as employee_count
    FROM employee_featured {where}
    GROUP BY department
    ORDER BY employee_count DESC
    """
    dept_df = pd.read_sql(dept_query, conn)
    
    # Gender Distribution
    gender_query = f"""
    SELECT gender, COUNT(*) as employee_count
    FROM employee_featured {where}
    GROUP BY gender
    ORDER BY employee_count DESC
    """
    gender_df = pd.read_sql(gender_query, conn)
    
    # Attrition by Department
    att_dept_query = f"""
    SELECT department, COUNT(*) as attrition_count
    FROM employee_featured
    WHERE attrition_status = 'Yes'
    """
    other_filters = []
    if filters['department'] and filters['department'] != 'All':
        other_filters.append(f"TRIM(department) = '{filters['department']}'")
    if filters['gender'] and filters['gender'] != 'All':
        other_filters.append(f"TRIM(gender) = '{filters['gender']}'")
    if filters['job_role'] and filters['job_role'] != 'All':
        other_filters.append(f"TRIM(job_role) = '{filters['job_role']}'")
    if filters['education_field'] and filters['education_field'] != 'All':
        other_filters.append(f"TRIM(education_field) = '{filters['education_field']}'")
    
    if other_filters:
        att_dept_query += " AND " + " AND ".join(other_filters)
    
    att_dept_query += " GROUP BY department ORDER BY attrition_count DESC"
    att_dept_df = pd.read_sql(att_dept_query, conn)
    
    # Salary Distribution
    salary_data_query = f"SELECT monthly_income FROM employee_featured {where}"
    salary_data_df = pd.read_sql(salary_data_query, conn)
    
    # Recent Employees
    recent_query = f"""
    SELECT employee_id, department, job_role, gender, age, monthly_income as salary, attrition_status
    FROM employee_featured {where}
    ORDER BY employee_id
    LIMIT 10
    """
    recent_df = pd.read_sql(recent_query, conn)
    
    conn.close()
    
except Exception as e:
    conn.close()
    st.error(f"⚠️ Error loading data: {e}")
    total = 0
    attrition = 0
    avg_age = 0
    avg_salary = 0
    dept_df = pd.DataFrame()
    gender_df = pd.DataFrame()
    att_dept_df = pd.DataFrame()
    salary_data_df = pd.DataFrame()
    recent_df = pd.DataFrame()

# =====================================================
# HEADER
# =====================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown('<p class="dashboard-title">👥 Workforce Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="dashboard-subtitle">Executive insights into workforce performance & organizational health</p>', unsafe_allow_html=True)

with col2:
    if total > 0:
        st.metric("👥 Total Workforce", f"{total:,}", delta=None)
    else:
        st.metric("👥 Total Workforce", "0", delta=None)

with col3:
    if total > 0:
        st.metric("📊 Attrition Rate", f"{attrition}%", delta=f"{attrition:.1f}%" if attrition > 0 else None, delta_color="inverse")
    else:
        st.metric("📊 Attrition Rate", "0%", delta=None)

st.divider()

# =====================================================
# KPI CARDS
# =====================================================

st.markdown('<p class="section-header">📈 Key Performance Indicators</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("👤 Total Employees", f"{total:,}", help="Total number of active employees")
with c2:
    st.metric("📉 Attrition Rate", f"{attrition}%", help="Percentage of employees who left")
with c3:
    st.metric("🎂 Average Age", f"{avg_age:.1f} years", help="Average age of workforce")
with c4:
    st.metric("💰 Average Salary", f"${avg_salary:,.0f}", help="Average monthly salary")

st.divider()

# =====================================================
# CHARTS
# =====================================================

st.markdown('<p class="section-header">📊 Workforce Distribution</p>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    if not dept_df.empty:
        fig = px.bar(
            dept_df,
            x="department",
            y="employee_count",
            text="employee_count",
            title="🏢 Employees by Department",
            color="department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title="Department",
            yaxis_title="Number of Employees"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No department data available")

with right:
    if not gender_df.empty:
        fig = px.pie(
            gender_df,
            names="gender",
            values="employee_count",
            title="👥 Gender Distribution",
            color_discrete_sequence=["#3B82F6", "#EC4899"],
            hole=0.4
        )
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No gender data available")

st.divider()

# =====================================================
# EMPLOYEE INSIGHTS
# =====================================================

st.markdown('<p class="section-header">📉 Employee Insights</p>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    if not att_dept_df.empty:
        fig = px.bar(
            att_dept_df,
            x="department",
            y="attrition_count",
            text="attrition_count",
            title="🚪 Attrition by Department",
            color="attrition_count",
            color_continuous_scale="Reds"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title="Department",
            yaxis_title="Number of Attritions"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No attrition data available")

with right:
    if not salary_data_df.empty:
        fig = px.histogram(
            salary_data_df,
            x="monthly_income",
            nbins=30,
            title="💰 Salary Distribution",
            color_discrete_sequence=["#3B82F6"],
            labels={"monthly_income": "Monthly Income ($)"}
        )
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title="Monthly Income ($)",
            yaxis_title="Number of Employees"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No salary data available")

st.divider()

# =====================================================
# EMPLOYEE TABLE
# =====================================================

st.markdown('<p class="section-header">👨‍💼 Recent Employees</p>', unsafe_allow_html=True)

if not recent_df.empty:
    display_df = recent_df.copy()
    display_df['salary'] = display_df['salary'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "employee_id": "Employee ID",
            "department": "Department",
            "job_role": "Job Role",
            "gender": "Gender",
            "age": "Age",
            "salary": "Salary",
            "attrition_status": "Attrition Status"
        }
    )
else:
    st.info("No employees match the selected filters")

# =====================================================
# ACTIVE FILTERS
# =====================================================

active_filters = []
for key, value in filters.items():
    if key in ["salary_range", "age_range"]:
        if value and len(value) == 2:
            if key == "salary_range":
                active_filters.append(f"Salary: ${value[0]:,} - ${value[1]:,}")
            else:
                active_filters.append(f"Age: {value[0]} - {value[1]}")
    elif value and value != "All" and str(value).strip() != "":
        if key == "search":
            active_filters.append(f"Search: {value}")
        else:
            active_filters.append(f"{key.replace('_', ' ').title()}: {value}")

st.divider()

if active_filters:
    st.caption(f"📌 **Active Filters:** {' | '.join(active_filters)}")
    if total == 0:
        st.warning("⚠️ No records match these filters. Try selecting different combinations.")
else:
    st.caption("📌 **Showing:** All Employees")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.caption(f"🔄 Last Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
with col2:
    st.caption("📊 Data Source: PostgreSQL")
with col3:
    st.caption("🤖 Powered by AI Workforce Intelligence")


# Add to sidebar in 1_Home.py

st.sidebar.markdown("---")
st.sidebar.subheader("📤 Export Data")

export_format = st.sidebar.radio(
    "Export Format",
    ["CSV", "Excel", "PDF Report"],
    key="export_format_radio"
)

if st.sidebar.button("📥 Export Data", use_container_width=True, key="export_btn"):
    try:
        from database.queries import get_all_employees
        from services.report_service import ReportService
        
        export_df = get_all_employees(filters)
        
        if not export_df.empty:
            if export_format == "CSV":
                csv = export_df.to_csv(index=False)
                st.sidebar.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="csv_download"
                )
            elif export_format == "Excel":
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    export_df.to_excel(writer, sheet_name='Employees', index=False)
                    
                    # Add summary sheet
                    summary = pd.DataFrame({
                        'Metric': ['Total Employees', 'Average Age', 'Average Salary'],
                        'Value': [len(export_df), export_df['age'].mean(), export_df['monthly_income'].mean()]
                    })
                    summary.to_excel(writer, sheet_name='Summary', index=False)
                
                st.sidebar.download_button(
                    label="⬇️ Download Excel",
                    data=output.getvalue(),
                    file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="excel_download"
                )
            else:  # PDF Report
                report_service = ReportService()
                insights = {
                    'total_employees': len(export_df),
                    'attrition_count': len(export_df[export_df['attrition_status'] == 'Yes']),
                    'attrition_rate': (len(export_df[export_df['attrition_status'] == 'Yes']) / len(export_df)) * 100,
                    'top_attrition_departments': export_df[export_df['attrition_status'] == 'Yes']['department'].value_counts().head(3).to_dict(),
                    'key_factors': {
                        'avg_age': {'attrited': export_df[export_df['attrition_status'] == 'Yes']['age'].mean(), 
                                   'non_attrited': export_df[export_df['attrition_status'] == 'No']['age'].mean()},
                        'avg_salary': {'attrited': export_df[export_df['attrition_status'] == 'Yes']['monthly_income'].mean(),
                                      'non_attrited': export_df[export_df['attrition_status'] == 'No']['monthly_income'].mean()}
                    }
                }
                pdf_path = report_service.generate_attrition_report(insights)
                with open(pdf_path, 'rb') as f:
                    st.sidebar.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=f"workforce_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        key="pdf_download"
                    )
            st.sidebar.success(f"✅ {len(export_df)} records ready")
        else:
            st.sidebar.warning("No data to export")
    except Exception as e:
        st.sidebar.error(f"Export failed: {e}")