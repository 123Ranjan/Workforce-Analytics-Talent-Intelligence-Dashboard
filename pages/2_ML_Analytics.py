# pages/2_ML_Analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="🧠",
    layout="wide"
)

try:
    from dashboard.styles.theme import load_theme
    load_theme()
except:
    pass

st.title("🧠 Predictive Analytics")
st.markdown("Advanced AI-powered insights for workforce intelligence")

ml_available = False
try:
    from services.ml_service import MLService
    ml_service = MLService()
    ml_available = True
except ImportError as e:
    st.warning("⚠️ ML Service not available. Please install required packages.")
    st.code("pip install scikit-learn joblib")

with st.sidebar:
    st.markdown("### 🤖 ML Features")
    st.markdown("---")
    
    if ml_available:
        ml_option = st.radio(
            "Select ML Feature",
            [
                "📊 Attrition Insights",
                "📊 Model Performance",
                "🎯 Predict Attrition",
                "📈 Feature Importance",
                "👥 Employee Clustering",
                "💰 Predict Salary",
                "📤 Batch Predictions",
                "📊 Model Comparison"
            ],
            key="ml_radio_selector"
        )
        st.markdown("---")
        st.caption("Models are trained on your employee data")
    else:
        st.error("⚠️ ML features unavailable")
        st.info("Install: pip install scikit-learn joblib")
        ml_option = None

if not ml_available:
    st.info("📚 To enable ML features, install required packages:")
    st.code("""
pip install scikit-learn joblib
    """)
    st.markdown("Then restart the application.")

elif ml_option == "📊 Attrition Insights":
    st.subheader("📊 Attrition Analytics Dashboard")
    st.markdown("Gain insights into employee attrition patterns")
    
    with st.spinner("Analyzing data..."):
        try:
            insights = ml_service.get_attrition_insights()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Total Employees", f"{insights['total_employees']:,}")
            with col2:
                st.metric("🚪 Attrition Count", f"{insights['attrition_count']:,}")
            with col3:
                st.metric("📊 Attrition Rate", f"{insights['attrition_rate']:.1f}%")
            with col4:
                st.metric("✅ Retention Rate", f"{100 - insights['attrition_rate']:.1f}%")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏢 Top Attrition Departments")
                if insights['top_attrition_departments']:
                    dept_df = pd.DataFrame(
                        list(insights['top_attrition_departments'].items()),
                        columns=['Department', 'Count']
                    )
                    fig = px.bar(
                        dept_df, 
                        x='Department', 
                        y='Count',
                        title="Departments with Highest Attrition",
                        color='Count',
                        color_continuous_scale='Reds',
                        text='Count'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("💼 Top Attrition Roles")
                if insights['top_attrition_roles']:
                    role_df = pd.DataFrame(
                        list(insights['top_attrition_roles'].items()),
                        columns=['Job Role', 'Count']
                    )
                    fig = px.bar(
                        role_df, 
                        x='Job Role', 
                        y='Count',
                        title="Roles with Highest Attrition",
                        color='Count',
                        color_continuous_scale='Reds',
                        text='Count'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            st.subheader("📈 Key Factors: Attrited vs Non-Attrited")
            
            factors_df = pd.DataFrame(insights['key_factors']).T
            factors_df.columns = ['Attrited', 'Non-Attrited']
            factors_df.index = ['Age', 'Salary', 'Years at Company', 'Job Satisfaction']
            
            fig = px.bar(
                factors_df,
                x=factors_df.index,
                y=['Attrited', 'Non-Attrited'],
                title="Average Values: Attrited vs Non-Attrited Employees",
                barmode='group',
                color_discrete_sequence=['#EF4444', '#3B82F6']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading insights: {e}")

elif ml_option == "📊 Model Performance":
    st.subheader("📊 Model Performance Metrics")
    st.markdown("Evaluate how well the attrition prediction model performs")
    
    if not os.path.exists("models/attrition_model.pkl"):
        st.warning("⚠️ Model not trained yet!")
        if st.button("🚀 Train Model Now", use_container_width=True, key="train_model_perf"):
            with st.spinner("Training model..."):
                try:
                    ml_service.train_attrition_model()
                    st.success("✅ Model trained successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error training model: {e}")
    else:
        try:
            metrics = ml_service.get_model_performance()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎯 Accuracy", f"{metrics['accuracy']*100:.1f}%", help="Percentage of correct predictions")
            with col2:
                st.metric("🔍 Precision", f"{metrics['precision']*100:.1f}%", help="Of predicted attrition, how many actually left")
            with col3:
                st.metric("📊 Recall", f"{metrics['recall']*100:.1f}%", help="Of actual attrition, how many were caught")
            with col4:
                st.metric("⭐ F1-Score", f"{metrics['f1_score']*100:.1f}%", help="Harmonic mean of precision and recall")
            
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 ROC-AUC", f"{metrics['roc_auc']*100:.1f}%", help="Area under ROC curve - higher is better")
            
            with col2:
                report = metrics['classification_report']
                st.metric("📊 Class 0 (Stay)", f"{report['0']['f1-score']*100:.1f}%", help="F1-score for employees who stay")
            
            with col3:
                st.metric("📊 Class 1 (Leave)", f"{report['1']['f1-score']*100:.1f}%", help="F1-score for employees who leave")
            
            st.divider()
            
            st.subheader("📊 Confusion Matrix")
            st.markdown("Shows how well the model predicts attrition")
            
            cm = metrics['confusion_matrix']
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Predicted: Stay', 'Predicted: Leave'],
                y=['Actual: Stay', 'Actual: Leave'],
                text=cm,
                texttemplate="%{text}",
                textfont={"size": 16},
                colorscale='Blues',
                showscale=True
            ))
            
            fig.update_layout(
                height=400,
                title="Confusion Matrix",
                xaxis_title="Predicted",
                yaxis_title="Actual"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.subheader("📈 Model Interpretation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ What This Model Does Well:**")
                if metrics['recall'] > 0.7:
                    st.success("✅ Good at catching employees who will leave (High Recall)")
                else:
                    st.warning("⚠️ May miss some employees who will leave")
                
                if metrics['precision'] > 0.7:
                    st.success("✅ When it predicts leave, it's usually correct (High Precision)")
                else:
                    st.warning("⚠️ May have false alarms")
            
            with col2:
                st.markdown("**📊 Model Performance Summary:**")
                if metrics['accuracy'] > 0.85:
                    st.success(f"✅ Overall accuracy: {metrics['accuracy']*100:.1f}% - Excellent!")
                elif metrics['accuracy'] > 0.75:
                    st.info(f"📊 Overall accuracy: {metrics['accuracy']*100:.1f}% - Good")
                else:
                    st.warning(f"⚠️ Overall accuracy: {metrics['accuracy']*100:.1f}% - Needs improvement")
                
                if metrics['roc_auc'] > 0.8:
                    st.success(f"✅ ROC-AUC: {metrics['roc_auc']*100:.1f}% - Excellent discrimination")
                elif metrics['roc_auc'] > 0.7:
                    st.info(f"📊 ROC-AUC: {metrics['roc_auc']*100:.1f}% - Good discrimination")
                else:
                    st.warning(f"⚠️ ROC-AUC: {metrics['roc_auc']*100:.1f}% - Needs improvement")
            
            with st.expander("📋 Detailed Classification Report"):
                report = metrics['classification_report']
                report_df = pd.DataFrame(report).transpose()
                st.dataframe(report_df.round(3), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading model performance: {e}")

elif ml_option == "🎯 Predict Attrition":
    st.subheader("🎯 Employee Attrition Prediction")
    st.markdown("Enter employee details to predict attrition risk")
    
    if not os.path.exists("models/attrition_model.pkl"):
        with st.spinner("Training attrition model... This may take a moment."):
            try:
                ml_service.train_attrition_model()
                st.success("✅ Model trained successfully!")
            except Exception as e:
                st.error(f"Error training model: {e}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Personal Information")
        age = st.number_input("Age", min_value=18, max_value=70, value=30, key="age_input_ml")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender_input_ml")
        education_field = st.selectbox("Education Field", [
            "Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"
        ], key="edu_input_ml")
    
    with col2:
        st.markdown("#### 💼 Work Information")
        department = st.selectbox("Department", ["Human Resources", "Research & Development", "Sales"], key="dept_input_ml")
        job_role = st.selectbox("Job Role", [
            "Healthcare Representative", "Human Resources", "Laboratory Technician",
            "Manager", "Manufacturing Director", "Research Director",
            "Research Scientist", "Sales Executive", "Sales Representative"
        ], key="role_input_ml")
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=5000, step=500, key="income_input_ml")
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5, key="years_input_ml")
        over_time = st.selectbox("Over Time", ["Yes", "No"], key="overtime_input_ml")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        work_life_balance = st.slider("⚖️ Work Life Balance (1-4)", 1, 4, 3, key="wlb_input_ml")
    with col2:
        job_satisfaction = st.slider("😊 Job Satisfaction (1-4)", 1, 4, 3, key="sat_input_ml")
    with col3:
        environment_satisfaction = st.slider("🏢 Environment Satisfaction (1-4)", 1, 4, 3, key="env_input_ml")
    
    if st.button("🔮 Predict Attrition Risk", use_container_width=True, type="primary", key="predict_btn_ml"):
        with st.spinner("Analyzing employee data..."):
            try:
                employee_data = {
                    'age': age,
                    'department': department,
                    'gender': gender,
                    'job_role': job_role,
                    'education_field': education_field,
                    'monthly_income': monthly_income,
                    'years_at_company': years_at_company,
                    'years_in_current_role': max(0, years_at_company - 2),
                    'years_since_last_promotion': 2,
                    'years_with_current_manager': max(0, years_at_company - 1),
                    'total_working_years': years_at_company + 3,
                    'work_life_balance': work_life_balance,
                    'job_satisfaction': job_satisfaction,
                    'environment_satisfaction': environment_satisfaction,
                    'relationship_satisfaction': 3,
                    'salary_hike_percent': 15,
                    'performance_rating': 3,
                    'over_time': over_time
                }
                
                prediction = ml_service.predict_attrition(employee_data)
                
                st.divider()
                st.subheader("📊 Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("⚠️ Risk Level", prediction['risk_level'])
                with col2:
                    st.metric("📊 Attrition Probability", f"{prediction['attrition_probability']:.1f}%")
                with col3:
                    st.metric("🎯 Prediction", prediction['attrition_prediction'])
                
                st.subheader("📈 Risk Assessment")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prediction['attrition_probability'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Attrition Risk Score"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#3B82F6"},
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(34, 197, 94, 0.5)'},
                            {'range': [30, 60], 'color': 'rgba(251, 146, 60, 0.5)'},
                            {'range': [60, 100], 'color': 'rgba(239, 68, 68, 0.5)'}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': prediction['attrition_probability']
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("💡 Recommendations")
                if prediction['risk_level'] == "Low":
                    st.success("✅ This employee has low attrition risk. Continue providing growth opportunities.")
                elif prediction['risk_level'] == "Medium":
                    st.warning("⚠️ This employee has medium attrition risk. Consider:")
                    st.write("- Regular feedback and recognition")
                    st.write("- Career development opportunities")
                    st.write("- Work-life balance initiatives")
                else:
                    st.error("🚨 This employee has HIGH attrition risk! Immediate action recommended:")
                    st.write("- Schedule a 1-on-1 meeting")
                    st.write("- Review compensation and benefits")
                    st.write("- Discuss career growth opportunities")
                    st.write("- Consider flexible work arrangements")
                
            except Exception as e:
                st.error(f"Error making prediction: {e}")

elif ml_option == "📈 Feature Importance":
    st.subheader("📈 Feature Importance Analysis")
    st.markdown("Understanding what factors most influence employee attrition")
    
    if not os.path.exists("models/attrition_model.pkl"):
        st.warning("⚠️ Model not trained yet!")
        if st.button("🚀 Train Model Now", use_container_width=True, key="train_model_btn"):
            with st.spinner("Training model..."):
                try:
                    ml_service.train_attrition_model()
                    st.success("✅ Model trained successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error training model: {e}")
    else:
        try:
            importance = ml_service.get_feature_importance()
            
            importance_df = pd.DataFrame(list(importance.items()), columns=['Feature', 'Importance'])
            importance_df = importance_df.sort_values('Importance', ascending=False)
            top_10 = importance_df.head(10)
            
            fig = px.bar(
                top_10, 
                x='Importance', 
                y='Feature',
                title="🏆 Top 10 Factors Influencing Attrition",
                orientation='h',
                color='Importance',
                color_continuous_scale='Blues',
                text='Importance'
            )
            fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading feature importance: {e}")

elif ml_option == "👥 Employee Clustering":
    st.subheader("👥 Employee Segmentation Analysis")
    st.markdown("Grouping employees based on similar characteristics")
    
    n_clusters = st.slider("Number of Employee Segments", 2, 6, 4, key="cluster_slider")
    
    if st.button("🔍 Analyze Clusters", use_container_width=True, type="primary", key="cluster_btn"):
        with st.spinner("Analyzing employee segments..."):
            try:
                df, cluster_info = ml_service.cluster_employees(n_clusters)
                
                st.success(f"✅ Found {n_clusters} distinct employee segments!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    cluster_counts = pd.DataFrame(
                        list(cluster_info['cluster_counts'].items()),
                        columns=['Segment', 'Count']
                    )
                    fig = px.pie(
                        cluster_counts, 
                        values='Count', 
                        names='Segment',
                        title="Employee Distribution by Segment",
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4
                    )
                    fig.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(cluster_counts, use_container_width=True, hide_index=True)
                
                st.subheader("👤 Segment Profiles")
                cluster_avg = df.groupby('cluster')[['age', 'monthly_income', 'years_at_company', 
                                                      'work_life_balance', 'job_satisfaction', 'performance_rating']].mean()
                cluster_avg.columns = ['Age', 'Monthly Income', 'Years at Company', 
                                       'Work Life Balance', 'Job Satisfaction', 'Performance Rating']
                st.dataframe(cluster_avg.round(1), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error clustering employees: {e}")

elif ml_option == "💰 Predict Salary":
    st.subheader("💰 Employee Salary Prediction")
    st.markdown("Predict expected salary based on employee attributes")
    
    if not os.path.exists("models/salary_model.pkl"):
        with st.spinner("Training salary prediction model..."):
            try:
                ml_service.train_salary_model()
                st.success("✅ Salary model trained successfully!")
            except Exception as e:
                st.error(f"Error training model: {e}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Personal Information")
        age = st.number_input("Age", min_value=18, max_value=70, value=30, key="salary_age_ml")
        gender = st.selectbox("Gender", ["Male", "Female"], key="salary_gender_ml")
        education_field = st.selectbox("Education Field", [
            "Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"
        ], key="salary_edu_ml")
    
    with col2:
        st.markdown("#### 💼 Work Information")
        department = st.selectbox("Department", ["Human Resources", "Research & Development", "Sales"], key="salary_dept_ml")
        job_role = st.selectbox("Job Role", [
            "Healthcare Representative", "Human Resources", "Laboratory Technician",
            "Manager", "Manufacturing Director", "Research Director",
            "Research Scientist", "Sales Executive", "Sales Representative"
        ], key="salary_role_ml")
        years_experience = st.number_input("Total Years of Experience", min_value=0, max_value=40, value=5, key="salary_exp_ml")
        performance_rating = st.slider("Performance Rating (1-4)", 1, 4, 3, key="salary_perf_ml")
    
    if st.button("💰 Predict Salary", use_container_width=True, type="primary", key="salary_predict_btn"):
        with st.spinner("Calculating predicted salary..."):
            try:
                employee_data = {
                    'age': age,
                    'department': department,
                    'gender': gender,
                    'job_role': job_role,
                    'education_field': education_field,
                    'monthly_income': 5000,
                    'years_at_company': years_experience,
                    'years_in_current_role': 3,
                    'years_since_last_promotion': 2,
                    'years_with_current_manager': 3,
                    'total_working_years': years_experience,
                    'work_life_balance': 3,
                    'job_satisfaction': 3,
                    'environment_satisfaction': 3,
                    'relationship_satisfaction': 3,
                    'salary_hike_percent': 15,
                    'performance_rating': performance_rating,
                    'over_time': 'No'
                }
                
                prediction = ml_service.predict_salary(employee_data)
                
                st.divider()
                st.subheader("📊 Salary Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💰 Predicted Monthly Salary", f"${prediction['predicted_salary']:,.2f}")
                with col2:
                    st.metric("📊 Annual Salary", f"${prediction['predicted_salary'] * 12:,.2f}")
                with col3:
                    st.metric("🎯 Confidence", prediction['confidence'])
                
                try:
                    from database.connection import get_connection
                    conn = get_connection()
                    avg_query = "SELECT AVG(monthly_income) as avg_salary FROM employee_featured"
                    avg_salary = pd.read_sql(avg_query, conn)['avg_salary'][0]
                    conn.close()
                    
                    predicted = prediction['predicted_salary']
                    diff_percent = ((predicted - avg_salary) / avg_salary) * 100
                    
                    if diff_percent > 10:
                        st.success(f"📈 This employee is predicted to earn {diff_percent:.1f}% above the average!")
                    elif diff_percent < -10:
                        st.warning(f"📉 This employee is predicted to earn {abs(diff_percent):.1f}% below average.")
                    else:
                        st.info(f"📊 This employee's predicted salary is near the average.")
                except:
                    pass
                
            except Exception as e:
                st.error(f"Error predicting salary: {e}")

# =====================================================
# BATCH PREDICTIONS
# =====================================================

elif ml_option == "📤 Batch Predictions":
    st.subheader("📤 Batch Attrition Prediction")
    st.markdown("Upload a CSV file to predict attrition for multiple employees at once")
    
    st.info("""
    **CSV Format Requirements:**
    - Must include columns: department, gender, job_role, education_field, over_time
    - Numeric columns: age, monthly_income, years_at_company, work_life_balance, 
      job_satisfaction, environment_satisfaction, relationship_satisfaction,
      salary_hike_percent, performance_rating
    - Sample format: Download the template below
    """)
    
    # Download template
    template_df = pd.DataFrame({
        'age': [30, 35, 28],
        'department': ['Sales', 'Research & Development', 'Human Resources'],
        'gender': ['Male', 'Female', 'Male'],
        'job_role': ['Sales Executive', 'Research Scientist', 'Human Resources'],
        'education_field': ['Marketing', 'Life Sciences', 'Human Resources'],
        'monthly_income': [5000, 7000, 4000],
        'years_at_company': [3, 5, 2],
        'years_in_current_role': [2, 3, 1],
        'years_since_last_promotion': [1, 2, 0],
        'years_with_current_manager': [2, 4, 1],
        'total_working_years': [8, 10, 5],
        'work_life_balance': [3, 2, 4],
        'job_satisfaction': [3, 4, 2],
        'environment_satisfaction': [3, 3, 4],
        'relationship_satisfaction': [3, 4, 3],
        'over_time': ['No', 'Yes', 'No'],
        'salary_hike_percent': [15, 12, 18],
        'performance_rating': [3, 4, 2]
    })
    
    csv_template = template_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV Template",
        data=csv_template,
        file_name="batch_prediction_template.csv",
        mime="text/csv",
        key="template_download"
    )
    
    st.divider()
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], key="batch_upload")
    
    if uploaded_file is not None:
        if st.button("🔮 Predict All Employees", use_container_width=True, type="primary", key="batch_predict_btn"):
            with st.spinner("Predicting attrition for all employees..."):
                result = ml_service.batch_predict_attrition(uploaded_file)
                
                if result['success']:
                    df = result['dataframe']
                    
                    # Summary stats
                    st.divider()
                    st.subheader("📊 Prediction Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("👥 Total Employees", result['total'])
                    with col2:
                        st.metric("🔴 High Risk", result['high_risk'], delta="Urgent", delta_color="inverse")
                    with col3:
                        st.metric("🟡 Medium Risk", result['medium_risk'])
                    with col4:
                        st.metric("🟢 Low Risk", result['low_risk'])
                    
                    st.divider()
                    
                    # Show results
                    st.subheader("📋 Prediction Results")
                    
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download results
                    st.divider()
                    csv_result = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Predictions (CSV)",
                        data=csv_result,
                        file_name="attrition_predictions.csv",
                        mime="text/csv",
                        key="batch_download"
                    )
                    
                    # High risk alert
                    if result['high_risk'] > 0:
                        st.error(f"🚨 {result['high_risk']} employees are at HIGH attrition risk! Review them immediately.")
                    
                else:
                    st.error(f"Error: {result['error']}")
                    st.info("Please check your CSV format and try again.")

# =====================================================
# MODEL COMPARISON
# =====================================================

elif ml_option == "📊 Model Comparison":
    st.subheader("📊 Model Comparison")
    st.markdown("Compare different ML models to find the best performer")
    
    if st.button("🔄 Run Model Comparison", use_container_width=True, type="primary", key="compare_btn"):
        with st.spinner("Training and comparing models..."):
            result = ml_service.compare_models()
            
            if result['success']:
                results = result['results']
                best_model = result['best_model']
                best_accuracy = result['best_accuracy']
                
                st.divider()
                st.subheader("📊 Model Performance Comparison")
                
                # Create comparison table
                compare_df = pd.DataFrame(results).T
                compare_df = compare_df.reset_index().rename(columns={'index': 'Model'})
                
                st.dataframe(compare_df, use_container_width=True, hide_index=True)
                
                # Best model highlight
                st.divider()
                st.success(f"🏆 **Best Model: {best_model}** with {best_accuracy}% accuracy")
                
                # Create bar chart comparison
                st.subheader("📈 Accuracy Comparison")
                
                fig_data = compare_df[compare_df['accuracy'] != 'N/A']
                fig = px.bar(
                    fig_data,
                    x='Model',
                    y='accuracy',
                    title="Model Accuracy Comparison",
                    color='accuracy',
                    color_continuous_scale='Blues',
                    text='accuracy'
                )
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                fig.update_layout(height=400, xaxis_title="Model", yaxis_title="Accuracy (%)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed metrics chart
                st.subheader("📊 Detailed Metrics Comparison")
                
                metrics_df = compare_df.melt(
                    id_vars=['Model'], 
                    value_vars=['precision', 'recall', 'f1', 'cv_score'],
                    var_name='Metric',
                    value_name='Score'
                )
                metrics_df = metrics_df[metrics_df['Score'] != 'N/A']
                
                fig2 = px.bar(
                    metrics_df,
                    x='Model',
                    y='Score',
                    color='Metric',
                    barmode='group',
                    title="Precision, Recall, F1, CV Score Comparison",
                    text='Score'
                )
                fig2.update_traces(texttemplate='%{text}%', textposition='outside')
                fig2.update_layout(height=400, xaxis_title="Model", yaxis_title="Score (%)")
                st.plotly_chart(fig2, use_container_width=True)
                
                # Recommendations
                st.divider()
                st.subheader("💡 Recommendation")
                
                if best_model == 'Random Forest':
                    st.info("""
                    **✅ Random Forest is the best model for this dataset.**
                    
                    **Why?**
                    - Handles non-linear relationships well
                    - Good for high-dimensional data
                    - Provides feature importance
                    - Less prone to overfitting with proper tuning
                    """)
                elif best_model == 'XGBoost':
                    st.info("""
                    **✅ XGBoost is the best model for this dataset.**
                    
                    **Why?**
                    - Handles missing values well
                    - Regularization reduces overfitting
                    - Fast and efficient
                    - Can handle complex patterns
                    """)
                elif best_model == 'Logistic Regression':
                    st.info("""
                    **✅ Logistic Regression is the best model for this dataset.**
                    
                    **Why?**
                    - Simple and interpretable
                    - Fast training
                    - Good baseline model
                    - Less chance of overfitting
                    """)
                
                # XGBoost note
                if 'note' in results.get('XGBoost', {}):
                    st.info("💡 **Note:** XGBoost is not installed. To include XGBoost in comparison, run: `pip install xgboost`")
                
            else:
                st.error(f"Error: {result['error']}")

st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.caption(f"🔄 Last Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
with col2:
    st.caption("📊 Data Source: PostgreSQL")
with col3:
    st.caption("🧠 Powered by ML Models")