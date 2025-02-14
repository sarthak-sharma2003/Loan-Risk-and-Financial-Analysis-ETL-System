# Loan Data Engineering Project

## Overview
This project processes loan application data using an **ETL (Extract, Transform, Load) pipeline** in Python. The goal is to clean, transform, integrate financial data, and store it in a structured format using SQLite, making it ready for analysis, reporting, and quant finance applications.

## Features
- **Extract:** Loads raw loan application data from CSV and fetches real-time exchange rates via API.
- **Transform:** Cleans and encodes categorical data, calculates income in USD, and derives a credit risk score.
- **Load:** Stores the cleaned and processed data in an **SQL database (SQLite)** for structured querying.
- **Financial Analytics:** Converts income to USD, calculates risk metrics such as `loan_income_ratio`, `debt_service_ratio`, `value_at_risk`, and `sharpe_ratio`.
- **Scalability:** Designed for integration with cloud storage and big data solutions.
- **Visualization:** Generates insights using Seaborn and Matplotlib.

## Technologies Used
- **Python** (Pandas, SQLite3, Requests for API integration)
- **Jupyter Notebooks** (for data exploration and validation)
- **SQLite** (for structured data storage)
- **GitHub** (for version control)
- **API Integration** (for real-time financial data retrieval)
- **Seaborn & Matplotlib** (for data visualization)

## Project Structure
```
Loan-Data-Engineering-Project/
│── data/
│   ├── loan.csv            # Raw dataset
│   ├── cleaned_loan.csv     # Processed dataset
│── notebooks/
│   ├── A1_data_cleaning.ipynb    # Initial cleaning
│   ├── A2_feature_engineering.ipynb  # Structured transformation
│── scripts/
│   ├── etl_pipeline.py   # Python script for ETL
│   ├── loan_data_visualization.py  # Data visualization
│   ├── database_setup.sql  # SQL schema
│── README.md
│── requirements.txt
│── .gitignore
```

## Installation & Setup
### Prerequisites
- Python 3.x
- SQLite3
- Required libraries:
  ```bash
  pip install pandas numpy sqlite3 requests matplotlib seaborn
  ```

### Running the ETL Pipeline
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Loan-Data-Engineering-Project.git
   cd Loan-Data-Engineering-Project
   ```
2. Run the ETL pipeline:
   ```bash
   python scripts/etl_pipeline.py
   ```
3. Run the SQL schema to create the database:
   ```bash
   sqlite3 loans.db < scripts/database_setup.sql
   ```
4. Verify that the SQLite database `loans.db` has been created with processed data.

### Running Data Visualizations
To generate insights, run the visualization script:
```bash
python scripts/loan_data_visualization.py
```

## Example SQL Queries
Once the data is loaded, you can run SQL queries:
```sql
SELECT * FROM loans LIMIT 10;
SELECT AVG(income_usd) FROM loans WHERE loan_status = 1;
SELECT credit_score, credit_risk_score FROM loans ORDER BY credit_risk_score DESC LIMIT 5;
```

## License
This project is licensed under the MIT License.
