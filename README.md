# CommerceIQ
### AI-Powered Real-Time E-Commerce Intelligence Platform

CommerceIQ is an end-to-end Business Intelligence and Data Analytics platform built to simulate a real-world e-commerce ecosystem. The project combines live transaction generation, interactive dashboards, AI-powered business insights, predictive analytics, and executive reporting into a single analytics solution.

Designed as a portfolio project for Data Analyst and Business Analyst roles, CommerceIQ demonstrates practical skills in data engineering, business intelligence, visualization, automation, and AI integration.

---

# Features

### Executive Dashboard
- Real-time KPI monitoring
- Revenue analysis
- Order analytics
- Customer insights
- Inventory monitoring
- Business health overview

---

### Sales Analytics Dashboard
- Revenue by category
- Brand performance
- Product performance
- Monthly sales trends
- Interactive filters
- Export sales data as CSV

---

### AI Business Insights
Powered by Google Gemini AI.

Automatically generates:

- Executive Summary
- Business Insights
- Risk Analysis
- Business Recommendations
- Future Outlook

using real business metrics from the database.

---

### Live Transaction Engine

Automatically simulates:

- Customer purchases
- Product selection
- Inventory updates
- Order creation
- Revenue generation

making the dashboard behave like a live business environment.

---

### Inventory Monitoring

Tracks:

- Low stock products
- Product sales
- Category performance
- Brand performance

---

### Forecasting

Machine Learning based forecasting includes:

- Sales trend prediction
- Revenue forecasting
- Business trend analysis

---

### Business Analytics

The platform calculates business KPIs including:

- Total Revenue
- Orders
- Customers
- Average Order Value
- Products Sold
- Repeat Customer Rate
- Inventory Status

---

# Project Architecture

```
                    CommerceIQ

                  Streamlit UI
                        │
 ┌───────────────┬──────────────┬──────────────┐
 │               │              │
Executive     Sales         AI Insights
Dashboard     Dashboard

                        │
                  SQLAlchemy ORM
                        │
                    SQLite Database
                        │
    Customers │ Products │ Orders │ Order Items
                        │
             Live Transaction Engine
                        │
               Business Analytics Engine
                        │
                  Machine Learning
```

---

# Project Structure

```
CommerceIQ/
│
├── dashboard.py
├── analytics_dashboard.py
├── sales_dashboard.py
├── ai_dashboard.py
│
├── ai.py
├── analytics.py
├── forecasting.py
├── transaction_engine.py
│
├── models.py
├── database.py
├── config.py
│
├── style.css
├── dashboard_style.css
│
├── requirements.txt
└── README.md
```

---

# Tech Stack

## Programming

- Python 3

## Database

- SQLite
- SQLAlchemy ORM

## Dashboard

- Streamlit
- Plotly

## Data Analysis

- Pandas
- NumPy

## Machine Learning

- Scikit-learn

## AI

- Google Gemini API

## Styling

- HTML
- CSS

---

# Business Metrics

CommerceIQ automatically calculates:

- Revenue
- Total Orders
- Customers
- Average Order Value
- Products Sold
- Repeat Customer Rate
- Inventory Status
- Category Revenue
- Brand Revenue

---

# AI Capabilities

CommerceIQ integrates Generative AI to automatically produce executive business reports based on live business metrics.

The AI analyzes:

- Revenue performance
- Customer behavior
- Inventory status
- Operational risks
- Business opportunities
- Strategic recommendations

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/CommerceIQ.git
```

Move into the project

```bash
cd CommerceIQ
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure your Gemini API key inside the `.env` file.

Run the application

```bash
streamlit run dashboard.py
```

---

# Dashboards

The project includes multiple dashboards:

![Dashboard](preview/preview1.png)

---

# Skills Demonstrated

## Data Analytics

- KPI Development
- Data Cleaning
- Business Reporting
- Revenue Analysis
- Customer Analytics

## Business Intelligence

- Executive Reporting
- Interactive Dashboards
- Business Metrics
- Operational Analytics

## Data Engineering

- Relational Database Design
- SQLAlchemy ORM
- Data Modeling
- Automated Data Generation

## Machine Learning

- Forecasting
- Predictive Analytics

## Artificial Intelligence

- LLM Integration
- Business Insight Generation
- Executive Report Automation

---

# Portfolio Highlights

This project demonstrates the ability to:

- Design relational databases
- Build interactive BI dashboards
- Automate business reporting
- Develop AI-assisted analytics solutions
- Simulate live business operations
- Perform end-to-end data analysis
- Apply machine learning for forecasting
- Create executive-level visualizations

---

# Future Enhancements

Planned improvements include:

- PostgreSQL integration
- Power BI dashboard
- Customer segmentation (RFM Analysis)
- Churn prediction
- Recommendation engine
- Demand forecasting
- Role-based authentication
- Cloud deployment
- REST API integration
- Docker support

---

# Author

**Aditya**

CommerceIQ was developed as a portfolio project showcasing modern Business Intelligence, Data Analytics, Machine Learning and AI-powered analytics using Python.

---

# License

This project is intended for educational and portfolio purposes.
