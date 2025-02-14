
    CREATE TABLE loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        marital_status TEXT,
        income FLOAT,
        credit_score FLOAT,
        loan_status INTEGER,
        exchange_rate FLOAT,
        income_usd FLOAT,
        loan_income_ratio FLOAT,
        debt_service_ratio FLOAT,
        loan_to_value_ratio FLOAT,
        net_worth FLOAT,
        default_probability FLOAT,
        expected_loss FLOAT,
        sharpe_ratio FLOAT,
        value_at_risk FLOAT,
        credit_score_category TEXT,
        timestamp TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_credit_score ON loans (credit_score);

    CREATE TABLE pipeline_log (
        run_time TEXT,
        status TEXT
    );
    