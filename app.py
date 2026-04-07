# app.py  —  MediScan AI  (Groq edition)
#
# Changed from HF version:
#   os.getenv("HF_TOKEN")      →  os.getenv("GROQ_API_KEY")
#   error message              →  mentions Groq instead of HF

import os
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from backend.pdf_extractor import extract_text
from backend.analyzer import analyze_report

load_dotenv()

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)
CORS(app)

UPLOAD_FOLDER  = "uploads"
ALLOWED_EXTS   = {"pdf", "txt"}
MAX_CONTENT_MB = 16

app.config["UPLOAD_FOLDER"]      = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_MB * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key or groq_key == "your-groq-api-key-here":
        return jsonify({
            "error": (
                "Groq API key not configured. "
                "Please set GROQ_API_KEY in your .env file. "
                "Get a FREE key at https://console.groq.com/keys"
            )
        }), 500

    age    = request.form.get("age",    35,     type=int)
    gender = request.form.get("gender", "male").lower()
    text   = request.form.get("text",   "").strip()

    file = request.files.get("file")
    if file and file.filename and _allowed(file.filename):
        filename  = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        try:
            text = extract_text(save_path)
        finally:
            os.remove(save_path)

    if not text:
        return jsonify({"error": "No report text found. Please paste text or upload a file."}), 400

    try:
        result = analyze_report(text, age, gender, groq_key)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "MediScan AI (Groq)"})


if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"\n  MediScan AI (Groq) running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
