# backend/reference_ranges.py
# Comprehensive medical reference ranges database

REFERENCE_RANGES = {
    # ── Complete Blood Count (CBC) ──────────────────────────────────────────
    "hemoglobin": {
        "male":   {"min": 13.5, "max": 17.5, "unit": "g/dL",   "category": "CBC",         "description": "Protein in red blood cells that carries oxygen"},
        "female": {"min": 12.0, "max": 15.5, "unit": "g/dL",   "category": "CBC",         "description": "Protein in red blood cells that carries oxygen"},
    },
    "hematocrit": {
        "male":   {"min": 41.0, "max": 53.0, "unit": "%",      "category": "CBC",         "description": "Percentage of red blood cells in total blood"},
        "female": {"min": 36.0, "max": 46.0, "unit": "%",      "category": "CBC",         "description": "Percentage of red blood cells in total blood"},
    },
    "wbc": {
        "male":   {"min": 4000, "max": 11000, "unit": "/µL",   "category": "CBC",         "description": "White blood cells that fight infection"},
        "female": {"min": 4000, "max": 11000, "unit": "/µL",   "category": "CBC",         "description": "White blood cells that fight infection"},
    },
    "wbc count": {
        "male":   {"min": 4000, "max": 11000, "unit": "/µL",   "category": "CBC",         "description": "White blood cells that fight infection"},
        "female": {"min": 4000, "max": 11000, "unit": "/µL",   "category": "CBC",         "description": "White blood cells that fight infection"},
    },
    "rbc": {
        "male":   {"min": 4.5,  "max": 5.9,  "unit": "M/µL",  "category": "CBC",         "description": "Red blood cells responsible for oxygen transport"},
        "female": {"min": 4.0,  "max": 5.2,  "unit": "M/µL",  "category": "CBC",         "description": "Red blood cells responsible for oxygen transport"},
    },
    "platelets": {
        "male":   {"min": 150000, "max": 400000, "unit": "/µL","category": "CBC",         "description": "Cells that help blood clot when you bleed"},
        "female": {"min": 150000, "max": 400000, "unit": "/µL","category": "CBC",         "description": "Cells that help blood clot when you bleed"},
    },
    "platelet count": {
        "male":   {"min": 150000, "max": 400000, "unit": "/µL","category": "CBC",         "description": "Cells that help blood clot when you bleed"},
        "female": {"min": 150000, "max": 400000, "unit": "/µL","category": "CBC",         "description": "Cells that help blood clot when you bleed"},
    },
    "mcv": {
        "male":   {"min": 80, "max": 100, "unit": "fL",        "category": "CBC",         "description": "Average size of red blood cells"},
        "female": {"min": 80, "max": 100, "unit": "fL",        "category": "CBC",         "description": "Average size of red blood cells"},
    },
    "mch": {
        "male":   {"min": 27, "max": 33,  "unit": "pg",        "category": "CBC",         "description": "Average amount of hemoglobin per red blood cell"},
        "female": {"min": 27, "max": 33,  "unit": "pg",        "category": "CBC",         "description": "Average amount of hemoglobin per red blood cell"},
    },
    "mchc": {
        "male":   {"min": 32, "max": 36,  "unit": "g/dL",      "category": "CBC",         "description": "Concentration of hemoglobin in red blood cells"},
        "female": {"min": 32, "max": 36,  "unit": "g/dL",      "category": "CBC",         "description": "Concentration of hemoglobin in red blood cells"},
    },

    # ── Blood Sugar ─────────────────────────────────────────────────────────
    "fasting blood sugar": {
        "male":   {"min": 70, "max": 99,  "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose after fasting overnight"},
        "female": {"min": 70, "max": 99,  "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose after fasting overnight"},
    },
    "blood sugar fasting": {
        "male":   {"min": 70, "max": 99,  "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose after fasting overnight"},
        "female": {"min": 70, "max": 99,  "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose after fasting overnight"},
    },
    "random blood sugar": {
        "male":   {"min": 70, "max": 140, "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose at any time of day"},
        "female": {"min": 70, "max": 140, "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose at any time of day"},
    },
    "hba1c": {
        "male":   {"min": 4.0, "max": 5.6,"unit": "%",         "category": "Blood Sugar", "description": "Average blood sugar over the past 2-3 months"},
        "female": {"min": 4.0, "max": 5.6,"unit": "%",         "category": "Blood Sugar", "description": "Average blood sugar over the past 2-3 months"},
    },
    "postprandial blood sugar": {
        "male":   {"min": 70, "max": 140, "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose 2 hours after eating"},
        "female": {"min": 70, "max": 140, "unit": "mg/dL",     "category": "Blood Sugar", "description": "Blood glucose 2 hours after eating"},
    },

    # ── Lipid Panel ─────────────────────────────────────────────────────────
    "total cholesterol": {
        "male":   {"min": 0,  "max": 200, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Total fat-like substances in blood"},
        "female": {"min": 0,  "max": 200, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Total fat-like substances in blood"},
    },
    "ldl": {
        "male":   {"min": 0,  "max": 130, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Bad cholesterol that can clog arteries"},
        "female": {"min": 0,  "max": 130, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Bad cholesterol that can clog arteries"},
    },
    "ldl cholesterol": {
        "male":   {"min": 0,  "max": 130, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Bad cholesterol that can clog arteries"},
        "female": {"min": 0,  "max": 130, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Bad cholesterol that can clog arteries"},
    },
    "hdl": {
        "male":   {"min": 40, "max": 999, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Good cholesterol that protects the heart"},
        "female": {"min": 50, "max": 999, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Good cholesterol that protects the heart"},
    },
    "hdl cholesterol": {
        "male":   {"min": 40, "max": 999, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Good cholesterol that protects the heart"},
        "female": {"min": 50, "max": 999, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Good cholesterol that protects the heart"},
    },
    "triglycerides": {
        "male":   {"min": 0,  "max": 150, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Type of fat in blood from excess calories"},
        "female": {"min": 0,  "max": 150, "unit": "mg/dL",     "category": "Lipid Panel", "description": "Type of fat in blood from excess calories"},
    },

    # ── Thyroid ─────────────────────────────────────────────────────────────
    "tsh": {
        "male":   {"min": 0.4, "max": 4.0, "unit": "mIU/L",   "category": "Thyroid",     "description": "Hormone that controls thyroid function"},
        "female": {"min": 0.4, "max": 4.0, "unit": "mIU/L",   "category": "Thyroid",     "description": "Hormone that controls thyroid function"},
    },
    "t3": {
        "male":   {"min": 80,  "max": 200, "unit": "ng/dL",   "category": "Thyroid",     "description": "Active thyroid hormone controlling metabolism"},
        "female": {"min": 80,  "max": 200, "unit": "ng/dL",   "category": "Thyroid",     "description": "Active thyroid hormone controlling metabolism"},
    },
    "t4": {
        "male":   {"min": 5.0, "max": 12.0,"unit": "µg/dL",   "category": "Thyroid",     "description": "Storage form of thyroid hormone"},
        "female": {"min": 5.0, "max": 12.0,"unit": "µg/dL",   "category": "Thyroid",     "description": "Storage form of thyroid hormone"},
    },
    "free t3": {
        "male":   {"min": 2.3, "max": 4.2, "unit": "pg/mL",   "category": "Thyroid",     "description": "Unbound active thyroid hormone"},
        "female": {"min": 2.3, "max": 4.2, "unit": "pg/mL",   "category": "Thyroid",     "description": "Unbound active thyroid hormone"},
    },
    "free t4": {
        "male":   {"min": 0.8, "max": 1.8, "unit": "ng/dL",   "category": "Thyroid",     "description": "Unbound storage thyroid hormone"},
        "female": {"min": 0.8, "max": 1.8, "unit": "ng/dL",   "category": "Thyroid",     "description": "Unbound storage thyroid hormone"},
    },

    # ── Liver Function ───────────────────────────────────────────────────────
    "sgpt": {
        "male":   {"min": 7,  "max": 56,  "unit": "U/L",      "category": "Liver",       "description": "Enzyme that indicates liver health (ALT)"},
        "female": {"min": 7,  "max": 45,  "unit": "U/L",      "category": "Liver",       "description": "Enzyme that indicates liver health (ALT)"},
    },
    "alt": {
        "male":   {"min": 7,  "max": 56,  "unit": "U/L",      "category": "Liver",       "description": "Liver enzyme — high levels may indicate liver stress"},
        "female": {"min": 7,  "max": 45,  "unit": "U/L",      "category": "Liver",       "description": "Liver enzyme — high levels may indicate liver stress"},
    },
    "sgot": {
        "male":   {"min": 10, "max": 40,  "unit": "U/L",      "category": "Liver",       "description": "Enzyme found in liver and heart (AST)"},
        "female": {"min": 10, "max": 35,  "unit": "U/L",      "category": "Liver",       "description": "Enzyme found in liver and heart (AST)"},
    },
    "ast": {
        "male":   {"min": 10, "max": 40,  "unit": "U/L",      "category": "Liver",       "description": "Liver enzyme that can signal damage"},
        "female": {"min": 10, "max": 35,  "unit": "U/L",      "category": "Liver",       "description": "Liver enzyme that can signal damage"},
    },
    "bilirubin": {
        "male":   {"min": 0.2, "max": 1.2,"unit": "mg/dL",    "category": "Liver",       "description": "Waste product from red blood cell breakdown"},
        "female": {"min": 0.2, "max": 1.2,"unit": "mg/dL",    "category": "Liver",       "description": "Waste product from red blood cell breakdown"},
    },
    "alkaline phosphatase": {
        "male":   {"min": 44, "max": 147, "unit": "U/L",      "category": "Liver",       "description": "Enzyme linked to liver and bone health"},
        "female": {"min": 44, "max": 147, "unit": "U/L",      "category": "Liver",       "description": "Enzyme linked to liver and bone health"},
    },
    "albumin": {
        "male":   {"min": 3.5, "max": 5.0,"unit": "g/dL",     "category": "Liver",       "description": "Protein made by liver — reflects nutrition status"},
        "female": {"min": 3.5, "max": 5.0,"unit": "g/dL",     "category": "Liver",       "description": "Protein made by liver — reflects nutrition status"},
    },

    # ── Kidney Function ──────────────────────────────────────────────────────
    "creatinine": {
        "male":   {"min": 0.7, "max": 1.3,"unit": "mg/dL",    "category": "Kidney",      "description": "Waste product filtered by kidneys"},
        "female": {"min": 0.6, "max": 1.1,"unit": "mg/dL",    "category": "Kidney",      "description": "Waste product filtered by kidneys"},
    },
    "urea": {
        "male":   {"min": 7,  "max": 25,  "unit": "mg/dL",    "category": "Kidney",      "description": "Nitrogen waste product from protein metabolism"},
        "female": {"min": 7,  "max": 25,  "unit": "mg/dL",    "category": "Kidney",      "description": "Nitrogen waste product from protein metabolism"},
    },
    "blood urea nitrogen": {
        "male":   {"min": 7,  "max": 20,  "unit": "mg/dL",    "category": "Kidney",      "description": "Nitrogen in blood from protein breakdown"},
        "female": {"min": 7,  "max": 20,  "unit": "mg/dL",    "category": "Kidney",      "description": "Nitrogen in blood from protein breakdown"},
    },
    "uric acid": {
        "male":   {"min": 3.5, "max": 7.2,"unit": "mg/dL",    "category": "Kidney",      "description": "Waste from purine breakdown — high levels cause gout"},
        "female": {"min": 2.6, "max": 6.0,"unit": "mg/dL",    "category": "Kidney",      "description": "Waste from purine breakdown — high levels cause gout"},
    },
    "gfr": {
        "male":   {"min": 60, "max": 999, "unit": "mL/min",   "category": "Kidney",      "description": "Rate at which kidneys filter blood"},
        "female": {"min": 60, "max": 999, "unit": "mL/min",   "category": "Kidney",      "description": "Rate at which kidneys filter blood"},
    },

    # ── Electrolytes ─────────────────────────────────────────────────────────
    "sodium": {
        "male":   {"min": 136, "max": 145,"unit": "mEq/L",    "category": "Electrolytes","description": "Mineral that regulates fluid balance"},
        "female": {"min": 136, "max": 145,"unit": "mEq/L",    "category": "Electrolytes","description": "Mineral that regulates fluid balance"},
    },
    "potassium": {
        "male":   {"min": 3.5, "max": 5.0,"unit": "mEq/L",    "category": "Electrolytes","description": "Mineral important for heart and muscle function"},
        "female": {"min": 3.5, "max": 5.0,"unit": "mEq/L",    "category": "Electrolytes","description": "Mineral important for heart and muscle function"},
    },
    "calcium": {
        "male":   {"min": 8.5, "max": 10.5,"unit": "mg/dL",   "category": "Electrolytes","description": "Mineral essential for bones and muscle contraction"},
        "female": {"min": 8.5, "max": 10.5,"unit": "mg/dL",   "category": "Electrolytes","description": "Mineral essential for bones and muscle contraction"},
    },

    # ── Vitamins ─────────────────────────────────────────────────────────────
    "vitamin d": {
        "male":   {"min": 30, "max": 100, "unit": "ng/mL",    "category": "Vitamins",    "description": "Vitamin for bone health and immune function"},
        "female": {"min": 30, "max": 100, "unit": "ng/mL",    "category": "Vitamins",    "description": "Vitamin for bone health and immune function"},
    },
    "vitamin b12": {
        "male":   {"min": 200, "max": 900,"unit": "pg/mL",    "category": "Vitamins",    "description": "Vitamin for nerve function and red blood cell production"},
        "female": {"min": 200, "max": 900,"unit": "pg/mL",    "category": "Vitamins",    "description": "Vitamin for nerve function and red blood cell production"},
    },
    "ferritin": {
        "male":   {"min": 12, "max": 300, "unit": "ng/mL",    "category": "Vitamins",    "description": "Stored iron in the body"},
        "female": {"min": 12, "max": 150, "unit": "ng/mL",    "category": "Vitamins",    "description": "Stored iron in the body"},
    },
}


def get_status(param_name: str, value: float, gender: str = "male") -> dict:
    """Return status, range string, and ref dict for a parameter value."""
    key    = param_name.lower().strip()
    gender = gender.lower()

    if key not in REFERENCE_RANGES:
        return {"status": "Unknown", "range": "—", "ref": None}

    ref    = REFERENCE_RANGES[key][gender]
    lo, hi = ref["min"], ref["max"]
    margin = (hi - lo) * 0.10

    if value < lo:
        status = "Borderline" if value >= lo - margin else "Low"
    elif value > hi:
        status = "Borderline" if value <= hi + margin else "High"
    else:
        status = "Normal"

    return {
        "status": status,
        "range":  f"{lo}–{hi} {ref['unit']}",
        "ref":    ref,
    }


def compute_health_score(parameters: list) -> int:
    """Compute 0-100 health score from a list of analysed parameters."""
    if not parameters:
        return 50
    weights = {"Normal": 1.0, "Borderline": 0.6, "Low": 0.3, "High": 0.3, "Unknown": 0.7}
    total   = sum(weights.get(p.get("status", "Unknown"), 0.7) for p in parameters)
    return max(0, min(100, round((total / len(parameters)) * 100)))
