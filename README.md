# Narrative Atelier: Kokoro Engine

A minimalist narrative workspace built to sharpen authors, not replace them.

## Features (MVP Foundation)

- **Authentication:** Secure session-based login and registration system.
- **Project Management:** Create, organize, and manage multiple writing projects from a central dashboard.
- **Writing Workspace:** A clean, distraction-free environment designed for immersion and focus.
- **Chapter System:** Organize your manuscripts into structured chapters with easy navigation.
- **Autosave Persistence:** Integrated autosave logic to ensure your progress is preserved as you write.
- **Atmospheric Design:** Japanese-inspired minimalist UI featuring muted indigo tones, elegant Noto Serif JP typography, and a calm, literary aesthetic.

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy ORM with SQLite
- **Frontend:** TailwindCSS (via CDN), Vanilla JavaScript, Jinja2 Templates
- **Authentication:** Flask-Login with Werkzeug password hashing

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Initialize the database and run the app:**
   ```bash
   python3 run.py
   ```
   *The database will be automatically initialized on first run.*
3. **Access the app:**
   Open `http://127.0.0.1:5000` in your browser.

## Project Structure

```
/app
    __init__.py     # App initialization and Blueprint registration
    config.py       # Configuration settings
    models.py       # SQLAlchemy models (User, Project, Chapter)
    /auth           # Authentication routes
    /dashboard      # User dashboard routes
    /projects       # Project management routes
    /editor         # Writing workspace routes
    /templates      # Jinja2 templates
    /static         # CSS and JS assets
run.py              # Application entry point
```
