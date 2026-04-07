# backend/analyzer.py  —  MediScan AI  (Groq Free API edition)
#
# Why Groq instead of Hugging Face?
#   - HF router URLs keep changing and returning 404/410 errors
#   - Groq is 100% free (no credit card needed), stable, and very fast
#   - Uses OpenAI-compatible /v1/chat/completions format
#   - Runs Llama-3 which produces much better structured JSON
#
# Free Groq account: https://console.groq.com
# Get your key:      https://console.groq.com/keys
#
# Change in .env:
#   HF_TOKEN=...  →  GROQ_API_KEY=gsk_...

import json
import re
import requests
from backend.reference_ranges import get_status, compute_health_score

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "gemma2-9b-it",
]

SYSTEM_PROMPT = """You are MediScan AI, an expert medical report analysis assistant.
Analyze the medical report provided by the user and return ONLY a valid JSON object.
Do NOT include any text, explanation, or markdown before or after the JSON.

Return exactly this JSON structure:
{
  "patientSummary": "2-3 sentence plain-English overview of the patient health",
  "report_type": "CBC|Lipid Panel|Blood Sugar|Thyroid|Liver Function|Kidney Function|Comprehensive|Other",
  "parameters": [
    {
      "name": "parameter name as in the report",
      "value_raw": "value with unit as written",
      "value_numeric": <number or null>,
      "unit": "unit string",
      "status": "Normal|High|Low|Borderline|Unknown",
      "normal_range": "normal range string",
      "plain_explanation": "one sentence a non-medical person can understand"
    }
  ],
  "insights": [
    {
      "type": "info|warning|danger",
      "text": "plain-language health insight"
    }
  ],
  "recommendations": [
    {
      "icon": "single emoji",
      "category": "diet|exercise|lifestyle|medical|hydration",
      "text": "specific actionable recommendation"
    }
  ],
  "consult_doctor": true|false
}

Rules:
- Extract EVERY numerical lab value you find in the report
- Use simple everyday language, no medical jargon
- Provide 3-8 parameters, 2-4 insights, 3-5 recommendations
- Never diagnose a disease, educational insights only
- Set consult_doctor to true if any values are critically abnormal
- Output ONLY the JSON object, nothing else"""


def _call_groq(messages: list, groq_api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type":  "application/json",
    }
    last_error = None

    for model in GROQ_MODELS:
        payload = {
            "model":       model,
            "messages":    messages,
            "max_tokens":  2048,
            "temperature": 0.1,
            "stream":      False,
        }
        try:
            print(f"   Trying: {model} ...")
            resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)

            if resp.status_code == 401:
                raise RuntimeError(
                    "Invalid Groq API key. "
                    "Please set GROQ_API_KEY in your .env file. "
                    "Get a free key at https://console.groq.com/keys"
                )
            if resp.status_code == 429:
                print(f"   Rate limited on {model}, trying next...")
                last_error = RuntimeError(f"{model} rate limited")
                continue
            if resp.status_code == 404:
                print(f"   {model} not found, trying next...")
                last_error = RuntimeError(f"{model} not found")
                continue
            if not resp.ok:
                try:
                    msg = resp.json().get("error", {}).get("message", resp.text[:200])
                except Exception:
                    msg = resp.text[:200]
                print(f"   {model} HTTP {resp.status_code}: {msg}")
                last_error = RuntimeError(f"HTTP {resp.status_code}: {msg}")
                continue

            content = resp.json()["choices"][0]["message"]["content"]
            print(f"   Success with {model}")
            return content

        except RuntimeError:
            raise
        except Exception as e:
            print(f"   {model} exception: {e}")
            last_error = e

    raise RuntimeError(
        f"All Groq models failed. Last error: {last_error}. "
        "Please verify your GROQ_API_KEY at https://console.groq.com/keys"
    )


def _parse_json(raw: str) -> dict:
    clean = re.sub(r"```json|```", "", raw).strip()
    brace = clean.find("{")
    if brace > 0:
        clean = clean[brace:]
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{.*\}', clean, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError("Could not parse JSON from model response. Please try again.")


def analyze_report(report_text: str, age: int, gender: str, groq_api_key: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Patient: {age}-year-old {gender}\n\n"
                f"Medical Report:\n{report_text}\n\n"
                "Extract all parameters and return the complete JSON analysis."
            ),
        },
    ]

    raw    = _call_groq(messages, groq_api_key)
    result = _parse_json(raw)

    for param in result.get("parameters", []):
        if param.get("value_numeric") is not None:
            ref = get_status(param["name"], param["value_numeric"], gender)
            if ref["status"] != "Unknown":
                param["status"]       = ref["status"]
                param["normal_range"] = ref["range"]

    score = compute_health_score(result.get("parameters", []))
    result["health_score"]  = score
    result["health_status"] = (
        "Good"            if score >= 85 else
        "Moderate"        if score >= 60 else
        "Needs Attention"
    )

    return result
