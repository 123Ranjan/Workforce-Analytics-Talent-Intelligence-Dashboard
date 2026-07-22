# pages/3_Performance_Analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from dashboard.styles.theme import load_theme
from database.connection import get_connection

st.set_page_config(
    page_title="Performance Analytics",
    page_icon="📈",
    layout="wide"
)

load_theme()

st.title("📈 Employee Performance Analytics")
st.markdown("Analyze why employees are underperforming and get actionable insights")

st.divider()

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=300)
def load_performance_data():
    conn = get_connection()
    
    query = """
    SELECT 
        employee_id,
        department,
        job_role,
        gender,
        age,
        monthly_income,
        years_at_company,
        years_in_current_role,
        years_since_last_promotion,
        total_working_years,
        work_life_balance,
        job_satisfaction,
        environment_satisfaction,
        relationship_satisfaction,
        over_time,
        salary_hike_percent,
        performance_rating,
        attrition_status,
        job_involvement_level,
        CASE 
            WHEN performance_rating >= 4 THEN 'High Performer'
            WHEN performance_rating >= 3 THEN 'Average Performer'
            ELSE 'Low Performer'
        END as performance_category,
        CASE 
            WHEN performance_rating <= 2 AND attrition_status = 'Yes' THEN 'Critical Risk'
            WHEN performance_rating <= 2 OR attrition_status = 'Yes' THEN 'At Risk'
            ELSE 'Stable'
        END as risk_category
    FROM employee_featured
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    df['promotion_delay'] = df['years_since_last_promotion'] - 2
    df['promotion_delay'] = df['promotion_delay'].clip(lower=0)
    
    return df

with st.spinner("Loading performance data..."):
    df = load_performance_data()

if df.empty:
    st.warning("No performance data available")
    st.stop()

# =====================================================
# HELPER FUNCTIONS - CASCADING FILTERS (SAME AS HOME)
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

def get_risk_categories(conn, department=None, job_role=None):
    """Get risk categories filtered by department and job role"""
    conditions = []
    if department and department != 'All':
        conditions.append(f"TRIM(department) = '{department}'")
    if job_role and job_role != 'All':
        conditions.append(f"TRIM(job_role) = '{job_role}'")
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT DISTINCT risk_category
    FROM (
        SELECT 
            CASE 
                WHEN performance_rating <= 2 AND attrition_status = 'Yes' THEN 'Critical Risk'
                WHEN performance_rating <= 2 OR attrition_status = 'Yes' THEN 'At Risk'
                ELSE 'Stable'
            END as risk_category
        FROM employee_featured
        {where}
    ) as subquery
    ORDER BY risk_category
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['risk_category'].tolist()

def get_performance_categories(conn, department=None, job_role=None, risk=None):
    """Get performance categories filtered by department, job role, and risk"""
    conditions = []
    if department and department != 'All':
        conditions.append(f"TRIM(department) = '{department}'")
    if job_role and job_role != 'All':
        conditions.append(f"TRIM(job_role) = '{job_role}'")
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
    SELECT DISTINCT performance_category
    FROM (
        SELECT 
            CASE 
                WHEN performance_rating >= 4 THEN 'High Performer'
                WHEN performance_rating >= 3 THEN 'Average Performer'
                ELSE 'Low Performer'
            END as performance_category
        FROM employee_featured
        {where}
    ) as subquery
    ORDER BY performance_category
    """
    df = pd.read_sql(query, conn)
    return ['All'] + df['performance_category'].tolist()

# =====================================================
# SIDEBAR FILTERS - CASCADING (SAME AS HOME)
# =====================================================

with st.sidebar:
    st.markdown("### 🔍 Filters")
    st.caption("Filters are dynamically updated based on your selections")
    
    conn = get_connection()
    
    # Initialize session state
    if 'perf_dept' not in st.session_state:
        st.session_state.perf_dept = 'All'
    if 'perf_job' not in st.session_state:
        st.session_state.perf_job = 'All'
    if 'perf_risk' not in st.session_state:
        st.session_state.perf_risk = 'All'
    if 'perf_perf' not in st.session_state:
        st.session_state.perf_perf = 'All'
    
    # 1. Department Filter
    departments = get_departments(conn)
    selected_department = st.selectbox(
        "🏢 Department",
        departments,
        index=departments.index(st.session_state.perf_dept) if st.session_state.perf_dept in departments else 0,
        key="perf_dept_select"
    )
    st.session_state.perf_dept = selected_department
    
    # 2. Job Role Filter (Filtered by Department)
    job_roles = get_job_roles(conn, selected_department if selected_department != 'All' else None)
    selected_job_role = st.selectbox(
        "💼 Job Role",
        job_roles,
        index=job_roles.index(st.session_state.perf_job) if st.session_state.perf_job in job_roles else 0,
        key="perf_job_select"
    )
    st.session_state.perf_job = selected_job_role
    
    # 3. Risk Category Filter (Filtered by Department and Job Role)
    risk_categories = get_risk_categories(
        conn,
        selected_department if selected_department != 'All' else None,
        selected_job_role if selected_job_role != 'All' else None
    )
    selected_risk = st.selectbox(
        "⚠️ Risk Category",
        risk_categories,
        index=risk_categories.index(st.session_state.perf_risk) if st.session_state.perf_risk in risk_categories else 0,
        key="perf_risk_select"
    )
    st.session_state.perf_risk = selected_risk
    
    # 4. Performance Category Filter (Filtered by Department, Job Role, and Risk)
    performance_categories = get_performance_categories(
        conn,
        selected_department if selected_department != 'All' else None,
        selected_job_role if selected_job_role != 'All' else None,
        selected_risk if selected_risk != 'All' else None
    )
    selected_performance = st.selectbox(
        "⭐ Performance Category",
        performance_categories,
        index=performance_categories.index(st.session_state.perf_perf) if st.session_state.perf_perf in performance_categories else 0,
        key="perf_perf_select"
    )
    st.session_state.perf_perf = selected_performance
    
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
    if selected_risk != 'All':
        st.write(f"✅ Risk: {selected_risk}")
        active_count += 1
    if selected_performance != 'All':
        st.write(f"✅ Performance: {selected_performance}")
        active_count += 1
    
    if active_count == 0:
        st.write("📌 All filters are set to 'All'")
    
    st.markdown("---")
    st.caption("💡 Insights based on employee performance data")
    
    conn.close()

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df.copy()

if selected_department != 'All':
    filtered_df = filtered_df[filtered_df['department'] == selected_department]
if selected_job_role != 'All':
    filtered_df = filtered_df[filtered_df['job_role'] == selected_job_role]
if selected_risk != 'All':
    filtered_df = filtered_df[filtered_df['risk_category'] == selected_risk]
if selected_performance != 'All':
    filtered_df = filtered_df[filtered_df['performance_category'] == selected_performance]

# =====================================================
# PERFORMANCE OVERVIEW
# =====================================================

st.subheader("📊 Performance Overview")

col1, col2, col3, col4 = st.columns(4)

total_employees = len(filtered_df)
high_performers = len(filtered_df[filtered_df['performance_category'] == 'High Performer'])
avg_performers = len(filtered_df[filtered_df['performance_category'] == 'Average Performer'])
low_performers = len(filtered_df[filtered_df['performance_category'] == 'Low Performer'])

with col1:
    st.metric("👥 Total Employees", total_employees)
with col2:
    st.metric("⭐ High Performers", high_performers, delta=f"{high_performers/total_employees*100:.1f}%" if total_employees > 0 else "0%")
with col3:
    st.metric("📊 Average Performers", avg_performers, delta=f"{avg_performers/total_employees*100:.1f}%" if total_employees > 0 else "0%")
with col4:
    st.metric("⚠️ Low Performers", low_performers, delta=f"{low_performers/total_employees*100:.1f}%" if total_employees > 0 else "0%", delta_color="inverse")

st.divider()

col1, col2 = st.columns(2)

with col1:
    perf_counts = filtered_df['performance_category'].value_counts().reset_index()
    perf_counts.columns = ['Category', 'Count']
    
    fig = px.pie(
        perf_counts,
        values='Count',
        names='Category',
        title="Performance Distribution",
        color='Category',
        color_discrete_map={
            'High Performer': '#22C55E',
            'Average Performer': '#F59E0B',
            'Low Performer': '#EF4444'
        }
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    dept_perf = filtered_df.groupby(['department', 'performance_category']).size().reset_index()
    dept_perf.columns = ['department', 'performance_category', 'count']
    
    fig = px.bar(
        dept_perf,
        x='department',
        y='count',
        color='performance_category',
        title="Performance by Department",
        color_discrete_map={
            'High Performer': '#22C55E',
            'Average Performer': '#F59E0B',
            'Low Performer': '#EF4444'
        },
        barmode='group'
    )
    fig.update_layout(height=350, xaxis_title="Department", yaxis_title="Number of Employees")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# ROOT CAUSE ANALYSIS
# =====================================================

st.subheader("🔍 Root Cause Analysis")
st.markdown("What factors are causing low performance?")

low_perf_df = filtered_df[filtered_df['performance_category'] == 'Low Performer']
others_df = filtered_df[filtered_df['performance_category'] != 'Low Performer']

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_sat_low = low_perf_df['job_satisfaction'].mean() if not low_perf_df.empty else 0
    avg_sat_others = others_df['job_satisfaction'].mean() if not others_df.empty else 0
    st.metric("😊 Job Satisfaction", f"{avg_sat_low:.1f} / 4", delta=f"{avg_sat_low - avg_sat_others:.1f} vs Others", delta_color="inverse")

with col2:
    avg_wlb_low = low_perf_df['work_life_balance'].mean() if not low_perf_df.empty else 0
    avg_wlb_others = others_df['work_life_balance'].mean() if not others_df.empty else 0
    st.metric("⚖️ Work-Life Balance", f"{avg_wlb_low:.1f} / 4", delta=f"{avg_wlb_low - avg_wlb_others:.1f} vs Others", delta_color="inverse")

with col3:
    avg_promo_low = low_perf_df['promotion_delay'].mean() if not low_perf_df.empty else 0
    avg_promo_others = others_df['promotion_delay'].mean() if not others_df.empty else 0
    st.metric("📅 Promotion Delay", f"{avg_promo_low:.1f} years", delta=f"+{avg_promo_low - avg_promo_others:.1f} vs Others", delta_color="inverse")

with col4:
    ot_pct_low = (low_perf_df['over_time'] == 'Yes').mean() * 100 if not low_perf_df.empty else 0
    ot_pct_others = (others_df['over_time'] == 'Yes').mean() * 100 if not others_df.empty else 0
    st.metric("⏰ Over Time", f"{ot_pct_low:.1f}%", delta=f"+{ot_pct_low - ot_pct_others:.1f}% vs Others", delta_color="inverse")

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        filtered_df,
        x='performance_category',
        y='job_satisfaction',
        title="Job Satisfaction vs Performance",
        color='performance_category',
        color_discrete_map={
            'High Performer': '#22C55E',
            'Average Performer': '#F59E0B',
            'Low Performer': '#EF4444'
        }
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(
        filtered_df,
        x='performance_category',
        y='work_life_balance',
        title="Work-Life Balance vs Performance",
        color='performance_category',
        color_discrete_map={
            'High Performer': '#22C55E',
            'Average Performer': '#F59E0B',
            'Low Performer': '#EF4444'
        }
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# PERFORMANCE VS ATTRITION
# =====================================================

st.subheader("📊 Performance vs Attrition Analysis")
st.markdown("Understand the relationship between performance and attrition")

col1, col2 = st.columns(2)

with col1:
    perf_attrition = filtered_df.groupby(['performance_category', 'attrition_status']).size().reset_index()
    perf_attrition.columns = ['performance_category', 'attrition_status', 'count']
    
    fig = px.bar(
        perf_attrition,
        x='performance_category',
        y='count',
        color='attrition_status',
        title="Performance Distribution by Attrition Status",
        color_discrete_map={
            'Yes': '#EF4444',
            'No': '#22C55E'
        },
        barmode='group',
        text='count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(height=350, xaxis_title="Performance Category", yaxis_title="Number of Employees")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    attrition_by_perf = filtered_df.groupby('performance_category').apply(
        lambda x: (x['attrition_status'] == 'Yes').mean() * 100
    ).reset_index()
    attrition_by_perf.columns = ['performance_category', 'attrition_rate']
    
    fig = px.bar(
        attrition_by_perf,
        x='performance_category',
        y='attrition_rate',
        title="Attrition Rate by Performance Category",
        color='attrition_rate',
        color_continuous_scale='Reds',
        text='attrition_rate'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        height=350,
        xaxis_title="Performance Category",
        yaxis_title="Attrition Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    high_perf_attrition = (filtered_df[(filtered_df['performance_category'] == 'High Performer') & 
                                       (filtered_df['attrition_status'] == 'Yes')].shape[0] / 
                           filtered_df[filtered_df['performance_category'] == 'High Performer'].shape[0] * 100) if filtered_df[filtered_df['performance_category'] == 'High Performer'].shape[0] > 0 else 0
    st.metric("⭐ High Performers Attrition", f"{high_perf_attrition:.1f}%")

with col2:
    low_perf_attrition = (filtered_df[(filtered_df['performance_category'] == 'Low Performer') & 
                                      (filtered_df['attrition_status'] == 'Yes')].shape[0] / 
                          filtered_df[filtered_df['performance_category'] == 'Low Performer'].shape[0] * 100) if filtered_df[filtered_df['performance_category'] == 'Low Performer'].shape[0] > 0 else 0
    st.metric("⚠️ Low Performers Attrition", f"{low_perf_attrition:.1f}%", delta=f"{low_perf_attrition - high_perf_attrition:.1f}% vs High Perf")

with col3:
    if low_perf_attrition > high_perf_attrition:
        st.success("✅ Low performers are more likely to leave")
    else:
        st.info("📊 High performers leaving at similar rates")

st.divider()

# =====================================================
# PERFORMANCE HEATMAP
# =====================================================

st.subheader("🔥 Performance Heatmap")
st.markdown("Department vs Performance Rating distribution")

heatmap_data = filtered_df.groupby(['department', 'performance_rating']).size().reset_index()
heatmap_data.columns = ['department', 'performance_rating', 'count']

pivot_data = heatmap_data.pivot(index='department', columns='performance_rating', values='count').fillna(0)

fig = go.Figure(data=go.Heatmap(
    z=pivot_data.values,
    x=pivot_data.columns.tolist(),
    y=pivot_data.index.tolist(),
    colorscale='Blues',
    text=pivot_data.values,
    texttemplate="%{text}",
    textfont={"size": 12},
    hovertemplate='Department: %{y}<br>Rating: %{x}<br>Count: %{z}<extra></extra>'
))

fig.update_layout(
    height=400,
    title="Performance Rating Distribution by Department",
    xaxis_title="Performance Rating",
    yaxis_title="Department"
)

st.plotly_chart(fig, use_container_width=True)

if not filtered_df.empty:
    dept_avg_rating = filtered_df.groupby('department')['performance_rating'].mean().sort_values(ascending=False)
    top_dept = dept_avg_rating.index[0] if not dept_avg_rating.empty else None
    top_rating = dept_avg_rating.iloc[0] if not dept_avg_rating.empty else 0
    
    if top_dept:
        st.info(f"🏆 **{top_dept}** has the highest average performance rating: {top_rating:.2f}/4")

st.divider()

# =====================================================
# RISK ASSESSMENT
# =====================================================

st.subheader("⚠️ Risk Assessment")
st.markdown("Identify employees who are underperforming AND at risk of attrition")

risk_counts = filtered_df['risk_category'].value_counts().reset_index()
risk_counts.columns = ['Category', 'Count']

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        risk_counts,
        values='Count',
        names='Category',
        title="Employee Risk Distribution",
        color='Category',
        color_discrete_map={
            'Critical Risk': '#EF4444',
            'At Risk': '#F59E0B',
            'Stable': '#22C55E'
        }
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    dept_risk = filtered_df.groupby(['department', 'risk_category']).size().reset_index()
    dept_risk.columns = ['department', 'risk_category', 'count']
    
    fig = px.bar(
        dept_risk,
        x='department',
        y='count',
        color='risk_category',
        title="Risk by Department",
        color_discrete_map={
            'Critical Risk': '#EF4444',
            'At Risk': '#F59E0B',
            'Stable': '#22C55E'
        },
        barmode='stack'
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.subheader("💡 Actionable Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Priority Actions")
    
    dept_low_perf = filtered_df[filtered_df['performance_category'] == 'Low Performer']['department'].value_counts()
    
    if not dept_low_perf.empty:
        top_dept = dept_low_perf.index[0]
        top_count = dept_low_perf.iloc[0]
        st.warning(f"**Department: {top_dept}** has {top_count} low performers")
        
        dept_data = filtered_df[filtered_df['department'] == top_dept]
        dept_low = dept_data[dept_data['performance_category'] == 'Low Performer']
        
        issues = []
        if dept_low['job_satisfaction'].mean() < 2.5:
            issues.append("Low job satisfaction")
        if dept_low['work_life_balance'].mean() < 2.5:
            issues.append("Poor work-life balance")
        if dept_low['promotion_delay'].mean() > 3:
            issues.append("Long promotion delays")
        if (dept_low['over_time'] == 'Yes').mean() > 0.5:
            issues.append("High over time")
            
        if issues:
            st.write("**Key Issues:** " + ", ".join(issues))
            st.write("**Recommended Actions:**")
            for issue in issues:
                if "satisfaction" in issue:
                    st.write("- Improve job satisfaction through recognition and feedback")
                elif "work-life" in issue:
                    st.write("- Implement flexible working hours and wellness programs")
                elif "promotion" in issue:
                    st.write("- Review promotion timelines and career development paths")
                elif "over time" in issue:
                    st.write("- Optimize workload distribution")
    else:
        st.info("No low performers found")

with col2:
    st.markdown("### 📋 General Recommendations")
    
    recommendations = []
    
    if low_performers > 0:
        avg_sat = filtered_df[filtered_df['performance_category'] == 'Low Performer']['job_satisfaction'].mean()
        if avg_sat < 2.5:
            recommendations.append("🔴 Low job satisfaction among low performers")
        
        avg_wlb = filtered_df[filtered_df['performance_category'] == 'Low Performer']['work_life_balance'].mean()
        if avg_wlb < 2.5:
            recommendations.append("🔴 Poor work-life balance affecting performance")
        
        avg_promo = filtered_df[filtered_df['performance_category'] == 'Low Performer']['promotion_delay'].mean()
        if avg_promo > 3:
            recommendations.append("🔴 Long promotion delays impacting motivation")
        
        ot_pct = (filtered_df[filtered_df['performance_category'] == 'Low Performer']['over_time'] == 'Yes').mean() * 100
        if ot_pct > 50:
            recommendations.append("🔴 High over time among low performers")
    
    if not recommendations:
        recommendations.append("✅ No major issues detected. Continue monitoring.")
    
    for rec in recommendations:
        st.write(rec)
    
    critical_risk = len(filtered_df[filtered_df['risk_category'] == 'Critical Risk'])
    at_risk = len(filtered_df[filtered_df['risk_category'] == 'At Risk'])
    
    if critical_risk > 0:
        st.error(f"🚨 {critical_risk} employees are at CRITICAL risk! Immediate action required.")
    if at_risk > 0:
        st.warning(f"⚠️ {at_risk} employees are at risk. Monitor closely.")

st.divider()

# =====================================================
# ACTION PLAN GENERATOR
# =====================================================

st.subheader("📋 Action Plan Generator")
st.markdown("Generate specific action plans for underperforming employees")

if low_performers > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dept_list = ['All Departments'] + filtered_df[filtered_df['performance_category'] == 'Low Performer']['department'].unique().tolist()
        selected_dept_action = st.selectbox("Select Department for Action Plan", dept_list, key="action_dept")
        num_employees = st.slider("Number of employees to include", 1, min(20, low_performers), 5, key="action_num")
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.metric("📉 Low Performers", low_performers)
        if selected_dept_action != 'All Departments':
            dept_count = len(filtered_df[(filtered_df['department'] == selected_dept_action) & 
                                        (filtered_df['performance_category'] == 'Low Performer')])
            st.metric(f"🏢 {selected_dept_action}", dept_count)
    
    if st.button("📋 Generate Action Plan", use_container_width=True, type="primary", key="gen_action_plan"):
        with st.spinner("Generating action plan..."):
            
            if selected_dept_action != 'All Departments':
                low_perf_employees = filtered_df[(filtered_df['performance_category'] == 'Low Performer') & 
                                                 (filtered_df['department'] == selected_dept_action)]
            else:
                low_perf_employees = filtered_df[filtered_df['performance_category'] == 'Low Performer']
            
            low_perf_employees = low_perf_employees.sort_values('performance_rating')
            low_perf_employees = low_perf_employees.head(num_employees)
            
            if not low_perf_employees.empty:
                st.divider()
                st.subheader(f"📋 Action Plan for {len(low_perf_employees)} Employees")
                
                for idx, (_, emp) in enumerate(low_perf_employees.iterrows(), 1):
                    with st.expander(f"#{idx} Employee {emp['employee_id']} - {emp['department']} | Rating: {emp['performance_rating']}/4"):
                        
                        issues = []
                        actions = []
                        
                        if emp['job_satisfaction'] < 2.5:
                            issues.append("😊 Low Job Satisfaction")
                            actions.append("• Schedule 1-on-1 meeting to discuss career goals and concerns")
                            actions.append("• Implement recognition program for achievements")
                            actions.append("• Provide regular feedback and coaching")
                        
                        if emp['work_life_balance'] < 2.5:
                            issues.append("⚖️ Poor Work-Life Balance")
                            actions.append("• Review workload and redistribute tasks")
                            actions.append("• Offer flexible working hours")
                            actions.append("• Encourage taking breaks and time off")
                        
                        if emp['promotion_delay'] > 3:
                            issues.append("📅 Long Promotion Delay")
                            actions.append("• Discuss career progression path")
                            actions.append("• Create development plan with clear milestones")
                            actions.append("• Consider mentoring or sponsorship programs")
                        
                        if emp['over_time'] == 'Yes':
                            issues.append("⏰ High Over Time")
                            actions.append("• Review workload distribution")
                            actions.append("• Hire additional resources if needed")
                            actions.append("• Improve time management processes")
                        
                        if emp['relationship_satisfaction'] < 2.5:
                            issues.append("👥 Poor Relationship Satisfaction")
                            actions.append("• Team building activities")
                            actions.append("• Improve communication channels")
                            actions.append("• Mediation if needed")
                        
                        if emp['environment_satisfaction'] < 2.5:
                            issues.append("🏢 Low Environment Satisfaction")
                            actions.append("• Improve office environment")
                            actions.append("• Provide necessary tools and equipment")
                            actions.append("• Create better workspace")
                        
                        if emp['salary_hike_percent'] < 12:
                            issues.append("💰 Low Salary Hike")
                            actions.append("• Review compensation package")
                            actions.append("• Consider market adjustment")
                            actions.append("• Discuss performance-based incentives")
                        
                        if not issues:
                            issues.append("⚠️ General Performance Improvement")
                            actions.append("• Set clear performance goals")
                            actions.append("• Provide additional training")
                            actions.append("• Regular performance reviews")
                        
                        st.markdown("**🔍 Root Causes:**")
                        for issue in issues:
                            st.write(f"- {issue}")
                        
                        st.markdown("---")
                        
                        st.markdown("**✅ Recommended Actions:**")
                        for action in actions:
                            st.write(action)
                        
                        st.markdown("---")
                        priority = "High" if len(actions) > 4 else "Medium" if len(actions) > 2 else "Low"
                        urgency = "Urgent" if len(issues) > 2 else "Normal"
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Priority:** `{priority}`")
                        with col2:
                            st.markdown(f"**Urgency:** `{urgency}`")
                        with col3:
                            st.markdown(f"**Expected Improvement:** 0.5-1.0 rating points")
                        
                        st.markdown("**📅 Action Timeline:**")
                        st.markdown("""
                        - **Week 1:** Schedule meeting and identify specific concerns
                        - **Week 2-3:** Implement immediate actions
                        - **Week 4-6:** Monitor progress and adjust
                        - **Week 8:** Review and evaluate improvement
                        """)
                        
                        if st.button(f"📥 Export Plan for Employee {emp['employee_id']}", key=f"export_plan_{idx}"):
                            plan_text = f"""
ACTION PLAN - Employee {emp['employee_id']}
Department: {emp['department']}
Current Rating: {emp['performance_rating']}/4

ROOT CAUSES:
{chr(10).join(['- ' + i for i in issues])}

RECOMMENDED ACTIONS:
{chr(10).join(['- ' + a for a in actions])}

PRIORITY: {priority}
URGENCY: {urgency}
EXPECTED IMPROVEMENT: 0.5-1.0 rating points

TIMELINE:
- Week 1: Schedule meeting and identify specific concerns
- Week 2-3: Implement immediate actions
- Week 4-6: Monitor progress
- Week 8: Review and evaluate
"""
                            st.download_button(
                                label="⬇️ Download Plan",
                                data=plan_text,
                                file_name=f"action_plan_emp_{emp['employee_id']}.txt",
                                mime="text/plain",
                                key=f"download_plan_{idx}"
                            )
                
                st.divider()
                st.subheader("📊 Action Plan Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("👥 Employees Covered", len(low_perf_employees))
                with col2:
                    avg_issues = low_perf_employees[['job_satisfaction', 'work_life_balance', 
                                                     'relationship_satisfaction', 'environment_satisfaction']].mean().mean()
                    st.metric("📊 Avg Issue Score", f"{avg_issues:.1f}/4")
                with col3:
                    st.metric("📋 Total Actions", len(actions) * len(low_perf_employees))
                
            else:
                st.info("No low performers found for the selected criteria")

else:
    st.success("🎉 No low performers found! All employees are performing well.")

# =====================================================
# EMPLOYEE TABLE
# =====================================================

st.subheader("👨‍💼 Employee Performance Table")

display_cols = ['employee_id', 'department', 'job_role', 'gender', 'age', 
                'performance_rating', 'performance_category', 'risk_category',
                'job_satisfaction', 'work_life_balance', 'over_time', 
                'years_since_last_promotion', 'attrition_status']

display_df = filtered_df[display_cols].copy()
display_df.columns = ['ID', 'Department', 'Job Role', 'Gender', 'Age', 
                      'Rating', 'Performance', 'Risk',
                      'Job Sat.', 'WLB', 'Over Time', 
                      'Years Since Promotion', 'Attrition']

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption(f"🔄 Last Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")