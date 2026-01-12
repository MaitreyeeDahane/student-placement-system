from flask import Flask, render_template, request
from flask import session, redirect, url_for
import hashlib


app = Flask(__name__)

app.secret_key = "admin_secret_key"

# ---------------- SAFE FLOAT HANDLER ----------------
def safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def student():
    return render_template("student_form.html")


@app.route("/submit", methods=["POST"])
def submit():

 # ================= GET FORM DATA SAFELY =================
    name = request.form.get("name")
    branch = request.form.get("branch")

    cgpa = safe_float(request.form.get("cgpa"))
    attendance = safe_float(request.form.get("attendance"))
    technical_skills = safe_float(request.form.get("technical_skills"))
    soft_skills = safe_float(request.form.get("soft_skills"))

    leetcode = safe_float(request.form.get("leetcode"))
    leetcode_level = request.form.get("leetcode_level")
    hackerrank_level = request.form.get("hackerrank_level")

    github_repos = safe_float(request.form.get("github_repos"))
    github_commits = safe_float(request.form.get("github_commits"))
    github_projects = safe_float(request.form.get("github_projects"))

 

    # --------- CONVERT TO PERCENTAGES ---------
    academics = int((cgpa / 10) * 100) if cgpa else 0
    technical = int((technical_skills / 10) * 100) if technical_skills else 0
    soft = int((soft_skills / 10) * 100) if soft_skills else 0
    coding = int(min((leetcode / 200) * 100, 100)) if leetcode else 0
    github = int(min((github_projects / 5) * 100, 100)) if github_projects else 0

    # --------- OVERALL SCORE ---------
    score = int((academics + technical + soft + coding + github) / 5)

    if score >= 80:
        status = "High Chance"
    elif score >= 60:
        status = "Medium Chance"
    else:
        status = "Low Chance"

    # ================= DETAILED CODING PROFILE ANALYSIS =================
    if coding >= 70:
        coding_message = (
            "You demonstrate a strong competitive coding profile with consistent problem-solving ability. "
            "You are comfortable with medium-level problems and are progressing well toward advanced concepts. "
            "Maintaining regular practice and participating in contests will further strengthen your performance."
        )
    elif coding >= 40:
        coding_message = (
             "Your coding performance is at an intermediate level. You have basic problem-solving exposure, "
            "but consistency in medium-level DSA problems is missing. Focus on strengthening data structures, "
            "improving logical thinking, and practicing timed problems regularly."
        )
    else:
        coding_message = (
             "Your competitive coding exposure is currently at a beginner level. You may find difficulty in "
            "solving standard DSA problems. It is recommended to start with fundamental topics such as arrays, "
            "strings, and basic algorithms, and gradually build problem-solving confidence."
        )

    # ================= DETAILED GITHUB ACTIVITY ANALYSIS =================
    if github >= 70:
        github_message = (
            "Your GitHub activity reflects strong practical exposure and hands-on development experience. "
            "Maintaining multiple repositories and project contributions indicates good understanding of "
            "real-world applications and version control practices."
        )
    elif github >= 40:
        github_message = (
            "You have moderate GitHub activity with some project exposure. While you have started building "
            "projects, increasing commit frequency and working on more complete applications will significantly "
            "improve your practical profile."
        )
    else:
        github_message = (
            "Your GitHub presence is currently limited, indicating low practical implementation experience. "
            "It is strongly recommended to build and upload real-world projects, regularly commit code, and "
            "use GitHub as a portfolio to showcase your technical skills."
        )

    # ================= FULLY DYNAMIC STRENGTHS & AREAS =================
    strengths = []
    improvements = []

    if academics >= 75:
        strengths.append("Strong academic performance with good conceptual understanding.")
    else:
        improvements.append("Academic consistency needs improvement.")

    if technical >= 70:
        strengths.append("Solid foundation in core technical subjects.")
    else:
        improvements.append("Core technical skills require strengthening.")

    if soft >= 70:
        strengths.append("Good communication and interpersonal skills.")
    else:
        improvements.append("Soft skills need improvement for interviews.")

    if coding >= 60:
        strengths.append("Good problem-solving ability through competitive coding.")
    else:
        improvements.append("More competitive coding practice is required.")

    if github >= 60:
        strengths.append("Hands-on development experience through GitHub projects.")
    else:
        improvements.append("More real-world project exposure on GitHub is needed.")

    strengths = strengths[:3]
    improvements = improvements[:3]

    # ================= FULLY DYNAMIC PERSONALIZED RECOMMENDATIONS =================
    recommendations = []

    if academics < 60:
        recommendations.append("Improve academic consistency to meet placement eligibility criteria.")

    if technical < 60:
        recommendations.append("Revise core technical subjects and apply concepts practically.")

    if coding < 50:
        recommendations.append("Practice DSA problems regularly to strengthen problem-solving skills.")

    if github < 50:
        recommendations.append("Build and upload at least one complete real-world project on GitHub.")

    if soft < 50:
        recommendations.append("Work on communication and interview-focused soft skills.")

    # If profile is strong
    if not recommendations:
        recommendations.append("Maintain consistency and focus on interview preparation.")

    # Keep UI clean
    recommendations = recommendations[:3]

    # ================= DATABASE INSERT (ALL TABLES) =================
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------- STUDENT ----------
        cursor.execute(
            "SELECT id FROM students WHERE name=%s AND branch=%s",
            (name, branch)
        )
        student = cursor.fetchone()

        if student:
            student_id = student["id"]
            cursor.execute("""
                UPDATE students
                SET cgpa=%s,
                    attendance=%s,
                    technical_skills=%s,
                    soft_skills=%s
                WHERE id=%s
            """, (cgpa, attendance, technical_skills, soft_skills, student_id))
        else:
            cursor.execute("""
                INSERT INTO students
                (name, branch, cgpa, attendance, technical_skills, soft_skills)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, branch, cgpa, attendance, technical_skills, soft_skills))
            student_id = cursor.lastrowid

        # ---------- CODING PROFILE ----------
        cursor.execute(
            "SELECT id FROM coding_profile WHERE student_id=%s",
            (student_id,)
        )
        if cursor.fetchone():
            cursor.execute("""
                UPDATE coding_profile
                SET leetcode_solved=%s,
                    leetcode_level=%s,
                    hackerrank_level=%s
                WHERE student_id=%s
            """, (leetcode, leetcode_level, hackerrank_level, student_id))
        else:
            cursor.execute("""
                INSERT INTO coding_profile
                (student_id, leetcode_solved, leetcode_level, hackerrank_level)
                VALUES (%s, %s, %s, %s)
            """, (student_id, leetcode, leetcode_level, hackerrank_level))

        # ---------- GITHUB ACTIVITY ----------
        cursor.execute(
            "SELECT id FROM github_activity WHERE student_id=%s",
            (student_id,)
        )
        if cursor.fetchone():
            cursor.execute("""
                UPDATE github_activity
                SET repositories=%s,
                    commits=%s,
                    projects=%s
                WHERE student_id=%s
            """, (github_repos, github_commits, github_projects, student_id))
        else:
            cursor.execute("""
                INSERT INTO github_activity
                (student_id, repositories, commits, projects)
                VALUES (%s, %s, %s, %s)
            """, (student_id, github_repos, github_commits, github_projects))

        # ---------- EVALUATION (ALWAYS INSERT) ----------
        cursor.execute("""
            INSERT INTO evaluations
            (student_id, academics_score, technical_score, soft_score,
            coding_score, github_score, overall_score, status, evaluated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (student_id, academics, technical, soft, coding, github, score, status))

        conn.commit()

    except Exception as e:
        print("Database error:", e)

    finally:
        cursor.close()
        conn.close()


    

    # ================= SEND DATA TO UI =================
    return render_template(
        "result.html",
        score=score,
        status=status,
        academics=academics,
        technical=technical,
        soft=soft,
        coding=coding,
        github=github,
        coding_message=coding_message,
        github_message=github_message,
        strengths=strengths,
        improvements=improvements,
        recommendations=recommendations
    )

from db import get_db_connection

@app.route("/db-test")
def db_test():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database connection successful"
    except Exception as e:
        return str(e)

import hashlib

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template(
                "admin_login.html",
                error="Please enter both username and password"
            )

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admins WHERE username = %s",
            (username,)
        )
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin and admin["password"] == hashed_password:
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------- STUDENT LIST (LATEST ONLY, NO DUPLICATES) ----------
    cursor.execute("""
    SELECT 
        s.id AS student_id,
        s.name,
        s.branch,
        e.overall_score,
        e.status,
        e.evaluated_at
    FROM students s
    JOIN evaluations e ON s.id = e.student_id
    WHERE e.evaluated_at = (
        SELECT MAX(e2.evaluated_at)
        FROM evaluations e2
        WHERE e2.student_id = s.id
    )
    ORDER BY e.evaluated_at DESC
""")

    students = cursor.fetchall()

    # ---------- STATS (MATCH TABLE EXACTLY) ----------
    cursor.execute("""
        SELECT
    COUNT(*) AS total,
    SUM(status='High Chance') AS high,
    SUM(status='Medium Chance') AS medium,
    SUM(status='Low Chance') AS low
FROM (
    SELECT e.*
    FROM evaluations e
    JOIN (
        SELECT student_id, MAX(evaluated_at) max_date
        FROM evaluations
        GROUP BY student_id
    ) latest
    ON e.student_id = latest.student_id
    AND e.evaluated_at = latest.max_date
) final;

    """)
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        stats=stats
    )




@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin/student/<int:student_id>")
def admin_student_history(student_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            academics_score,
            technical_score,
            soft_score,
            coding_score,
            github_score,
            overall_score,
            status,
            evaluated_at
        FROM evaluations
        WHERE student_id = %s
        ORDER BY evaluated_at DESC
    """, (student_id,))

    evaluations = cursor.fetchall()

    cursor.execute("""
        SELECT name, branch
        FROM students
        WHERE id = %s
    """, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "admin_student_history.html",
        student=student,
        evaluations=evaluations
    )




if __name__ == "__main__":
    app.run(debug=True)
