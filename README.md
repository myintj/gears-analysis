# Gear Analysis Flask App

This Flask application lets you compare a user-uploaded gear vibration CSV to a preloaded **no-fault** baseline. It plots each sensor’s vibration data, highlighting potential anomalies or faults. Under each plot, the app provides a short explanation, and it also displays the first 10 rows of both datasets for a quick comparison.

Data from: (https://www.kaggle.com/datasets/hieudaotrung/gear-vibration/data)

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
├── uploads/      
├── app.py
├── requirements.txt
└── README.md
```
## Overview

This application provides a straightforward web interface for uploading and comparing gear vibration data against a known no-fault baseline. By plotting sensor signals (e.g., x-axis, y-axis, rolling mean), it helps users quickly detect anomalies and assess gear health. Under each chart, explanatory text clarifies potential fault indicators, and the first 10 rows of both datasets are shown for easy reference.

## Features

- **CSV Upload & Comparison**: Upload a gear-vibration CSV to compare against the preloaded `no_fault.csv`.
- **Multiple Visualizations**: Generate separate plots for sensor1 (x-axis vibration), sensor2 (y-axis vibration), and a rolling mean trend.
- **Automated Explanations**: Each plot comes with a brief description to help interpret the results.
- **Tabular Data**: View the first 10 rows of both datasets side by side.
- **Easy Navigation**: A simple home page lets you choose and upload your file, then click “Analyse” for immediate feedback.

## Requirements

- **Python 3.8+**
- **Flask** (web framework)
- **pandas** (data handling)
- **matplotlib** (plotting)

*(All dependencies are listed in `requirements.txt`.)*


