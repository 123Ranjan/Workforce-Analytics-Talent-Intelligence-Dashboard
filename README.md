AI_WORKFORCE_INTELLIGENCE/
│
├── .venv/
├── .vscode/
│
├── dashboard/                         # Streamlit Application
│   ├── app.py                         # Main Entry Point
│   │
│   ├── pages/
│   │   ├── 1_Home.py
│   │   ├── 2_Employee_Analytics.py
│   │   ├── 3_Attrition_Analytics.py
│   │   ├── 4_Recruitment_Analytics.py
│   │   ├── 5_AI_Assistant.py
│   │   ├── 6_Reports.py
│   │   └── 7_Settings.py
│   │
│   ├── components/
│   │   ├── cards.py
│   │   ├── charts.py
│   │   ├── tables.py
│   │   ├── sidebar.py
│   │   ├── filters.py
│   │   ├── metrics.py
│   │   └── navbar.py
│   │
│   ├── assets/
│   │   ├── logo.png
│   │   ├── styles.css
│   │   └── icons/
│   │
│   └── utils/
│       ├── loader.py
│       ├── formatter.py
│       ├── constants.py
│       └── session.py
│
├── database/
│   ├── connection.py
│   ├── queries.py
│   ├── models.py
│   └── config.py
│
├── services/
│   ├── llm_service.py
│   ├── insight_service.py
│   ├── recommendation_service.py
│   ├── report_service.py
│   ├── analytics_service.py
│   └── employee_service.py
│
├── prompts/
│   ├── executive_summary.txt
│   ├── recommendations.txt
│   ├── chat_prompt.txt
│   └── report_prompt.txt
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── featured/
│   └── processed/
│
├── notebooks/
│   ├── 01_Data_Preparation.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_EDA_Analytics.ipynb
│   ├── 04_SQL_Load.ipynb
│   └── 05_Model_Research.ipynb
│
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   ├── procedures.sql
│   └── SQL_Business_Analysis.sql
│
├── reports/
│   ├── pdf/
│   ├── excel/
│   └── generated/
│
├── docs/
│   ├── architecture.md
│   ├── workflow.md
│   ├── api.md
│   └── screenshots/
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── eda.py
│   └── visualization.py
│
├── tests/
│   ├── test_database.py
│   ├── test_dashboard.py
│   └── test_ai.py
│
├── requirements.txt
├── README.md
├── .env
├── .gitignore
└── LICENSE