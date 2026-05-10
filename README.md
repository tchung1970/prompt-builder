# Prompt Builder

A web app for generating detailed AI image prompts. Select options from a visual chip-based UI and let Google Gemini write a rich, coherent prompt ready to paste into any image generator.

---

## Live Demo

**https://ai.tchung.org/prompt-builder/**

---

## Features

- Click-to-select chips for subject, style, lighting, mood, palette, composition, and quality
- Portrait and Fantasy/Sci-Fi subjects reveal a dedicated **Person / Character** section (see below)
- Gemini generates a 120–250 word flowing prompt from your selections
- One-click copy to clipboard
- Recommended image models shown alongside the generated prompt

### Portrait & Character Options

Selecting **Portrait** as the subject unlocks a Person / Character panel with four additional option groups:

| Option | Choices |
|---|---|
| **Gender** | Male, Female |
| **Ethnicity** | Korean, Japanese, Chinese, Indian, American, British, French, Scandinavian, Latino, Black / African, Middle Eastern |
| **Age** | Child, Teen, 20s, 30s, 40s, 50s, Senior |
| **Expression** | Smiling, Serious, Contemplative, Confident, Mysterious, Laughing, Sad, Surprised |

These options combine with the main style, lighting, mood, and composition choices to produce highly specific character prompts — for example: a contemplative Korean woman in her 30s shot in cinematic lighting with a moody atmosphere and cool blue palette. The panel hides automatically when a non-portrait subject is selected, and any character selections are cleared.

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

## Recommended Image Generation Models

After a prompt is generated, the UI displays a list of suggested image models you can paste it into:

| Model                | Notes                                    |
|----------------------|------------------------------------------|
| Google Nano Banana 2 | Google next-gen creative image model     |
| GPT Image 2          | OpenAI latest image generation model     |
| FLUX.2 Pro           | Next-gen photorealism and fine detail    |
| Midjourney v8.1      | Best for artistic, stylized & cinematic looks |
| Seedream 5 Lite      | Fast, high-quality generation            |

## License

MIT License — see [LICENSE](LICENSE) for details.
