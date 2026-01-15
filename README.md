
#  Student Placement Evaluation & Analytics System

A full-stack web application designed to evaluate student placement readiness based on academics, skills, competitive coding, and project activity, with a secure admin dashboard for analytics and progress tracking.

---

##  Overview

This system helps analyze and track a student’s placement preparedness through structured evaluations and meaningful insights. It supports multiple evaluations per student, enabling progress monitoring over time, and provides administrators with a centralized dashboard for analytics and decision-making.

---

## ✨ Key Features

###  Student Module
- Structured evaluation form covering:
  - Academics (CGPA & attendance)
  - Technical skills
  - Soft skills
  - Competitive coding (LeetCode, HackerRank)
  - GitHub projects & activity
- Automatic placement readiness score calculation
- Detailed feedback on strengths and improvement areas
- Personalized recommendations based on performance

###  Admin Module
- Secure admin login & logout
- Interactive dashboard with:
  - Total students evaluated
  - High / Medium / Low placement chance statistics
- Displays **latest evaluation per student**
- View **complete evaluation history** for each student
- Clean, modern, Gen-Z inspired UI
- Consistent design across dashboard, history, and login pages

---

##  Evaluation Logic

Each evaluation is calculated using weighted metrics:
- **Academics:** CGPA & attendance
- **Skills:** Technical and soft skills
- **Coding:** Competitive programming performance
- **Projects:** GitHub repositories and practical work

An overall placement readiness score is generated and classified as:
- **High Chance**
- **Medium Chance**
- **Low Chance**

The system supports **multiple evaluations per student**, allowing admins to track progress and improvement over time.

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Font Awesome
- **Backend:** Python (Flask)
- **Database:** MySQL (local)
- **Authentication:** Session-based admin authentication
- **Version Control:** Git & GitHub

---

## 📸 Screenshots
#### 1. Index Page
<img width="1900" height="900" alt="Index Page" src="https://github.com/user-attachments/assets/b456bd30-31ba-4341-98b4-166116fffb8d" />

#### 2. Student Form
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/ea227557-c0d4-48e2-8d9d-98ac141daa04" />

#### 3. Result Page
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/16960695-58e7-4c67-992a-b63b64a20e5f" />

#### 4. Admin Login
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/e941fcdb-2c1e-4538-a116-dd94f8e3c89b" />

#### 5. Admin Dashboard
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/422ac557-0287-44f7-a5fc-b8cdc80612b6" />

#### 6. Student History
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/71620d0f-48e4-4f91-82d3-e5b3d48128a2" />

## ⚙️ How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/MaitreyeeDahane/student-placement-system.git
cd student_placement_system/backend
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Configure MySQL Database

- Create a MySQL database

- Create the required tables:

  - students

  - evaluations

  - coding_profile

  - github_activity

  - admins

- Update database credentials in db.py

### 4️⃣ Run the Application
```bash
python app.py
```
5️⃣ Open in Browser
```bash
http://127.0.0.1:5000/
```
### 📌 Project Status : 

###  🚧 Actively in Development

#### Planned Enhancements

- 📊 Visual performance analytics (radar & trend graphs)

- 🔍 Search, filters, and sorting in admin dashboard

- 📄 Export evaluation reports (PDF / CSV)

- ☁️ Cloud deployment (future-ready architecture)

### 💡 Why This Project?

#### This project demonstrates:

- Full-stack web development using Flask

- Relational database design with constraints & normalization

- Secure admin authentication and dashboards

- Analytics-driven student performance evaluation

- Clean UI/UX design with consistency across pages

- Real-world problem solving for placement readiness analysis

---

### 👤 Author

**Maitreyee Dahane**
#### Computer Engineering Student




