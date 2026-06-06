from database.db_connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name VARCHAR(100) NOT NULL,
            patient_id VARCHAR(50) NOT NULL,
            age INT,
            systolic_bp FLOAT,
            diastolic_bp FLOAT,
            bs FLOAT,
            body_temp FLOAT,
            heart_rate FLOAT,
            risk_level VARCHAR(50),
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) 
    """)

    conn.commit()
    cursor.close()
    conn.close()

def insert_record(data: dict, result: dict):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO patient_records (
            patient_name, patient_id, age, systolic_bp, diastolic_bp,
            bs, body_temp, heart_rate, risk_level, recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = (
        data["PatientName"],
        data["PatientID"],
        data["Age"],
        data["SystolicBP"],
        data["DiastolicBP"],
        data["BS"],
        data["BodyTemp"],
        data["HeartRate"],
        result["risk_level"],
        result["recommendation"]
    )

    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

def get_all_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT patient_name, patient_id, age, systolic_bp, diastolic_bp,
               bs, body_temp, heart_rate, risk_level, recommendation, created_at
        FROM patient_records
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_records_by_patient_id(patient_id, limit=3):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT patient_name, patient_id, age, systolic_bp, diastolic_bp,
               bs, body_temp, heart_rate, risk_level, recommendation, created_at
        FROM patient_records
        WHERE patient_id = %s
        ORDER BY created_at DESC
        LIMIT %s
    """

    cursor.execute(query, (patient_id, limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
