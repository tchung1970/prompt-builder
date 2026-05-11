# Prompt Builder

A web app for generating detailed AI image prompts by selecting options from a visual chip-based UI. Selections are sent to Google Gemini, which writes a rich, coherent prompt ready to paste into any image generator.

**Server (English):** https://ai.tchung.org/prompt-builder/
**Server (Korean):** https://ai.tchung.org/prompt-builder-ko/
**GitHub:** https://github.com/tchung1970/prompt-builder

---

## Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | Vanilla HTML / CSS / JS             |
| Backend    | Python 3.12 + Flask                 |
| AI Model   | Google Gemini `gemini-3.1-flash-lite` |
| Web Server | nginx (reverse proxy → port 5002)   |
| Process    | systemd service                     |

---

## Files

```
/var/www/html/prompt-builder/       ← server
~/claude/prompt-builder/            ← local copy
├── index.html                      frontend UI
├── web.py                          Flask backend
├── .env                            API keys
└── README.md                       this file
```

---

## API

### `GET /`
Serves `index.html`.

### `POST /generate`
Accepts a JSON body with any combination of the fields below. At least one field must be non-empty.

**Request fields:**

| Field        | Description                              |
|--------------|------------------------------------------|
| `subject`    | What the image depicts                   |
| `style`      | Art style / medium                       |
| `lighting`   | Lighting conditions                      |
| `mood`       | Mood and atmosphere                      |
| `palette`    | Color palette                            |
| `shot`       | Composition / camera framing             |
| `gender`     | Person gender *(portrait only)*          |
| `ethnicity`  | Person ethnicity *(portrait only)*       |
| `age`        | Person age *(portrait only)*             |
| `expression` | Facial expression *(portrait only)*      |
| `quality`    | Quality / finish modifiers               |

**Success response:**
```json
{ "prompt": "A cinematic portrait of a young Korean woman..." }
```

**Error response:**
```json
{ "error": "Please select at least one option." }
```

---

## UI Option Groups

### Subject
Portrait, Landscape, Architecture, Fantasy/Sci-Fi, Abstract, Animal, Still Life, Vehicle

> Selecting **Portrait** reveals the Person/Character section.

### Person / Character *(portrait only)*

**Gender:** Male, Female

**Ethnicity:** Korean, Japanese, Chinese, Indian, American, British, French, Scandinavian, Latino, Black/African, Middle Eastern

**Age:** Child, Teen, 20s, 30s, 40s, 50s, Senior

**Expression:** Smiling, Serious, Contemplative, Confident, Mysterious, Laughing, Sad, Surprised

### Art Style
Photorealistic, Cinematic, Oil Painting, Watercolor, Digital Art, Anime/Manga, Pencil Sketch, Vintage/Film, Concept Art

### Lighting
Golden Hour, Studio, Dramatic, Moody/Overcast, Night/Neon, Backlit, Natural/Soft, Harsh Sunlight

### Mood & Atmosphere
Serene, Dramatic, Mysterious, Joyful, Dark, Ethereal, Epic, Romantic

### Color Palette
Warm Tones, Cool Blues, Monochrome, Vibrant, Pastel, Earth Tones, Neon/Cyberpunk, Desaturated

### Composition
Close-Up, Medium Shot, Full Body, Wide Angle, Aerial, Macro, Cinematic Wide, Low Angle

### Quality & Finish
Ultra Detail, Film Grain, Professional

---

## Recommended Models

Displayed below the generated prompt (informational, no links):

| Model               | Description                          |
|---------------------|--------------------------------------|
| Google Nano Banana 2 | Google next-gen creative image model |
| GPT Image 2         | OpenAI latest image generation       |
| FLUX.2 Pro          | Next-gen photorealism and fine detail|
| Midjourney v8.1     | Artistic, stylized & cinematic       |
| Seedream 5 Lite     | Fast, high-quality generation        |

---

## Deployment

### nginx (`/etc/nginx/sites-enabled/default`)
```nginx
location /prompt-builder/ {
    proxy_pass http://127.0.0.1:5002/;
    proxy_http_version 1.1;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_read_timeout 60s;
    proxy_send_timeout 60s;
}
```

### systemd (`/etc/systemd/system/prompt-builder.service`)
```ini
[Unit]
Description=Prompt Builder Web App
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/html/prompt-builder
ExecStart=/usr/bin/python3 /var/www/html/prompt-builder/web.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Common commands
```bash
sudo systemctl status prompt-builder
sudo systemctl restart prompt-builder
sudo systemctl stop prompt-builder
sudo journalctl -u prompt-builder -f
```

### `.env` location and format

Stored at `/root/.env` (not in the web root) so it is never accidentally served by nginx.
`web.py` searches for `.env` in this order: app directory → `/root/.env`.

```
GEMINI_API_KEY=your_key_here
```

---

*Written with Claude Opus 4.7 · Powered by Google Gemini API*
