from flask import render_template
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/otp", methods=["GET"])
def otp_page():
    return render_template("anxisense_otp.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("anxisense_dashboard.html")

@app.route("/patient-info", methods=["GET"])
def patient_info():
    return render_template("patient_information.html")

@app.route("/patients", methods=["GET"])
def my_patients():
    return render_template("mypatients.html")

@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")

@app.route("/quick-scan", methods=["GET"])
def quick_scan():
    return render_template("quick_scan.html")

@app.route("/facial-scan", methods=["GET"])
def facial_scan():
    return render_template("facial_scan.html")

@app.route("/facial-analysis-processing", methods=["GET"])
def facial_analysis_processing():
    return render_template("facial_analysis_processing.html")

@app.route("/analysis-report", methods=["GET"])
def analysis_report():
    return render_template("anxiety_analysis_report.html")

@app.route("/scan-success", methods=["GET"])
def scan_success():
    return render_template("scan_success_confirmation.html")

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/terms", methods=["GET"])
def terms():
    return render_template("terms.html")

@app.route("/help", methods=["GET"])
def help():
    return render_template("help.html")

@app.route("/nav.js")
def serve_nav():
    return render_template("nav.js"), {"Content-Type": "application/javascript"}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
