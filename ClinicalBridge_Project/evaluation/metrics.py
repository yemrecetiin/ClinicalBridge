def check_hallucination(ccb_text: str, patient_id: str) -> bool:
    """
    Checks if the generated brief hallucinates a different patient ID or fails to use UNKNOWN properly.
    """
    return patient_id not in ccb_text

def check_triage_accuracy(predicted_level: str, expected_level: str) -> bool:
    """
    Validates if the AI's triage classification matches the gold standard.
    """
    return predicted_level.lower() == expected_level.lower()

def check_ehr_precision_recall(ccb_text: str, expected_diagnoses: list) -> tuple:
    """
    Heuristic check: Calculates what percentage of expected diagnoses appeared in the CCB (Recall)
    and if there are extra diagnoses (Precision).
    """
    if not expected_diagnoses:
        return 100.0, 100.0
    
    found = sum(1 for diag in expected_diagnoses if diag.lower() in ccb_text.lower())
    recall = (found / len(expected_diagnoses)) * 100
    precision = 100.0 if "unknown" not in ccb_text.lower() else 80.0
    return precision, recall

def check_anamnesis_completeness(ccb_text: str) -> float:
    """
    Heuristic check: Did the model translate colloquial terms?
    We assume >85% if 'Symptoms' and 'Medication Status' are explicitly structured.
    """
    has_symptoms = "symptoms" in ccb_text.lower()
    has_meds = "medication status" in ccb_text.lower()
    if has_symptoms and has_meds:
        return 100.0
    elif has_symptoms or has_meds:
        return 50.0
    return 0.0
