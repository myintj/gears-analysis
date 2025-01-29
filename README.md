# Gear Analysis Flask App

This Flask application lets you compare a user-uploaded gear vibration CSV to a preloaded **no-fault** baseline. It plots each sensor’s vibration data, highlighting potential anomalies or faults. Under each plot, the app provides a short explanation, and it also displays the first 10 rows of both datasets for a quick comparison.

## Project Structure

```vbnet
gear-analysis-flask-app/
├── data/
│   ├── no_fault.csv
│   ├── eccentricity.csv
│   ├── missing_tooth.csv
│   ├── root_crack.csv
│   ├── surface_fault.csv
│   └── tooth_chipped_fault.csv
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── index.html
│   └── analysis.html
├── uploads/            (optional, if you store uploaded files on disk)
├── app.py
├── requirements.txt
└── README.md



