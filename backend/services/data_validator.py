def validate_input(data: dict):
    errors = []

    if not str(data["PatientName"]).strip():
        errors.append("Patient name is required.")

    if not str(data["PatientID"]).strip():
        errors.append("Patient ID is required.")

    if not (10 <= data["Age"] <= 60):
        errors.append("Age must be between 10 and 60")

    if not (70 <= data["SystolicBP"] <= 200):
        errors.append("Systolic BP must be between 70 and 200")

    if not (40 <= data["DiastolicBP"] <= 130):
        errors.append("Diastolic BP must be between 40 and 130")

    if not (4 <= data["BS"] <= 20):
        errors.append("Blood Sugar must be between 4 and 20")

    if not (95 <= data["BodyTemp"] <= 105):
        errors.append("Body Temperature must be between 95 F and 105 F")

    if not (40 <= data["HeartRate"] <= 150):
        errors.append("Heart Rate must be between 40 and 150")

    return errors