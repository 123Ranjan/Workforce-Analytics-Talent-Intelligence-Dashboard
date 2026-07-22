# services/ml_service.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.cluster import KMeans
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from database.connection import get_connection

# Check if XGBoost is available
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

class MLService:
    def __init__(self):
        self.model_path = "models/"
        os.makedirs(self.model_path, exist_ok=True)
        
    def load_data(self):
        """Load employee data from database"""
        conn = get_connection()
        query = """
        SELECT 
            age,
            department,
            gender,
            job_role,
            education_field,
            monthly_income,
            years_at_company,
            years_in_current_role,
            years_since_last_promotion,
            years_with_current_manager,
            total_working_years,
            work_life_balance,
            job_satisfaction,
            environment_satisfaction,
            relationship_satisfaction,
            over_time,
            salary_hike_percent,
            performance_rating,
            attrition_status,
            employee_id
        FROM employee_featured
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def prepare_features(self, df):
        """Prepare features for ML models"""
        df_ml = df.copy()
        
        # Handle missing values
        df_ml = df_ml.fillna(0)
        
        # Encode categorical variables
        le_dict = {}
        categorical_cols = ['department', 'gender', 'job_role', 'education_field', 'over_time']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_ml[col] = le.fit_transform(df_ml[col].astype(str))
            le_dict[col] = le
        
        # Prepare features
        feature_cols = [
            'age', 'department', 'gender', 'job_role', 'education_field',
            'monthly_income', 'years_at_company', 'years_in_current_role',
            'years_since_last_promotion', 'years_with_current_manager',
            'total_working_years', 'work_life_balance', 'job_satisfaction',
            'environment_satisfaction', 'relationship_satisfaction',
            'salary_hike_percent', 'performance_rating', 'over_time'
        ]
        
        X = df_ml[feature_cols]
        y = df_ml['attrition_status'].map({'Yes': 1, 'No': 0})
        
        return X, y, le_dict, df_ml
    
    def train_attrition_model(self):
        """Train Random Forest model for attrition prediction"""
        df = self.load_data()
        X, y, le_dict, df_ml = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        rf_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = rf_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model
        model_data = {
            'model': rf_model,
            'accuracy': accuracy,
            'feature_names': X.columns.tolist(),
            'le_dict': le_dict,
            'feature_importance': dict(zip(X.columns, rf_model.feature_importances_))
        }
        joblib.dump(model_data, f"{self.model_path}attrition_model.pkl")
        
        return model_data
    
    def get_model_performance(self):
        """Get detailed model performance metrics"""
        if not os.path.exists(f"{self.model_path}attrition_model.pkl"):
            self.train_attrition_model()
        
        # Load model and data
        model_data = joblib.load(f"{self.model_path}attrition_model.pkl")
        model = model_data['model']
        
        df = self.load_data()
        X, y, le_dict, df_ml = self.prepare_features(df)
        
        # Split and predict
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        return metrics
    
    def predict_attrition(self, employee_data):
        """Predict attrition for specific employee(s)"""
        # Check if model exists
        if not os.path.exists(f"{self.model_path}attrition_model.pkl"):
            self.train_attrition_model()
        
        # Load model
        model_data = joblib.load(f"{self.model_path}attrition_model.pkl")
        model = model_data['model']
        feature_names = model_data['feature_names']
        
        # Prepare input
        df_input = pd.DataFrame([employee_data])
        
        # Encode categorical
        for col, le in model_data['le_dict'].items():
            if col in df_input.columns:
                df_input[col] = le.transform(df_input[col].astype(str))
        
        # Ensure correct feature order
        X_input = df_input[feature_names]
        
        # Predict
        prediction = model.predict(X_input)
        probability = model.predict_proba(X_input)[0][1]
        
        return {
            'attrition_prediction': 'Yes' if prediction[0] == 1 else 'No',
            'attrition_probability': round(probability * 100, 2),
            'risk_level': self.get_risk_level(probability)
        }
    
    def get_risk_level(self, probability):
        if probability < 0.3:
            return 'Low'
        elif probability < 0.6:
            return 'Medium'
        else:
            return 'High'
    
    def get_feature_importance(self):
        if not os.path.exists(f"{self.model_path}attrition_model.pkl"):
            self.train_attrition_model()
        
        model_data = joblib.load(f"{self.model_path}attrition_model.pkl")
        importance = model_data['feature_importance']
        sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        return sorted_importance
    
    def train_salary_model(self):
        df = self.load_data()
        X, y, le_dict, df_ml = self.prepare_features(df)
        
        y_salary = df['monthly_income']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_salary, test_size=0.2, random_state=42
        )
        
        rf_reg = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        rf_reg.fit(X_train, y_train)
        
        y_pred = rf_reg.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        model_data = {
            'model': rf_reg,
            'r2_score': r2,
            'mae': mae,
            'feature_names': X.columns.tolist(),
            'le_dict': le_dict
        }
        joblib.dump(model_data, f"{self.model_path}salary_model.pkl")
        
        return model_data
    
    def predict_salary(self, employee_data):
        if not os.path.exists(f"{self.model_path}salary_model.pkl"):
            self.train_salary_model()
        
        model_data = joblib.load(f"{self.model_path}salary_model.pkl")
        model = model_data['model']
        feature_names = model_data['feature_names']
        
        df_input = pd.DataFrame([employee_data])
        
        for col, le in model_data['le_dict'].items():
            if col in df_input.columns:
                df_input[col] = le.transform(df_input[col].astype(str))
        
        X_input = df_input[feature_names]
        prediction = model.predict(X_input)[0]
        
        return {
            'predicted_salary': round(prediction, 2),
            'confidence': 'High'
        }
    
    def cluster_employees(self, n_clusters=4):
        df = self.load_data()
        X, y, le_dict, df_ml = self.prepare_features(df)
        
        cluster_features = [
            'age', 'monthly_income', 'years_at_company', 
            'work_life_balance', 'job_satisfaction', 'performance_rating'
        ]
        
        X_cluster = df_ml[cluster_features]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_cluster)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        df['cluster'] = clusters
        
        cluster_info = {
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'cluster_labels': clusters.tolist(),
            'cluster_counts': df['cluster'].value_counts().to_dict()
        }
        
        joblib.dump(cluster_info, f"{self.model_path}clusters.pkl")
        
        return df, cluster_info
    
    def get_attrition_insights(self):
        df = self.load_data()
        
        total = len(df)
        attrition_count = len(df[df['attrition_status'] == 'Yes'])
        attrition_rate = (attrition_count / total) * 100
        
        dept_attrition = df[df['attrition_status'] == 'Yes']['department'].value_counts().to_dict()
        role_attrition = df[df['attrition_status'] == 'Yes']['job_role'].value_counts().to_dict()
        
        attrited = df[df['attrition_status'] == 'Yes']
        non_attrited = df[df['attrition_status'] == 'No']
        
        factors = {
            'avg_age': {'attrited': attrited['age'].mean(), 'non_attrited': non_attrited['age'].mean()},
            'avg_salary': {'attrited': attrited['monthly_income'].mean(), 'non_attrited': non_attrited['monthly_income'].mean()},
            'avg_years_company': {'attrited': attrited['years_at_company'].mean(), 'non_attrited': non_attrited['years_at_company'].mean()},
            'avg_job_satisfaction': {'attrited': attrited['job_satisfaction'].mean(), 'non_attrited': non_attrited['job_satisfaction'].mean()},
        }
        
        return {
            'total_employees': total,
            'attrition_count': attrition_count,
            'attrition_rate': attrition_rate,
            'department_attrition': dept_attrition,
            'role_attrition': role_attrition,
            'key_factors': factors,
            'top_attrition_departments': dict(sorted(dept_attrition.items(), key=lambda x: x[1], reverse=True)[:3]),
            'top_attrition_roles': dict(sorted(role_attrition.items(), key=lambda x: x[1], reverse=True)[:3])
        }

    # =====================================================
    # BATCH PREDICTIONS
    # =====================================================

    def batch_predict_attrition(self, file):
        """Predict attrition for multiple employees from CSV"""
        try:
            # Read uploaded file
            df = pd.read_csv(file)
            
            # Check if model exists
            if not os.path.exists(f"{self.model_path}attrition_model.pkl"):
                self.train_attrition_model()
            
            # Load model
            model_data = joblib.load(f"{self.model_path}attrition_model.pkl")
            model = model_data['model']
            feature_names = model_data['feature_names']
            le_dict = model_data['le_dict']
            
            # Prepare data
            df_ml = df.copy()
            
            # Encode categorical variables
            for col, le in le_dict.items():
                if col in df_ml.columns:
                    df_ml[col] = df_ml[col].astype(str)
                    try:
                        df_ml[col] = le.transform(df_ml[col])
                    except:
                        for idx, val in enumerate(df_ml[col]):
                            if val not in le.classes_:
                                df_ml[col].iloc[idx] = le.classes_[0]
                        df_ml[col] = le.transform(df_ml[col])
            
            # Ensure correct feature order
            X_input = df_ml[feature_names]
            
            # Predict
            predictions = model.predict(X_input)
            probabilities = model.predict_proba(X_input)[:, 1]
            
            # Add predictions to dataframe
            df['attrition_prediction'] = ['Yes' if p == 1 else 'No' for p in predictions]
            df['attrition_probability'] = [round(p * 100, 2) for p in probabilities]
            
            # Add risk level
            df['risk_level'] = df['attrition_probability'].apply(self.get_risk_level)
            
            return {
                'success': True,
                'dataframe': df,
                'total': len(df),
                'high_risk': len(df[df['risk_level'] == 'High']),
                'medium_risk': len(df[df['risk_level'] == 'Medium']),
                'low_risk': len(df[df['risk_level'] == 'Low'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    # =====================================================
    # MODEL COMPARISON
    # =====================================================

    def compare_models(self):
        """Compare Random Forest vs XGBoost vs Logistic Regression"""
        try:
            # Load data
            df = self.load_data()
            X, y, le_dict, df_ml = self.prepare_features(df)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            results = {}
            
            # 1. Random Forest
            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced',
                n_jobs=-1
            )
            rf.fit(X_train, y_train)
            rf_pred = rf.predict(X_test)
            rf_score = accuracy_score(y_test, rf_pred)
            rf_cv = cross_val_score(rf, X, y, cv=5).mean()
            
            results['Random Forest'] = {
                'accuracy': round(rf_score * 100, 2),
                'cv_score': round(rf_cv * 100, 2),
                'precision': round(precision_score(y_test, rf_pred) * 100, 2),
                'recall': round(recall_score(y_test, rf_pred) * 100, 2),
                'f1': round(f1_score(y_test, rf_pred) * 100, 2)
            }
            
            # 2. Logistic Regression
            lr = LogisticRegression(
                random_state=42,
                class_weight='balanced',
                max_iter=1000
            )
            lr.fit(X_train, y_train)
            lr_pred = lr.predict(X_test)
            lr_score = accuracy_score(y_test, lr_pred)
            lr_cv = cross_val_score(lr, X, y, cv=5).mean()
            
            results['Logistic Regression'] = {
                'accuracy': round(lr_score * 100, 2),
                'cv_score': round(lr_cv * 100, 2),
                'precision': round(precision_score(y_test, lr_pred) * 100, 2),
                'recall': round(recall_score(y_test, lr_pred) * 100, 2),
                'f1': round(f1_score(y_test, lr_pred) * 100, 2)
            }
            
            # 3. XGBoost (if available)
            if XGBOOST_AVAILABLE:
                xgb = XGBClassifier(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42,
                    use_label_encoder=False,
                    eval_metric='logloss'
                )
                xgb.fit(X_train, y_train)
                xgb_pred = xgb.predict(X_test)
                xgb_score = accuracy_score(y_test, xgb_pred)
                xgb_cv = cross_val_score(xgb, X, y, cv=5).mean()
                
                results['XGBoost'] = {
                    'accuracy': round(xgb_score * 100, 2),
                    'cv_score': round(xgb_cv * 100, 2),
                    'precision': round(precision_score(y_test, xgb_pred) * 100, 2),
                    'recall': round(recall_score(y_test, xgb_pred) * 100, 2),
                    'f1': round(f1_score(y_test, xgb_pred) * 100, 2)
                }
            else:
                results['XGBoost'] = {
                    'accuracy': 'N/A',
                    'cv_score': 'N/A',
                    'precision': 'N/A',
                    'recall': 'N/A',
                    'f1': 'N/A',
                    'note': 'XGBoost not installed. Run: pip install xgboost'
                }
            
            # Find best model
            best_model = max(results.items(), key=lambda x: x[1]['accuracy'] if isinstance(x[1]['accuracy'], float) else 0)
            
            return {
                'success': True,
                'results': results,
                'best_model': best_model[0],
                'best_accuracy': best_model[1]['accuracy']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }