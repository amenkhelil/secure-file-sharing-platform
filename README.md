# SecureShare — Secure File Sharing Platform

A simple, self-hosted Flask web application that lets users upload, manage, and securely share files via private share links.

---

## Features

- **User accounts** — register, log in, and log out securely
- **File uploads** — drag-and-drop or click-to-browse; supports PDF, DOCX, TXT, PNG, JPG, JPEG (max 20 MB)
- **File management** — view, download, and delete your own files
- **Secure share links** — generate a private token link for any file; anyone with the link can download it without logging in
- **Revoke sharing** — remove a share link at any time to make a file private again
- **Profile management** — update your display name
- **Responsive UI** — works on desktop and mobile

---

## Tech Stack

- **Backend:** Python 3, Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite (file: `database/database.db`)
- **Frontend:** Vanilla HTML, CSS, JavaScript (no frameworks)

---

## Project Structure

```
secure-file-sharing-platform/
├── app.py                  # Flask app, all routes
├── requirements.txt        # Python dependencies
├── models/
│   └── models.py           # SQLAlchemy User + File models
├── templates/
│   ├── base.html           # Shared layout (nav, flash messages)
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashbord.html       # Dashboard (stats + recent files)
│   ├── files.html          # File list + upload form
│   ├── profile.html        # Profile settings
│   └── error.html          # 403 / 404 error page
├── static/
│   ├── css/style.css       # All styles
│   └── js/main.js          # Frontend interactions
├── uploads/                # Uploaded files stored here (auto-created)
└── database/
    └── database.db         # SQLite database (auto-created)
```

---

## Installation & Setup

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd secure-file-sharing-platform
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
```

Activate it:

- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python app.py
```

The server starts on **http://127.0.0.1:5000**

Open that URL in your browser. You will be redirected to the login page.  
Create an account first via the **"Create one"** link, then log in.

> The `uploads/` folder and `database/database.db` are created automatically on first run.

---

## Page Overview

| URL | Description |
|-----|-------------|
| `/` | Redirects to dashboard (logged in) or login |
| `/login` | Sign in page |
| `/register` | Create a new account |
| `/dashboard` | Overview of your files and stats |
| `/files` | Upload, manage, and share files |
| `/profile` | Update your display name |
| `/share/<token>` | Public download link (no login required) |

---

## Configuration

In `app.py`, you can change:

```python
app.config['SECRET_KEY'] = 'change-this-secret-key-in-production'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}
```

> ⚠️ Always change `SECRET_KEY` before deploying to production.

---

## Stopping the Server

Press `Ctrl + C` in the terminal where the app is running.

---

## Notes

- Files are stored in the `uploads/` folder on disk. Back this folder up if you care about the files.
- The SQLite database is stored at `database/database.db`. Back this up too.
- This app is intended for local / small-scale use. For production, use a proper WSGI server (e.g. Gunicorn) and a production-grade database.