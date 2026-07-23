# 📊 Workforce Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557C.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.14+-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

</div>

A comprehensive **HR Analytics Platform** for workforce intelligence, predictive analytics, and performance management. Built with Python, Streamlit, and PostgreSQL, it enables organizations to analyze employee data, predict attrition, and generate actionable insights.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
---

## ✨ Features

### 📊 **Executive Dashboard**
- Interactive KPI cards (Total Employees, Attrition Rate, Avg Age, Avg Salary)
- Cascading filters (Department → Job Role → Education → Gender → Attrition)
- Employee search with ID lookup
- Salary & Age range sliders
- Interactive charts (Department, Gender, Attrition, Salary Distribution)
- Recent employees table with real-time updates
- Dark/Light theme toggle

### 🧠 **Predictive Analytics**
- **Attrition Insights** - Department and role-wise attrition analysis
- **Model Performance** - Accuracy, Precision, Recall, F1-Score metrics
- **Confusion Matrix** - Visual representation of model predictions
- **Attrition Prediction** - Predict individual employee attrition risk
- **Feature Importance** - Identify key factors driving attrition
- **Employee Clustering** - K-Means segmentation for targeted interventions
- **Salary Prediction** - Predict employee salary based on attributes
- **Batch Predictions** - Upload CSV and predict for multiple employees
- **Model Comparison** - Compare Random Forest vs XGBoost vs Logistic Regression

### 📈 **Performance Analytics**
- **Performance Overview** - High/Average/Low performer distribution
- **Root Cause Analysis** - Identify why employees underperform
- **Performance vs Attrition** - Correlation analysis between performance and attrition
- **Performance Heatmap** - Department vs Performance Rating distribution
- **Risk Assessment** - Identify underperformers at risk of attrition
- **Action Plan Generator** - Generate specific action plans for low performers
- **Employee Performance Table** - Detailed performance data

### 📋 **Report Center**
- CSV Export with full data
- Excel Export with summary and department sheets
- PDF Report with charts and visualizations
- Department-wise summary
- Data preview before export
- Filter-based reporting

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core programming language |
| **Pandas** | 2.0.3 | Data manipulation & analysis |
| **NumPy** | 1.24.3 | Numerical computations |
| **Matplotlib** | 3.7.1 | Data visualization |
| **Scikit-Learn** | 1.3.0 | Machine Learning models |
| **Joblib** | 1.3.2 | Model persistence |

### Database
| Technology | Version | Purpose |
|------------|---------|---------|
| **PostgreSQL** | 15+ | Production database |
| **psycopg2-binary** | 2.9.7 | Database adapter |

### Dashboard
| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.28.0 | Web framework |
| **Plotly** | 5.14.1 | Interactive visualizations |
| **ReportLab** | 4.0.4 | PDF generation |
| **XlsxWriter** | 3.1.2 | Excel export |

### Machine Learning
| Technology | Version | Purpose |
|------------|---------|---------|
| **Random Forest** | - | Attrition classification |
| **XGBoost** | 2.0.0 | Model comparison |
| **K-Means** | - | Employee clustering |
| **Logistic Regression** | - | Baseline model |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.11+ | [Download](https://www.python.org/downloads/) |
| **PostgreSQL** | 15+ | [Download](https://www.postgresql.org/download/) |
| **Git** | Latest | [Download](https://git-scm.com/) |
| **pip** | Latest | Included with Python |

###  🚀 Installation
### Verify Installations
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check PostgreSQL version
psql --version
```
### Step 1: Clone the Repository
```git clone https://github.com/yourusername/workforce-analytics-platform.git
cd workforce-analytics-platform
```
### Step 2: Create Virtual Environment
``` # Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```
### Step 3: Install Dependencies
``` pip install -r requirements.txt
```
### Step 4: Set Up Database
``` # Create PostgreSQL database
psql -U postgres
CREATE DATABASE workforce_db;
\q
```
### Step 5: Load Data
``` Run the Jupyter notebooks in order:
1.notebooks/02_Feature_Engineering.ipynb
2.notebooks/SQLLoad.ipynb
3.notebooks/03_EDA_Analytics.ipynb
```

##  ⚙️ Configuration
### Environment Variables
Create a .env file in the project root:
```
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=workforce_db
DB_USER=postgres
DB_PASSWORD=your_password

# App Configuration
APP_ENV=production
DEBUG=False```
Edit application.properties with the following content:

```
## Database Configuration
### database/config.py
```
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'workforce_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}
```

## 🏃 Running the Application
### Start the Application

``` # Navigate to project root
cd workforce-analytics-platform

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run the app
streamlit run app.py
```
### Access the Application
```Local URL: http://localhost:8501

Network URL: http://10.75.212.116:8501
```
### Quick Commands
```
# Run with custom port
streamlit run app.py --server.port 8502

# Run with debug mode
streamlit run app.py --logger.level debug
```

## 📁 Project Structure
```
AI_WORKFORCE_INTELLIGENCE/
│
├── 📁 dashboard/                    # 🎨 Dashboard Components
│   ├── 📁 components/
│   │   ├── cards.py                 # 🃏 KPI Card Components
│   │   ├── charts.py                # 📊 Chart Functions
│   │   └── tables.py                # 📋 Table Functions
│   └── 📁 styles/
│       └── theme.py                 # 🎨 Dark/Light Theme
│
├── 📁 database/                     # 🗄️ Database Layer
│   ├── config.py                    # ⚙️ Database Configuration
│   ├── connection.py                # 🔗 PostgreSQL Connection
│   └── queries.py                   # 📝 SQL Queries
│
├── 📁 services/                     # 🛠️ Business Services
│   ├── ml_service.py                # 🤖 Machine Learning Service
│   ├── report_service.py            # 📋 Report Generation
│   └── pdf_service.py               # 📄 PDF with Charts
│
├── 📁 pages/                        # 📄 Streamlit Pages
│   ├── 1_Home.py                    # 🏠 Executive Dashboard
│   ├── 2_ML_Analytics.py            # 🧠 Predictive Analytics
│   ├── 3_Performance_Analytics.py   # 📈 Performance Analytics
│   └── 4_Export.py                  # 📋 Report Center
│
├── 📁 notebooks/                    # 📓 Jupyter Notebooks
│   ├── 02_Feature_Engineering.ipynb # 🔧 Feature Creation
│   ├── 03_EDA_Analytics.ipynb       # 📊 Exploratory Analysis
│   └── SQLLoad.ipynb                # 📤 PostgreSQL Loading
│
├── 📁 sql/                          # 📝 SQL Scripts
│   └── SQL_Business_Analysis.sql    # 📊 Business Queries
│
├── 📁 data/                         # 📂 Data Storage
│   ├── 📁 raw/                      # Raw Data
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   ├── 📁 cleaned/                  # Cleaned Data
│   │   └── employee_cleaned.csv
│   └── 📁 featured/                 # Feature Engineered Data
│       └── employee_featured.csv
│
├── 📁 models/                       # 🧠 Saved ML Models
│   ├── attrition_model.pkl          # 🤖 Attrition Model
│   ├── salary_model.pkl             # 💰 Salary Model
│   └── clusters.pkl                 # 👥 Clustering Model
│
├── 📁 reports/                      # 📊 Generated Reports
│
├── app.py                           # 🚀 Main Entry Point
├── requirements.txt                 # 📦 Python Dependencies
├── .env                             # 🔒 Environment Variables
├── .gitignore                       # 🙈 Git Ignore Rules
└── README.md                        # 📖 Documentation

```


## 📖 Usage Guide
### 1. Navigate the Dashboard

| Page | Purpose |
|------|---------|
| 📊 Executive Dashboard | View KPI cards and charts |
| 🧠 Predictive Analytics | Run ML models and predictions |
| 📈 Performance Analytics | Analyze performance data |
| 📋 Report Center | Export reports |

### 2. Apply Filters
```
- Select **Department** → **Job Role** → **Education** → **Gender** → **Attrition**
- Filters cascade automatically
- Use **Employee Search** for specific employees
- Adjust **Salary** and **Age** sliders
```
### 3. Export Reports
```
- Choose format (CSV, Excel, PDF)
- Click **Export Data**
- Download automatically
```
### 4. Generate Action Plans
```
- Go to **Performance Analytics**
- Select department and number of employees
- Click **Generate Action Plan**
- Download individual plans
```
### 5. Predict Attrition
```
- Go to **Predictive Analytics** → **Predict Attrition**
- Enter employee details
- Click **Predict Attrition Risk**
- View risk level and recommendations
```
### 6. Batch Predictions
```
- Go to **Predictive Analytics** → **Batch Predictions**
- Download template CSV
- Upload employee data
- Click **Predict All Employees**
```
---

## 🖼️ Screenshots

<div align="center">

### 📊 Executive Dashboard

| Dashboard Overview | Key Metrics View |
|:---:|:---:|
| <img width="400" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/9ae59860-4632-43a1-b50b-2b2f6f9e05d4" /> | <img width="400" alt="Key Metrics View" src="https://github.com/user-attachments/assets/08b3ad5f-fa47-4800-8551-7162ad0886c1" /> |

| Filters & Charts |
|:---:|
| <img width="800" alt="Filters and Charts" src="https://github.com/user-attachments/assets/a7b6e04b-0b62-4f67-ae17-9b1c38b9a99d" /> |

*Interactive dashboard showing KPI cards, workforce distribution, cascading filters, and key metrics*

---

### 🧠 Predictive Analytics

| Attrition Insights | Model Performance |
|:---:|:---:|
| <img width="400" alt="Attrition Insights" src="https://github.com/user-attachments/assets/2dc7a8ea-41f9-4cbc-bad1-ae5523a29019" /> | <img width="400" alt="Model Performance" src="https://github.com/user-attachments/assets/9cccd987-bd77-45f7-b066-08709fa748bf" /> |

*Attrition analysis dashboard and model performance metrics (Accuracy, Precision, Recall, F1-Score)*

---

### 📈 Performance Analytics

| Performance Overview | Root Cause Analysis |
|:---:|:---:|
| <img width="400" alt="Performance Overview" src="https://github.com/user-attachments/assets/13e21739-2aea-4054-8ebd-d6414fd826bf" /> | <img width="400" alt="Root Cause Analysis" src="https://github.com/user-attachments/assets/413104a3-38ad-4a82-9dd5-256221bb3e41" /> |

| Risk Assessment | Action Plan Generator |
|:---:|:---:|
| <img width="400" alt="Risk Assessment" src="https://github.com/user-attachments/assets/2f125c1d-0e31-4ccb-add2-9ad69bdc6f69" /> | <img width="400" alt="Action Plan Generator" src="https://github.com/user-attachments/assets/d5883250-4feb-4ca7-9778-20115ccfed89" /> |

*Performance overview, root cause analysis, risk assessment, and action plan generator*

---

### 📋 Report Center

| Report Preview | Export Options |
|:---:|:---:|
| <img width="400" alt="Report Preview"  src="https://github.com/user-attachments/assets/6006246a-337b-402f-a8bd-47cc6dd3e223" /> | <img width="400" alt="Export Options" src="https://github.com/user-attachments/assets/75acd5b1-ed22-4382-81a0-29fc14dbe27f" /> |

*Export reports in CSV, Excel, and PDF formats with visualizations*
*Export reports in CSV, Excel, and PDF formats with visualizations*

---

</div>

 Made with ❤️ by Ranjan  
⭐ If this project will help you, give a star to this repo


