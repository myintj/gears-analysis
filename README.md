# Gear Analysis Flask App

This is a Flask-based application that compares user-uploaded gear vibration data against a baseline **no-fault** gear dataset. It helps detect potential gear faults by visualizing vibration signals and highlighting deviations from normal operation.

---

## Project Structure


- **`app.py`** – Main Flask application code.  
- **`data/`** – Stores the preloaded `no_fault.csv` (and optional fault examples).  
- **`static/`** – CSS and JavaScript files.  
- **`templates/`** – HTML templates for Flask routes.  
- **`uploads/`** – Optional folder if you choose to keep uploaded files instead of just reading them into memory.  
- **`requirements.txt`** – Lists Python dependencies.

---

## Installation & Setup

1. **Clone** this repo or [download the ZIP](https://github.com/your-username/gear-analysis-flask-app/archive/refs/heads/main.zip).

   ```bash
   git clone https://github.com/your-username/gear-analysis-flask-app.git
   cd gear-analysis-flask-app


