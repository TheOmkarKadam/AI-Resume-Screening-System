from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from matcher import (
    extract_email,
    extract_phone,
    extract_skills,
    calculate_match_score,
)
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():

    file = request.files["resume"]

    if file:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)
        job_description = request.form["job_description"]

        from matcher import extract_email, extract_phone, extract_skills
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        score, matched_skills, missing_skills = calculate_match_score(skills,job_skills)

        return f"""
<h1>Resume Analysis</h1>

<h2>Email</h2>
<p>{email}</p>

<h2>Phone</h2>
<p>{phone}</p>

<hr>

<h2>ATS Match Score</h2>

<h1>{score}%</h1>

<hr>

<h2>Matched Skills</h2>

<p>{matched_skills}</p>

<hr>

<h2>Missing Skills</h2>

<p>{missing_skills}</p>

<hr>

<h2>Resume Skills</h2>

<p>{skills}</p>

<hr>

<h2>Job Description Skills</h2>

<p>{job_skills}</p>
"""
    
if __name__ == "__main__":
    app.run(debug=True)