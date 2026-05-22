# Billing App

A desktop billing and invoicing application built with Flask, SQLAlchemy, and fpdf2.
Developed as a group project for the Software Engineering and Design Patterns course.

## Features

- **Customer management** — create, view, edit, and delete customers with full address details
- **Employee management** — manage employees with roles (Owner, Manager, Worker)
- **Work reports** — log work sessions with personnel (hours × rate) and material (qty × unit price) line items
- **Invoices** — group work reports into invoices, track status (Draft → Sent → Paid), and download as PDF
- **PDF export** — generates a formatted PDF invoice with itemised breakdown and tax calculation (8.1%)

## Architecture

The project follows a layered Domain-Driven Design:

```
app/
├── domain/         # Entities and business rules (pure Python, no framework deps)
├── repositories/   # Data access layer (SQLAlchemy sessions)
├── service/        # Application services (orchestrate domain + repositories)
├── model/          # ORM mappings (SQLAlchemy declarative models)
├── routes/         # Flask blueprints (HTTP layer)
├── templates/      # Jinja2 HTML templates
└── static/         # CSS
tests/
└── domain/         # Unit tests for all domain entities
```

Design patterns used: Repository, Service Layer, Value Object, State Machine, Soft Delete.

## Requirements

- Python 3.11+
- Conda (recommended) or virtualenv

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/usu259/Project_SoftwareEngineering.git
   cd Project_SoftwareEngineering
   ```

2. **Create and activate a virtual environment**

   With conda:
   ```bash
   conda create -n billing python=3.11
   conda activate billing
   ```

   Or with venv:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python main.py
   ```

   The app will start on `http://127.0.0.1:5000` and open in your default browser automatically.
   The SQLite database (`billing.db`) is created automatically on first run.

## Running tests

```bash
pytest tests/
```

All tests are unit tests for the domain layer and require no database or running server.

## Building the standalone executable (Windows)

```bash
pip install pyinstaller
pyinstaller app.spec
```

The executable will be created at `dist/Billing App.exe`.

## Project structure highlights

| File | Purpose |
|------|---------|
| `main.py` | Entry point — creates the Flask app and starts the server |
| `config.py` | App-wide constants (tax rate, field max lengths) |
| `app/database.py` | SQLAlchemy engine and table initialisation |
| `app/app.py` | Flask app factory, blueprint registration |

## License

MIT
