import os
import re
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import pdfplumber
import docx
from werkzeug.utils import secure_filename
from ai_engine import analyze_with_ai
from report_generator import generate_pdf_report

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath, filename):
    ext = filename.rsplit('.', 1)[1].lower()
    text = ""
    try:
        if ext == 'pdf':
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
        elif ext == 'docx':
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif ext == 'txt':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        else:
            text = f"[File uploaded: {filename}]"
    except Exception as e:
        text = f"Error: {str(e)}"

    return text.strip()



def extract_patient_info(text):
    name = "Unknown"
    age = "Unknown"
    gender = "Unknown"

    # Normalize text
    text = text.replace("\n", " ").strip()

    # ✅ 1. Patient Name label
    name_match = re.search(
        r'Patient Name\s*[:\-]?\s*([A-Za-z .]+)',
        text,
        re.IGNORECASE
    )
    if name_match:
        name = name_match.group(1).strip()

    # ✅ 2. Title-based name (Mr., Ms., etc.)
    if name == "Unknown":
        title_match = re.search(
            r'(Mr\.?|Mrs\.?|Ms\.?)\s+([A-Za-z .]+)',
            text
        )
        if title_match:
            name = title_match.group(2).strip()

    # ✅ 3. First line name fallback (like Yash M. Patel)
    if name == "Unknown":
        lines = text.split(" ")
        possible_name = " ".join(lines[:3])  # first 2-3 words
        if re.match(r'[A-Za-z]+\s+[A-Za-z]+', possible_name):
            name = possible_name.strip()

    # ✅ 4. Age extraction
    age_match = re.search(
        r'Age\s*[:/\-]?\s*(\d{1,3})',
        text,
        re.IGNORECASE
    )
    if age_match:
        age = age_match.group(1)

    # ✅ 5. Gender / Sex extraction
    gender_match = re.search(
        r'(?:Sex|Gender)\s*[:/\-]?\s*(Male|Female|M|F)',
        text,
        re.IGNORECASE
    )
    if gender_match:
        g = gender_match.group(1).upper()
        gender = "Male" if g in ["M", "MALE"] else "Female"

    return name, age, gender





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    report_text = ""
    filename = "Manual Input"

    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            report_text = extract_text_from_file(filepath, filename)

    if not report_text and 'report_text' in request.form:
        report_text = request.form['report_text'].strip()

    if not report_text:
        return jsonify({'error': 'No medical report content provided'}), 400

    patient_name, patient_age, patient_gender = extract_patient_info(report_text)

    result = analyze_with_ai(report_text, patient_name, patient_age, patient_gender)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"mediscan_report_{timestamp}.pdf"
    report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)

    try:
        generate_pdf_report(result, patient_name, patient_age, patient_gender, report_path, filename)
        result['report_file'] = report_filename
    except Exception as e:
        result['report_file'] = None
        result['pdf_error'] = str(e)

    result['patient_name'] = patient_name
    result['patient_age'] = patient_age
    result['patient_gender'] = patient_gender

    return jsonify(result)


@app.route('/download/<filename>')
def download_report(filename):
    path = os.path.join(app.config['REPORTS_FOLDER'], filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/sample')
def get_sample():
    sample = """
PATIENT MEDICAL REPORT
Date: 2026-04-07
Patient: Rahul Sharma | Age: 28 | Gender: Male

COMPLETE BLOOD COUNT (CBC)
Hemoglobin: 15.2 g/dL
WBC Count: 7200 /µL
Platelet Count: 250000 /µL
Hematocrit: 45%
MCV: 88 fL
MCH: 30 pg

BLOOD CHEMISTRY
Glucose (Fasting): 92 mg/dL
HbA1c: 5.2%
Creatinine: 0.9 mg/dL
BUN: 14 mg/dL
eGFR: 95 mL/min

LIPID PROFILE
Total Cholesterol: 170 mg/dL
LDL Cholesterol: 90 mg/dL
HDL Cholesterol: 55 mg/dL
Triglycerides: 110 mg/dL

LIVER FUNCTION
AST: 22 U/L
ALT: 25 U/L
Total Bilirubin: 0.8 mg/dL

THYROID
TSH: 2.1 mIU/L
Free T4: 1.2 ng/dL

URINALYSIS
Protein: Negative
Glucose: Negative
Blood: Negative

VITALS
Blood Pressure: 118/76 mmHg
Heart Rate: 72 bpm
BMI: 22.5
"""
    return jsonify({'sample': sample})

def run_launcher():
    try:
        import run  # this executes run.py logic
        print("[MediScan] run.py executed successfully ✅")
    except Exception as e:
        print("[MediScan] run.py failed:", e)

if __name__ == '__main__':
    run_launcher()  # 🔥 this runs run.py logic

    os.makedirs('uploads', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    port = int(os.getenv('PORT', 5000))

    print(f"🏥 MediScan running on http://localhost:{port}")

    app.run(host='0.0.0.0', port=port, debug=False)