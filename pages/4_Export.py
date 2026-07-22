# pages/4_Export.py - Export Reports with Visualizations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
from io import BytesIO
import base64
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.styles.theme import load_theme
from database.connection import get_connection
from database.queries import get_all_employees, build_where_clause

st.set_page_config(
    page_title="Report Center",
    page_icon="📤",
    layout="wide"
)

load_theme()

st.title("📤 Export Reports")
st.markdown("Generate and export comprehensive workforce reports with visualizations")

st.divider()

# =====================================================
# DATA LOADING
# =====================================================

@st.cache_data(ttl=300)
def load_export_data(filters=None):
    """Load data for export"""
    conn = get_connection()
    
    # Get all data with filters
    where = build_where_clause(filters) if filters else ""
    query = f"SELECT * FROM employee_featured {where} ORDER BY employee_id"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# =====================================================
# SIDEBAR FILTERS
# =====================================================

with st.sidebar:
    st.markdown("### 🔍 Filters")
    st.markdown("Apply filters to export specific data")
    
    conn = get_connection()
    
    # Get filter options
    departments = ['All'] + pd.read_sql("SELECT DISTINCT department FROM employee_featured ORDER BY department", conn)['department'].tolist()
    genders = ['All'] + pd.read_sql("SELECT DISTINCT gender FROM employee_featured ORDER BY gender", conn)['gender'].tolist()
    job_roles = ['All'] + pd.read_sql("SELECT DISTINCT job_role FROM employee_featured ORDER BY job_role", conn)['job_role'].tolist()
    
    conn.close()
    
    selected_department = st.selectbox("🏢 Department", departments, key="export_dept")
    selected_gender = st.selectbox("👤 Gender", genders, key="export_gender")
    selected_job_role = st.selectbox("💼 Job Role", job_roles, key="export_role")
    
    st.markdown("---")
    
    # Export format selection
    export_format = st.radio(
        "📄 Export Format",
        ["CSV", "Excel", "PDF Report with Charts"],
        key="export_format_main"
    )
    
    st.markdown("---")
    st.caption("💡 Data is filtered based on your selections")

# =====================================================
# BUILD FILTERS
# =====================================================

filters = {
    'department': selected_department if selected_department != 'All' else None,
    'gender': selected_gender if selected_gender != 'All' else None,
    'job_role': selected_job_role if selected_job_role != 'All' else None
}

# Load data
df = load_export_data(filters)

if df.empty:
    st.warning("No data available with the selected filters")
    st.stop()

# =====================================================
# DATA PREVIEW
# =====================================================

st.subheader("📊 Data Preview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Records", len(df))
with col2:
    attrition_rate = (len(df[df['attrition_status'] == 'Yes']) / len(df) * 100) if len(df) > 0 else 0
    st.metric("📉 Attrition Rate", f"{attrition_rate:.1f}%")
with col3:
    st.metric("💰 Avg Salary", f"${df['monthly_income'].mean():,.0f}")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# =====================================================
# VISUALIZATIONS FOR PDF
# =====================================================

st.subheader("📊 Dashboard Visualizations")

col1, col2 = st.columns(2)

with col1:
    # Department Distribution
    dept_data = df['department'].value_counts().reset_index()
    dept_data.columns = ['Department', 'Count']
    fig1 = px.bar(
        dept_data,
        x='Department',
        y='Count',
        title="Employees by Department",
        color='Count',
        color_continuous_scale='Blues',
        text='Count'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(height=350)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Gender Distribution
    gender_data = df['gender'].value_counts().reset_index()
    gender_data.columns = ['Gender', 'Count']
    fig2 = px.pie(
        gender_data,
        values='Count',
        names='Gender',
        title="Gender Distribution",
        color_discrete_sequence=['#3B82F6', '#EC4899'],
        hole=0.4
    )
    fig2.update_traces(textinfo='percent+label')
    fig2.update_layout(height=350)
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Performance Distribution
    perf_data = df['performance_rating'].value_counts().sort_index().reset_index()
    perf_data.columns = ['Rating', 'Count']
    fig3 = px.bar(
        perf_data,
        x='Rating',
        y='Count',
        title="Performance Rating Distribution",
        color='Count',
        color_continuous_scale='Greens',
        text='Count'
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Attrition by Department
    att_data = df[df['attrition_status'] == 'Yes']['department'].value_counts().reset_index()
    if not att_data.empty:
        att_data.columns = ['Department', 'Count']
        fig4 = px.bar(
            att_data,
            x='Department',
            y='Count',
            title="Attrition by Department",
            color='Count',
            color_continuous_scale='Reds',
            text='Count'
        )
        fig4.update_traces(textposition='outside')
        fig4.update_layout(height=350)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No attrition data available")

st.divider()

# =====================================================
# EXPORT BUTTONS
# =====================================================

st.subheader("📥 Download Report")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Download CSV", use_container_width=True, type="primary"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Click to Download CSV",
            data=csv,
            file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="csv_download_main"
        )
        st.success("✅ CSV ready for download")

with col2:
    if st.button("📊 Download Excel", use_container_width=True, type="primary"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Employees', index=False)
            
            # Summary sheet
            summary = pd.DataFrame({
                'Metric': ['Total Employees', 'Average Age', 'Average Salary', 'Attrition Rate', 'High Performers', 'Low Performers'],
                'Value': [
                    len(df),
                    round(df['age'].mean(), 1),
                    f"${round(df['monthly_income'].mean(), 2):,.2f}",
                    f"{round((len(df[df['attrition_status'] == 'Yes']) / len(df)) * 100, 1)}%",
                    len(df[df['performance_rating'] >= 4]),
                    len(df[df['performance_rating'] <= 2])
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Department summary
            dept_summary = df.groupby('department').agg({
                'employee_id': 'count',
                'monthly_income': 'mean',
                'age': 'mean',
                'performance_rating': 'mean'
            }).reset_index()
            dept_summary.columns = ['Department', 'Count', 'Avg Salary', 'Avg Age', 'Avg Performance']
            dept_summary.to_excel(writer, sheet_name='Department Summary', index=False)
        
        st.download_button(
            label="⬇️ Click to Download Excel",
            data=output.getvalue(),
            file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="excel_download_main"
        )
        st.success("✅ Excel ready for download")

with col3:
    if st.button("📑 Download PDF with Charts", use_container_width=True, type="primary"):
        try:
            from services.report_service import ReportService
            from services.pdf_service import PDFWithChartsService
            
            pdf_service = PDFWithChartsService()
            
            # Get insights
            insights = {
                'total_employees': len(df),
                'attrition_count': len(df[df['attrition_status'] == 'Yes']),
                'attrition_rate': (len(df[df['attrition_status'] == 'Yes']) / len(df) * 100) if len(df) > 0 else 0,
                'avg_age': df['age'].mean(),
                'avg_salary': df['monthly_income'].mean(),
                'high_performers': len(df[df['performance_rating'] >= 4]),
                'low_performers': len(df[df['performance_rating'] <= 2]),
                'departments': df['department'].value_counts().to_dict(),
                'gender': df['gender'].value_counts().to_dict(),
                'attrition_by_dept': df[df['attrition_status'] == 'Yes']['department'].value_counts().to_dict()
            }
            
            # Generate PDF with charts
            pdf_path = pdf_service.generate_report_with_charts(df, insights)
            
            with open(pdf_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Click to Download PDF",
                    data=f,
                    file_name=f"workforce_report_with_charts_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    key="pdf_download_main"
                )
            st.success("✅ PDF with charts ready for download")
            
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            st.info("Please install reportlab: pip install reportlab")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(f"🔄 Data exported on: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
st.caption("📊 Powered by AI Workforce Intelligence")