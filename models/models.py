"""
Database Models
Defines the User and File tables using Flask-SQLAlchemy.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Create the SQLAlchemy instance
# This will be initialized with the app in app.py
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model - stores account information.
    UserMixin provides default implementations for Flask-Login
    (is_authenticated, is_active, get_id, etc.)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: one user has many files
    # cascade='all, delete-orphan' means if user is deleted, their files are too
    files = db.relationship('File', backref='owner', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        """Hash and store the password. Never store plain text passwords."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a plain text password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class File(db.Model):
    """
    File model - stores metadata about uploaded files.
    The actual file is stored on disk in the uploads/ folder.
    """
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # The unique filename on disk (e.g., "a3f2b1c4.pdf")
    filename = db.Column(db.String(256), nullable=False)

    # The original filename as uploaded by the user (e.g., "my_report.pdf")
    original_filename = db.Column(db.String(256), nullable=False)

    # File size in bytes
    file_size = db.Column(db.Integer, nullable=False)

    # When the file was uploaded
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Sharing token - if set, anyone with /share/<token> can download
    # If None, the file is private
    share_token = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return f'<File {self.original_filename}>'