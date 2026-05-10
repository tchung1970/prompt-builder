# Prompt Builder

A web app for generating detailed AI image prompts. Select options from a visual chip-based UI and let Google Gemini write a rich, coherent prompt ready to paste into any image generator.

**Live demo:** https://ai.tchung.org/prompt-builder/

---

## Features

- Click-to-select chips for subject, style, lighting, mood, palette, composition, and quality
- Portrait and Fantasy/Sci-Fi subjects reveal character options (gender, ethnicity, age, expression)
- Gemini generates a 120–250 word flowing prompt from your selections
- One-click copy to clipboard
- Recommended image models shown alongside the generated prompt

## Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | Vanilla HTML / CSS / JS             |
| Backend    | Python 3.12 + Flask                 |
| AI Model   | Google Gemini `gemini-3.1-flash-lite` |
| Web Server | nginx (reverse proxy → port 5002)   |
| Process    | systemd service                     |

## Setup

**Requirements:** Python 3.12+, a [Google Gemini API key](https://aistudio.google.com/app/apikey)

```bash
pip install flask google-genai
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

Run locally:
```bash
python web.py
# Open http://localhost:5002
```

## API

### `POST /generate`

Accepts JSON with any combination of these fields (at least one required):

| Field        | Description                          |
|--------------|--------------------------------------|
| `subject`    | What the image depicts               |
| `style`      | Art style / medium                   |
| `lighting`   | Lighting conditions                  |
| `mood`       | Mood and atmosphere                  |
| `palette`    | Color palette                        |
| `shot`       | Composition / camera framing         |
| `gender`     | Person gender *(portrait only)*      |
| `ethnicity`  | Person ethnicity *(portrait only)*   |
| `age`        | Person age *(portrait only)*         |
| `expression` | Facial expression *(portrait only)*  |
| `quality`    | Quality / finish modifiers           |
| `details`    | Free-text additional details         |

**Response:**
```json
{ "prompt": "A cinematic portrait of a young Korean woman..." }
```

---

*Written with Claude Opus 4.7 · Powered by Google Gemini API*
