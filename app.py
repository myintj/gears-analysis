import os
import io
import base64

from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Replace with a secure key in production

# ------------------------------------------------------------------------------
# Load "no_fault.csv" from your data/ folder (lowercase columns: sensor1, sensor2, etc.)
# ------------------------------------------------------------------------------
no_fault_path = os.path.join("data", "no_fault.csv")
df_no_fault = pd.read_csv(no_fault_path)

# Global variables for the uploaded dataframe and the uploaded file's base name.
df_uploaded = None
uploaded_basename = None  # e.g. "root_crack" from "root_crack.csv"

@app.route("/")
def index():
    """
    Render the main page with the upload form and an 'Analyse' button.
    """
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """
    Handle file upload; store the uploaded CSV in a global DataFrame variable,
    and remember the base name (filename minus ".csv").
    """
    global df_uploaded, uploaded_basename
    
    if "file" not in request.files:
        flash("No file part in the request.")
        return redirect(url_for("index"))
    
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file.")
        return redirect(url_for("index"))
    
    try:
        df_uploaded = pd.read_csv(file)
        uploaded_basename = os.path.splitext(file.filename)[0]
        
        flash("File uploaded successfully!")
    except Exception as e:
        flash(f"Error reading file: {e}")
        return redirect(url_for("index"))
    
    return redirect(url_for("index"))

@app.route("/analyze", methods=["GET"])
def analyze():
    """
    Create 3 comparison plots between df_no_fault and df_uploaded.
    Display the first 10 rows of both DataFrames.
    """
    global df_uploaded, uploaded_basename
    
    if df_uploaded is None:
        flash("Please upload a CSV file first.")
        return redirect(url_for("index"))

    compare_length = min(500, len(df_no_fault), len(df_uploaded))
    df_no_fault_sample = df_no_fault.head(compare_length)
    df_uploaded_sample = df_uploaded.head(compare_length)

    # Use the uploaded filename in the explanatory text
    fault_label = f"{uploaded_basename} gear fault"

    # --------------------------------------------------------------------------
    # Generate the three plots
    # --------------------------------------------------------------------------
    plots = []
    
    # --- 1) Sensor 1 (x-axis vibration) ---
    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(df_no_fault_sample["sensor1"], label="No Fault", color="blue")
    ax1.plot(df_uploaded_sample["sensor1"], label=f"{fault_label}", color="red")
    ax1.set_title("Sensor 1 – vibration [mm] along x-axis")
    ax1.set_xlabel("Time (index)")
    ax1.set_ylabel("Vibration (mm)")
    ax1.legend()
    plot1_url = _fig_to_base64(fig1)

    explanation1 = (
        "This chart compares the sensor1 (x-axis) vibration signals from a no-fault gear "
        f"to the {fault_label}. Notice the amplitude and frequency changes to gauge "
        "whether there’s an anomaly. A stable baseline with few spikes suggests a healthy gear. "
        "Significant differences from the no-fault pattern may hint at mechanical faults."
    )

    plots.append((
        "Sensor 1 – vibration [mm] along x-axis",
        explanation1,
        plot1_url
    ))
    
    # --- 2) Sensor 2 (y-axis vibration) ---
    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.plot(df_no_fault_sample["sensor2"], label="No Fault", color="green")
    ax2.plot(df_uploaded_sample["sensor2"], label=f"{fault_label}", color="orange")
    ax2.set_title("Sensor 2 – vibration [mm] along y-axis")
    ax2.set_xlabel("Time (index)")
    ax2.set_ylabel("Vibration (mm)")
    ax2.legend()
    plot2_url = _fig_to_base64(fig2)

    explanation2 = (
        "This chart compares the sensor2 (y-axis) vibration signals of a no-fault gear "
        f"versus the {fault_label}. Looking at fluctuations can help identify abnormal resonance or wear. "
        "If the amplitude is consistently higher than the no-fault baseline, it may indicate gear damage. "
        "Trends in this axis often complement sensor1 findings for a fuller picture."
    )

    plots.append((
        "Sensor 2 – vibration [mm] along y-axis",
        explanation2,
        plot2_url
    ))

    # --- 3) Rolling mean (Sensor 1) ---
    fig3, ax3 = plt.subplots(figsize=(6,4))
    window_size = 10
    no_fault_rolling = df_no_fault_sample["sensor1"].rolling(window=window_size).mean()
    uploaded_rolling = df_uploaded_sample["sensor1"].rolling(window=window_size).mean()
    ax3.plot(no_fault_rolling, label="No Fault (rolling mean)", color="purple")
    ax3.plot(uploaded_rolling, label=f"{fault_label} (rolling mean)", color="brown")
    ax3.set_title("Sensor 1 – rolling mean (vibration [mm] along x-axis)")
    ax3.set_xlabel("Time (index)")
    ax3.set_ylabel("Rolling Mean (mm)")
    ax3.legend()
    plot3_url = _fig_to_base64(fig3)

    explanation3 = (
        "This graph displays a rolling mean of sensor1 data, smoothing out short-term noise "
        "to highlight broader trends. A stable rolling mean often indicates consistent operation, "
        f"while shifts in the {fault_label} line could suggest growing wear. "
        "Comparing both lines helps spot subtle deviations that raw signals might conceal."
    )

    plots.append((
        "Sensor 1 – rolling mean (vibration [mm] along x-axis)",
        explanation3,
        plot3_url
    ))
    
    # --------------------------------------------------------------------------
    # Prepare tables of the first 10 rows for display
    # --------------------------------------------------------------------------
    no_fault_head = df_no_fault.head(10)
    uploaded_head = df_uploaded.head(10)
    
    return render_template(
        "analysis.html",
        plots=plots,
        no_fault_head=no_fault_head.to_html(classes="table table-striped", index=False),
        uploaded_head=uploaded_head.to_html(classes="table table-striped", index=False)
    )

def _fig_to_base64(fig):
    """
    Helper function: convert a Matplotlib figure to a base64-encoded PNG string.
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    plt.close(fig)
    return "data:image/png;base64," + encoded

if __name__ == "__main__":
    app.run(debug=True)


