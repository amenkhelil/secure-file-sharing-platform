"""
init_db.py
----------
Run this script ONCE before starting the app for the first time.
It creates the 'database/' folder (if missing) and builds all
SQLite tables from the SQLAlchemy models.

Usage:
    python init_db.py
"""

import os
from app import app, db

# Make sure the database folder exists
db_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
os.makedirs(db_folder, exist_ok=True)
print(f"[1/3] database/ folder ready  →  {db_folder}")

# Make sure the uploads folder exists
uploads_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(uploads_folder, exist_ok=True)
print(f"[2/3] uploads/ folder ready   →  {uploads_folder}")

# Create all database tables defined in models/models.py
with app.app_context():
    db.create_all()
    print("[3/3] Database tables created successfully.")
    print()
    print("Tables now in database:")
    import sqlite3
    db_path = os.path.join(db_folder, 'database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    for (table_name,) in cur.fetchall():
        cur2 = conn.cursor()
        cur2.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cur2.fetchall()]
        print(f"  {table_name}: {', '.join(columns)}")
    conn.close()
    print()
    print("✓ Database is ready. You can now run:  python app.py")
