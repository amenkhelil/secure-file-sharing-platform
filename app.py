"""
Secure File Sharing Platform
Main application file - contains all routes and app configuration.
"""

import os
import uuid
import secrets

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_from_directory, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from werkzeug.utils import secure_filename

# Import database and models
from models.models import db, User, File

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Secret key for session management - change this in production!
app.config['SECRET_KEY'] = 'change-this-secret-key-in-production'

# SQLite database file location
# Using absolute path so it always resolves to the 'database/' folder
# next to app.py, regardless of where you run Flask from.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "sqlite:///database.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload settings
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

# ---------------------------------------------------------------------------
# Initialize extensions
# ---------------------------------------------------------------------------

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'          # Redirect to login if not authenticated
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Tell Flask-Login how to load a user from the database."""
    return User.query.get(int(user_id))


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def format_file_size(size_bytes):
    """Convert bytes to a human-readable string (KB, MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


# Make format_file_size available in all templates
app.jinja_env.globals['format_file_size'] = format_file_size


# ---------------------------------------------------------------------------
# Authentication Routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else to login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    # If already logged in, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # --- Validation ---
        errors = []

        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')

        # Check if email already exists
        if email and User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            # Pass back form values so user doesn't have to retype
            return render_template('register.html', name=name, email=email)

        # --- Create the user ---
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        # Find the user
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            # Redirect to the page the user was trying to access
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log the user out and redirect to login."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Dashboard Route
# ---------------------------------------------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing user stats."""
    # Count total files uploaded by this user
    total_files = File.query.filter_by(user_id=current_user.id).count()

    # Count files that have been shared (have a share token)
    shared_files = File.query.filter_by(
        user_id=current_user.id
    ).filter(File.share_token.isnot(None)).count()

    # Get the 5 most recently uploaded files for display
    recent_files = (
        File.query
        .filter_by(user_id=current_user.id)
        .order_by(File.upload_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'dashboard.html',
        total_files=total_files,
        shared_files=shared_files,
        recent_files=recent_files
    )


# ---------------------------------------------------------------------------
# File Management Routes
# ---------------------------------------------------------------------------

@app.route('/files')
@login_required
def files():
    """Show all files uploaded by the current user."""
    user_files = (
        File.query
        .filter_by(user_id=current_user.id)
        .order_by(File.upload_date.desc())
        .all()
    )
    return render_template('files.html', files=user_files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload."""
    # Check if a file was included in the request
    if 'file' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('files'))

    file = request.files['file']

    # Check if user actually selected a file
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('files'))

    # Validate the file type
    if not allowed_file(file.filename):
        flash(
            'File type not allowed. Allowed types: PDF, DOCX, TXT, PNG, JPG, JPEG.',
            'danger'
        )
        return redirect(url_for('files'))

    # --- Save the file securely ---
    original_filename = file.filename

    # secure_filename removes dangerous characters from the filename
    safe_name = secure_filename(original_filename)

    # Generate a unique filename to avoid collisions on disk
    file_extension = safe_name.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    # Get the actual file size after saving
    file_size = os.path.getsize(file_path)

    # --- Save file record to database ---
    new_file = File(
        user_id=current_user.id,
        filename=unique_filename,
        original_filename=original_filename,
        file_size=file_size
    )
    db.session.add(new_file)
    db.session.commit()

    flash(f'"{original_filename}" uploaded successfully!', 'success')
    return redirect(url_for('files'))


@app.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """Download a file (only the owner can download)."""
    file = File.query.get_or_404(file_id)

    # Security check: make sure the file belongs to the current user
    if file.user_id != current_user.id:
        abort(403)

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,
        download_name=file.original_filename  # Use the original name for download
    )


@app.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    """Delete a file (only the owner can delete)."""
    file = File.query.get_or_404(file_id)

    # Security check: make sure the file belongs to the current user
    if file.user_id != current_user.id:
        abort(403)

    # Delete the actual file from disk
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the database record
    original_name = file.original_filename
    db.session.delete(file)
    db.session.commit()

    flash(f'"{original_name}" deleted successfully.', 'success')
    return redirect(url_for('files'))


# ---------------------------------------------------------------------------
# Secure Sharing Routes
# ---------------------------------------------------------------------------

@app.route('/share/generate/<int:file_id>', methods=['POST'])
@login_required
def generate_share_link(file_id):
    """Generate a unique sharing token for a file."""
    file = File.query.get_or_404(file_id)

    # Security check
    if file.user_id != current_user.id:
        abort(403)

    # Generate a secure random token (32 bytes = 64 hex characters)
    file.share_token = secrets.token_urlsafe(32)
    db.session.commit()

    flash('Share link generated successfully!', 'success')
    return redirect(url_for('files'))


@app.route('/share/revoke/<int:file_id>', methods=['POST'])
@login_required
def revoke_share_link(file_id):
    """Remove the sharing token, making the file private again."""
    file = File.query.get_or_404(file_id)

    # Security check
    if file.user_id != current_user.id:
        abort(403)

    file.share_token = None
    db.session.commit()

    flash('Share link revoked. The file is now private.', 'info')
    return redirect(url_for('files'))


@app.route('/share/<string:token>')
def shared_file(token):
    """Public route - anyone with the token can download the file."""
    # Find the file by its share token
    file = File.query.filter_by(share_token=token).first_or_404()

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,
        download_name=file.original_filename
    )


# ---------------------------------------------------------------------------
# Profile Routes
# ---------------------------------------------------------------------------

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page - view and update profile info."""
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()

        if not new_name:
            flash('Name cannot be empty.', 'danger')
        else:
            current_user.name = new_name
            db.session.commit()
            flash('Profile updated successfully!', 'success')

        return redirect(url_for('profile'))

    return render_template('profile.html')


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message='Page not found.'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', code=403, message='Access denied.'), 403


@app.errorhandler(413)
def file_too_large(e):
    flash('File is too large. Maximum size is 20 MB.', 'danger')
    return redirect(url_for('files'))


# ---------------------------------------------------------------------------
# App Entry Point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Make sure required folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('database', exist_ok=True)

    # Create all database tables
    with app.app_context():
        db.create_all()

    # Run the development server
    app.run(debug=True, host='0.0.0.0', port=5000)
  