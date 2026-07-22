import streamlit as st
import plotly.express as px

# =====================================================
# CHART CARD
# =====================================================

def chart_card(title):
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:18px;
            border-radius:16px;
            border:1px solid #E2E8F0;
            box-shadow:0 6px 18px rgba(15,23,42,.08);
            margin-bottom:12px;
        ">
            <h4 style="
                margin:0;
                color:#0F172A;
                font-weight:600;
                font-size:20px;
            ">
                {title}
            </h4>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# COMMON LAYOUT
# =====================================================

CHART_LAYOUT = dict(
    template="plotly_white",
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(
        family="Segoe UI",
        size=13,
        color="#1E293B"
    ),
    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False
    )
)


# =====================================================
# DEPARTMENT CHART
# =====================================================

def department_chart(df):
    chart_card("🏢 Employees by Department")
    
    if df.empty:
        st.info("No department data available")
        return

    fig = px.bar(
        df,
        x="department",
        y="employee_count",
        text="employee_count",
        color_discrete_sequence=["#2563EB"]
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Employees: %{y}<extra></extra>"
    )

    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# GENDER CHART
# =====================================================

def gender_chart(df):
    chart_card("👥 Gender Distribution")
    
    if df.empty:
        st.info("No gender data available")
        return

    fig = px.pie(
        df,
        names="gender",
        values="employee_count",
        hole=0.65,
        color_discrete_sequence=[
            "#2563EB",
            "#10B981",
            "#F59E0B",
            "#EF4444"
        ]
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value} Employees<extra></extra>"
    )

    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# ATTRITION CHART
# =====================================================

def attrition_chart(df):
    chart_card("📉 Attrition by Department")
    
    if df.empty:
        st.info("No attrition data available")
        return

    fig = px.bar(
        df,
        x="department",
        y="attrition_count",
        text="attrition_count",
        color_discrete_sequence=["#EF4444"]
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Attrition: %{y}<extra></extra>"
    )

    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# SALARY DISTRIBUTION
# =====================================================

def salary_distribution_chart(df):
    chart_card("💰 Salary Distribution")
    
    # Check if data is empty
    if df.empty:
        st.info("No salary data available")
        return
    
    # Handle different data formats
    if "monthly_income" in df.columns:
        # Original format: raw monthly income data
        fig = px.histogram(
            df,
            x="monthly_income",
            nbins=25,
            color_discrete_sequence=["#2563EB"]
        )
        fig.update_traces(
            hovertemplate="Salary: %{x}<br>Employees: %{y}<extra></extra>"
        )
        
    elif "salary_band" in df.columns and "employee_count" in df.columns:
        # New format: aggregated salary bands
        fig = px.bar(
            df,
            x="salary_band",
            y="employee_count",
            text="employee_count",
            color_discrete_sequence=["#2563EB"]
        )
        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Employees: %{y}<extra></extra>"
        )
        # Set proper order for salary bands
        salary_order = ["Under $3K", "$3K-$5K", "$5K-$8K", "$8K-$12K", "Over $12K"]
        existing_bands = [band for band in salary_order if band in df["salary_band"].values]
        if existing_bands:
            fig.update_layout(
                xaxis=dict(
                    categoryorder="array",
                    categoryarray=existing_bands
                )
            )
    else:
        # Fallback: show error
        st.error("Unexpected salary data format")
        return

    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)