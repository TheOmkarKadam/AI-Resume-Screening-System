from flask import Flask, render_template, request, redirect
from database import (
    create_database,
    get_report,
    save_analysis,
    get_all_history,
    search_history,
    delete_resume,
    get_report
)
from resume_parser import extract_text_from_pdf
from matcher import (
    extract_email,
    extract_phone,
    extract_skills,
    calculate_match_score,
)
import os


app = Flask(__name__)
create_database()

@app.route("/dashboard")
def dashboard():

    keyword = request.args.get("search")

    if keyword:

        history = search_history(keyword)

    else:

        history = get_all_history()

    return render_template(

        "dashboard.html",

        history=history,

        keyword=keyword

    )

@app.route("/delete/<int:record_id>")
def delete(record_id):

    delete_resume(record_id)

    return redirect("/dashboard")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report/<int:record_id>")
def report(record_id):

    report = get_report(record_id)

    return render_template(

        "report.html",

        report=report

    )


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
        save_analysis(email, phone, score, matched_skills, missing_skills)

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
@app.route("/history")
def history():

    history = get_all_history()

    return render_template(
        "history.html",
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True)