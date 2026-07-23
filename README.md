# 📊 Workforce Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-1.3+-orange.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.14+-blueviolet.svg?style=for-the-badge&logo=plotly&logoColor=white)

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
- [Contributing](#-contributing)
- [Contact](#-contact)

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

## 🚀 Installation
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

## ⚙️ Configuration
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
