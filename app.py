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

        # Extract resume text
        resume_text = extract_text_from_pdf(filepath)

        # Read Job Description
        job_description = request.form["job_description"]

        # Candidate Details
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)

        # Extract Skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        # ATS Score
        score, matched_skills, missing_skills = calculate_match_score(
            resume_skills,
            job_skills
        )

        # Recommendations
        recommendations = []

        if score < 80:
            recommendations.append(
                "Improve your resume by adding the missing technical skills."
            )

        for skill in missing_skills:
            recommendations.append(
                f"Consider learning {skill}."
            )

        return render_template(
            "result.html",
            email=email,
            phone=phone,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendations=recommendations,
        )

    return "No file uploaded."


if __name__ == "__main__":
    app.run(debug=True)