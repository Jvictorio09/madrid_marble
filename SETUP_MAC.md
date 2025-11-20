# Setting Up Django Environment on Mac

## Prerequisites
- Python 3.x installed (check with `python3 --version`)
- pip installed (comes with Python)

## Step-by-Step Setup

### 1. Navigate to Project Directory
```bash
cd /Users/julia/Desktop/madrid_marble
```

### 2. Create a Virtual Environment (if not already created)
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Database (Run Migrations)
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional - for admin access)
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/` by default.

## Quick Start Commands

Once your environment is set up, you can use these shortcuts:

**Activate virtual environment:**
```bash
source venv/bin/activate
```

**Start the server:**
```bash
python manage.py runserver
```

**Start on a specific port:**
```bash
python manage.py runserver 8080
```

**Deactivate virtual environment (when done):**
```bash
deactivate
```

## Troubleshooting

- **If you get "command not found" errors**: Make sure your virtual environment is activated
- **If you get import errors**: Run `pip install -r requirements.txt` again
- **If port 8000 is in use**: Use `python manage.py runserver 8080` to use a different port
- **Database errors**: Make sure you've run `python manage.py migrate`

