import re

def extract_email(text):

    text = text.replace(" @", "@")
    text = text.replace("@ ", "@")

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.search(pattern, text)

    return match.group() if match else "Not Found"


def extract_phone(text):

    pattern = r'\b\d{10}\b'

    match = re.search(pattern, text)

    return match.group() if match else "Not Found"

import re

def extract_skills(text):

    skills_database = [
        "Python",
        "Java",
        "JavaScript",
        "React",
        "Django",
        "Flask",
        "SQL",
        "MongoDB",
        "PostgreSQL",
        "AWS",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Git",
        "GitHub",
        "REST API",
        "Pandas",
        "NumPy"
    ]

    found_skills = []

    for skill in skills_database:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills

def calculate_match_score(resume_skills, job_skills):

    matched = []

    missing = []

    for skill in job_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = 0

    if len(job_skills) > 0:
        score = round(
            (len(matched) / len(job_skills)) * 100,
            2
        )

    return score, matched, missing
    