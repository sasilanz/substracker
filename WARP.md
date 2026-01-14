# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Substracker is a Flask-based web application for managing subscriptions and recurring payments. It's a simple monolithic application with SQLite persistence, designed for personal use with Docker deployment support.

**Language**: German (UI, comments, and documentation)

## Development Commands

### Running Locally
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application (with hot reload)
python app.py
```

Access at `http://localhost:5000`

### Docker Development
```bash
# Build and start container
docker-compose up --build

# Stop container
docker-compose down
```

### Database Management
```bash
# Reset database (deletes all data)
rm subscriptions.db
python app.py  # Will recreate database automatically
```

The database file is `subscriptions.db` (SQLite) and is created automatically on first run via `@app.before_request` hook in `app.py`.

## Architecture

### Application Structure

This is a **Flask monolith** with a classic MVC pattern:
- **Model**: `models.py` defines SQLAlchemy models (single `Subscription` model)
- **View**: Jinja2 templates in `templates/` directory
- **Controller**: Route handlers in `app.py`

### Key Components

**app.py**
- Main Flask application with all route handlers
- Database initialization happens via `@app.before_request` hook
- Routes: `/` (dashboard), `/add`, `/edit/<id>`, `/delete/<id>`
- Calculates total monthly/yearly costs on dashboard

**models.py**
- Single `Subscription` model with SQLAlchemy
- Fields: name, amount, cycle (monthly/yearly/quarterly), due_date, login, password, notes
- Passwords stored in **plaintext** (security concern documented in README)

**Database**
- SQLite file: `subscriptions.db`
- Initialized automatically on first request
- Volume-mounted in Docker at `/app` directory

### Data Flow

1. User requests route → Flask handler in `app.py`
2. Handler queries `Subscription` model via SQLAlchemy
3. Data passed to Jinja2 template in `templates/`
4. Template rendered with base layout (`base.html`)
5. Static assets served from `static/` (CSS/JS)

### Important Patterns

- All subscriptions sorted by `due_date` on dashboard
- Flash messages used for user feedback (success/error)
- Form submissions use POST, redirects to dashboard after success
- No authentication/authorization (single-user app)

## Important Configuration

### Secret Key
Change `app.config['SECRET_KEY']` in `app.py` for production (currently set to `'dev-secret-key-change-in-production'`)

### Environment Variables
- `FLASK_ENV`: Set to `production` or `development`
- `FLASK_APP`: Should be `app.py`

## Security Considerations

⚠️ This application is designed for **personal use only**:
- Passwords stored in plaintext in database
- No user authentication/authorization
- No CSRF protection beyond Flask's built-in session handling
- SQLite database file not encrypted

When modifying code that handles sensitive data, be aware of these limitations.

## Testing

No test suite currently exists. When adding tests, you'll need to:
- Add testing framework (e.g., pytest) to `requirements.txt`
- Create test database configuration
- Mock database for unit tests or use in-memory SQLite

## Notes for AI Assistants

- All user-facing text (templates, flash messages, comments) should be in **German**
- When adding new subscriptions fields, update both `models.py` and all relevant templates (`add.html`, `edit.html`, `index.html`)
- Database schema changes require manual migration or database reset
- The application uses Flask's development server (not production-ready)
