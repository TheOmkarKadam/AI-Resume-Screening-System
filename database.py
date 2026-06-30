import sqlite3

DATABASE_NAME = "resume_analyzer.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        phone TEXT,

        ats_score INTEGER,

        matched_skills TEXT,

        missing_skills TEXT,

        analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_analysis(
    email,
    phone,
    score,
    matched,
    missing
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO resume_history(

        email,
        phone,
        ats_score,
        matched_skills,
        missing_skills

    )

    VALUES(?,?,?,?,?)

    """,
    (
        email,
        phone,
        score,
        ",".join(matched),
        ",".join(missing)
    ))

    conn.commit()
    conn.close()


def get_all_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        id,
        email,
        phone,
        ats_score,
        analysis_date

    FROM resume_history

    ORDER BY analysis_date DESC

    """)

    history = cursor.fetchall()

    conn.close()

    return history


def search_history(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        id,
        email,
        phone,
        ats_score,
        analysis_date

    FROM resume_history

    WHERE email LIKE ?

    ORDER BY analysis_date DESC

    """, ('%' + keyword + '%',))

    history = cursor.fetchall()

    conn.close()

    return history

def delete_resume(record_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM resume_history

    WHERE id=?

    """, (record_id,))

    conn.commit()

    conn.close()

def delete_resume(record_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM resume_history
    WHERE id = ?
    """, (record_id,))

    conn.commit()

    conn.close()

def get_report(record_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        email,
        phone,
        ats_score,
        matched_skills,
        missing_skills,
        analysis_date

    FROM resume_history

    WHERE id=?

    """,(record_id,))

    report = cursor.fetchone()

    conn.close()

    return report