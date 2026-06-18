from resume_parser import extract_text_from_pdf

from flask import Flask, render_template, request
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

        from matcher import extract_email, extract_phone, extract_skills
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)

        return f"""
        <h1>Resume Analysis</h1>

        <h3>Email:</h3>
        <p>{email}</p>

        <h3>Phone:</h3>
        <p>{phone}</p>

        <h3>Skills:</h3>
        <p>{", ".join(skills)}</p>

        <h3>Resume Text:</h3>

        <pre>{resume_text}</pre>
        """

        return f"Resume uploaded successfully: {file.filename}"

    return "No file uploaded"


if __name__ == "__main__":
    app.run(debug=True)