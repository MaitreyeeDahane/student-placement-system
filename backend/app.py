from flask import Flask, render_template, request

app = Flask(__name__)

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
    # --------- GET FORM DATA SAFELY ---------
    cgpa = safe_float(request.form.get("cgpa"))
    attendance = safe_float(request.form.get("attendance"))
    technical_skills = safe_float(request.form.get("technical_skills"))
    soft_skills = safe_float(request.form.get("soft_skills"))
    leetcode = safe_float(request.form.get("leetcode"))
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



if __name__ == "__main__":
    app.run(debug=True)
