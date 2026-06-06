CREATE TABLE IF NOT EXISTS patient_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    age INT,
    systolicbp FLOAT,
    diastolicbp FLOAT,
    bs FLOAT,
    body_temp FLOAT,
    heart_rate FLOAT,
    risk_level VARCHAR(50),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);