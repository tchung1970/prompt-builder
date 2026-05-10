#!/usr/bin/env python3
"""
prompt-builder — Generate image prompts from selected options.
"""

import os
from pathlib import Path

app_dir = Path(__file__).parent
env_file = next((p for p in [app_dir / ".env", Path("/root/.env")] if p.exists()), None)
if env_file and env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

from flask import Flask, request, jsonify, send_from_directory
from google import genai

app = Flask(__name__)

MODEL = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = """\
You are an expert prompt engineer for AI image generation models (Stable Diffusion, Midjourney, FLUX, etc.).

Given a set of user-selected parameters, generate a single highly detailed image generation prompt.

Rules:
- Incorporate all provided parameters naturally and coherently
- Add rich, specific details: textures, materials, spatial relationships, fine details
- Use vivid and precise language throughout
- Write as a single flowing paragraph — no lists, no headers, no labels
- Aim for 120–250 words
- Output ONLY the prompt text, nothing else
"""


def build_user_message(options: dict) -> str:
    lines = ["Generate a detailed image prompt with these parameters:"]
    labels = [
        ("subject",  "Subject"),
        ("style",    "Art Style"),
        ("lighting", "Lighting"),
        ("mood",     "Mood / Atmosphere"),
        ("palette",  "Color Palette"),
        ("shot",     "Composition / Shot"),
        ("gender",   "Gender"),
        ("ethnicity", "Ethnicity"),
        ("age",      "Age"),
        ("expression", "Expression"),
        ("quality",  "Quality / Finish"),
    ]
    for key, label in labels:
        val = options.get(key, "").strip()
        if val:
            lines.append(f"{label}: {val}")
    return "\n".join(lines)


def generate_prompt(options: dict) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    user_msg = build_user_message(options)
    response = client.models.generate_content(
        model=MODEL,
        contents=[{"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_msg}]}],
    )
    return response.text.strip()


@app.route("/")
def index():
    return send_from_directory(Path(__file__).parent, "index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    options = {
        "subject":  data.get("subject", ""),
        "style":    data.get("style", ""),
        "lighting": data.get("lighting", ""),
        "mood":     data.get("mood", ""),
        "palette":  data.get("palette", ""),
        "shot":     data.get("shot", ""),
        "gender":     data.get("gender", ""),
        "ethnicity":  data.get("ethnicity", ""),
        "age":        data.get("age", ""),
        "expression": data.get("expression", ""),
        "quality":  data.get("quality", ""),
    }
    if not any(v.strip() for v in options.values()):
        return jsonify({"error": "Please select at least one option."}), 400
    try:
        prompt_text = generate_prompt(options)
        return jsonify({"prompt": prompt_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════╗
║         PROMPT  BUILDER              ║
║         Web Application              ║
╚══════════════════════════════════════╝

Provider: Google Gemini API
Model:    gemini-3.1-flash-lite
Port:     5002

Open http://localhost:5002 in your browser
""")
    app.run(debug=True, port=5002)
