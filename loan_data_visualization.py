import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
db_path = "loans.db"
conn = sqlite3.connect(db_path)

# Load data
df = pd.read_sql_query("SELECT * FROM loans", conn)
conn.close()

# Check for missing columns
expected_columns = ['loan_status', 'credit_score', 'income_usd', 'debt_service_ratio', 'default_probability']
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"⚠️ Warning: Missing columns in the dataset: {missing_columns}")
else:
    # Ensure correct column names after encoding
    if 'loan_status' in df.columns:
        df['loan_status'] = df['loan_status'].map({1: "Approved", 0: "Denied"})
    
    if 'credit_score_category' in df.columns:
        df['credit_score_category'] = df['credit_score_category'].astype(str)
    
    # Set style
    sns.set(style="whitegrid")
    
    # Loan Approval vs. Denial Count
    plt.figure(figsize=(6,4))
    sns.countplot(x='loan_status', data=df, palette='coolwarm')
    plt.title("Loan Approval vs. Denial Count")
    plt.xlabel("Loan Status")
    plt.ylabel("Count")
    plt.show()
    
    # Credit Score Distribution
    plt.figure(figsize=(6,4))
    sns.histplot(df['credit_score'], bins=30, kde=True, color='blue')
    plt.title("Credit Score Distribution")
    plt.xlabel("Credit Score")
    plt.ylabel("Frequency")
    plt.show()
    
    # Debt-to-Income Ratio vs. Loan Status
    plt.figure(figsize=(6,4))
    sns.boxplot(x='loan_status', y='debt_service_ratio', data=df, palette='pastel')
    plt.title("Debt Service Ratio vs. Loan Status")
    plt.xlabel("Loan Status")
    plt.ylabel("Debt Service Ratio")
    plt.show()
    
    # Credit Risk Score vs. Income (Correlation)
    plt.figure(figsize=(6,4))
    sns.scatterplot(x='income_usd', y='credit_score', hue='loan_status', data=df, palette='coolwarm', alpha=0.7)
    plt.title("Credit Score vs. Income")
    plt.xlabel("Income (USD)")
    plt.ylabel("Credit Score")
    plt.show()
    
    # Loan Default Probability Distribution
    plt.figure(figsize=(6,4))
    sns.kdeplot(df['default_probability'], shade=True, color='red')
    plt.title("Loan Default Probability Distribution")
    plt.xlabel("Default Risk Probability")
    plt.ylabel("Density")
    plt.show()
    
    print("✅ Data visualization completed!")
