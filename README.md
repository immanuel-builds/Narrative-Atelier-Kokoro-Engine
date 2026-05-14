# Narrative Atelier: Kokoro Engine

A minimalist narrative workspace built to sharpen authors, not replace them.

## Features (MVP Foundation)

- **Authentication:** Session-based login and registration.
- **Project Management:** Create and dismantle narrative observatories (projects).
- **Writing Workspace:** A distraction-free editor with chapter organization and a robust Draft and Versioning system.
- **Draft & Versioning:** Create multiple drafts for each chapter, switch between them, archive "stored memories", and experiment without fear of losing progress.
- **Atmospheric Design:** Japanese-inspired minimalist UI with a focus on typography and calm.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **Database:** SQLite (default for MVP), support for MySQL
- **Frontend:** Jinja2 Templates, Vanilla JavaScript, Modular CSS

## Setup Instructions

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you encounter bcrypt issues, ensure you are using `bcrypt<4.1.0` with `passlib`.*
3. **Initialize the database:**
   ```bash
   python3 init_db.py
   ```
4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Access the app:**
   Open `http://127.0.0.1:8000` in your browser.

## Project Structure

```
/app
    main.py         # App entry point and router registration
    /core           # Config and database setup
    /auth           # Authentication logic and routes
    /dashboard      # Project listing and dashboard
    /projects       # Project CRUD
    /editor         # Writing workspace and chapter management
    /models         # SQLAlchemy models
    /templates      # Jinja2 templates
    /static         # CSS, JS, and images
```
