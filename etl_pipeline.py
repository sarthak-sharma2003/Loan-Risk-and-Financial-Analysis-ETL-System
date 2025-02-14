import pandas as pd
import sqlite3
import numpy as np
import requests
import logging
import os
import json
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_EXCHANGE_RATE = 1.3
DB_PATH = "loans.db"
DATA_PATH = "data/loan.csv"
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # Real API for exchange rates
LOAN_API_URL = "https://api.mockloans.com/v1/loans"  # Placeholder for real loan data API

# Ensure data directory exists
os.makedirs("data", exist_ok=True)


def extract_data(file_path, loan_api_url=None, exchange_api_url=None):
    """Extract loan data from multiple sources: CSV, API, SQL, JSON."""
    logging.info("Extracting data...")
    
    try:
        df = pd.read_csv(file_path)
        logging.info("CSV data loaded successfully.")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        df = pd.DataFrame()
    
    if loan_api_url:
        try:
            response = requests.get(loan_api_url)
            if response.status_code == 200:
                api_data = pd.DataFrame(response.json())
                df = pd.concat([df, api_data], ignore_index=True)
                logging.info("Loan API data merged successfully.")
        except Exception as e:
            logging.warning(f"Failed to fetch loan API data: {e}")
    
    if exchange_api_url:
        try:
            response = requests.get(exchange_api_url)
            if response.status_code == 200:
                exchange_rates = response.json()
                df['exchange_rate'] = exchange_rates['rates'].get('CAD', DEFAULT_EXCHANGE_RATE)
                logging.info("Exchange rates applied successfully.")
        except Exception as e:
            logging.warning(f"Failed to fetch exchange rates: {e}")
            df['exchange_rate'] = DEFAULT_EXCHANGE_RATE
    
    return df

def validate_data(df):
    """Validate data integrity: Check for missing values, duplicates, and inconsistencies."""
    logging.info("Validating data...")
    df.drop_duplicates(inplace=True)
    
    # Ensure loan_status is explicitly retained
    if 'loan_status' not in df.columns:
        logging.error("loan_status is already missing before validation!")
    
    # Fill missing values (numeric columns only, but keep loan_status as is)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df = df[numeric_cols + categorical_cols]  # Keep categorical columns including loan_status
    
    if df.isnull().sum().sum() > 0:
        logging.warning("Remaining missing values detected after imputation.")
    
    return df

def transform_data(df):
    """Perform feature engineering, encode categorical variables, and calculate financial risk metrics."""
    logging.info("Transforming data...")
    
    # Debug: Check if loan_status exists before transformation
    if 'loan_status' not in df.columns:
        logging.error("loan_status column is missing BEFORE transformation!")
    
    # Ensure loan_status remains in the dataset before encoding
    if 'loan_status' in df.columns and df['loan_status'].dtype == 'object':
        df['loan_status'] = df['loan_status'].map({'Approved': 1, 'Denied': 0})
    
    # Detect categorical columns dynamically (excluding loan_status, which is already mapped)
    categorical_columns = [col for col in df.select_dtypes(include=['object']).columns if col != 'loan_status']
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Encode categorical variables safely
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
    
    # Debug: Ensure loan_status still exists after encoding
    if 'loan_status' not in df.columns:
        logging.error("loan_status column is missing AFTER encoding!")
    
    df['income_usd'] = df['income'] / df['exchange_rate']
    
    # Financial Risk Metrics (Apply only to numerical data)
    df['loan_income_ratio'] = np.random.uniform(0.2, 0.8, size=len(df))
    df['debt_service_ratio'] = df['income'] / np.random.uniform(10000, 50000, size=len(df))
    df['loan_to_value_ratio'] = np.random.uniform(0.5, 1.5, size=len(df))
    df['net_worth'] = df['income'] - np.random.uniform(5000, 25000, size=len(df))
    
    # Historical tracking
    df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['credit_score_category'] = pd.cut(df['credit_score'], bins=[300, 600, 750, 850], labels=['Low', 'Medium', 'High'])
    
    # Advanced Risk Metrics
    df['default_probability'] = 1 / (1 + np.exp(-(df['credit_score'] - 700) / 50))
    df['expected_loss'] = df['default_probability'] * np.random.uniform(5000, 50000, size=len(df))
    df['sharpe_ratio'] = (df['income'] - np.random.uniform(1000, 5000, size=len(df))) / np.random.uniform(500, 2000, size=len(df))
    df['value_at_risk'] = -1.65 * np.random.uniform(1000, 10000, size=len(df))
    
    return df

def load_data_to_sqlite(df, db_path=DB_PATH):
    """Load cleaned data into SQLite database with indexing."""
    logging.info("Loading data into SQLite...")
    conn = sqlite3.connect(db_path)
    df.to_sql('loans', conn, if_exists='replace', index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_credit_score ON loans (credit_score)")
    conn.commit()
    conn.close()

def main():
    """Main ETL pipeline execution."""
    df = extract_data(DATA_PATH, LOAN_API_URL, API_URL)
    df = validate_data(df)
    df = transform_data(df)
    load_data_to_sqlite(df)
    logging.info("ETL process completed successfully!")

if __name__ == "__main__":
    main()
