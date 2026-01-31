def calculate_risk(finding):
    technique = finding["technique"]

    if "UNION" in technique:
        return "Critical"
    if "Time-based" in technique:
        return "High"
    if "Error-based" in technique:
        return "High"
    if "Boolean" in technique:
        return "Medium"

    return "Low"