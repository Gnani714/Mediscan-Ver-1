# 🏥 MediScan AI — Medical Report Analysis System

An AI-powered web application that simplifies medical reports (CBC, Blood Sugar, Lipid Panel,
Thyroid, Liver, Kidney) into plain-English insights, health scores, and personalized recommendations
using Claude AI (Anthropic).

---

## 📁 Project Structure

```
mediscan_ai/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
│
├── backend/
│   ├── __init__.py
│   ├── analyzer.py             # Claude AI analysis engine
│   ├── pdf_extractor.py        # PDF / TXT text extraction
│   └── reference_ranges.py    # Medical reference ranges database (25+ parameters)
│
└── frontend/
    ├── templates/
    │   └── index.html          # Main HTML page
    └── static/
        ├── css/
        │   └── style.css       # Stylesheet
        └── js/
            └── app.js          # Frontend logic + Chart.js rendering
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- An [Anthropic API key](https://console.anthropic.com/)

### 2. Clone / Extract the project
```bash
cd mediscan_ai
```

### 3. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment
```bash
# Copy the example file
cp .env.example .env

# Open .env and set your API key:
#   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

### 6. Run the application
```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Upload | Extracts text from PDF medical reports automatically |
| 📝 Text Paste | Paste raw report text directly |
| 🤖 AI Analysis | Claude AI extracts all lab parameters |
| 📊 Health Score | 0–100 score with animated ring gauge |
| 🔬 Parameter Table | Every value vs normal range with status tags |
| 📈 Charts | Bar chart + status distribution pie chart |
| 💡 Insights | Plain-English observations about abnormal values |
| 🏃 Recommendations | Personalized diet, exercise & lifestyle tips |
| 💾 JSON Export | Download analysis results as JSON |

---

## 🧪 Supported Report Types

- **CBC** — Hemoglobin, WBC, RBC, Platelets, MCV, MCH, Hematocrit
- **Blood Sugar** — Fasting glucose, Random glucose, HbA1c, Postprandial
- **Lipid Panel** — Total Cholesterol, LDL, HDL, Triglycerides
- **Thyroid** — TSH, T3, T4, Free T3, Free T4
- **Liver Function** — SGPT/ALT, SGOT/AST, Bilirubin, Albumin, ALP
- **Kidney Function** — Creatinine, Urea, BUN, Uric Acid, GFR
- **Electrolytes** — Sodium, Potassium, Calcium
- **Vitamins** — Vitamin D, Vitamin B12, Ferritin

---

## ⚠️ Disclaimer

This application is for **educational purposes only**. It does not provide medical diagnoses
and is not a substitute for professional medical advice. Always consult a qualified healthcare
provider for clinical decisions.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-CORS |
| AI | Anthropic Claude (claude-opus-4-6) |
| PDF | pdfplumber, PyPDF2 |
| Frontend | HTML5, CSS3, Vanilla JS |
| Charts | Chart.js 4 |
| Fonts | DM Sans, DM Serif Display (Google Fonts) |
