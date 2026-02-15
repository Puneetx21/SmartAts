#  AI Resume ATS – Smart Resume Analyzer

An AI-powered Resume Analysis System built using Flask that evaluates resumes based on ATS (Applicant Tracking System) scoring, keyword matching, and intelligent feedback generation.

This project helps job seekers optimize their resumes according to job descriptions using NLP-based analysis.

---

##  Features

- 📄 Resume Upload (PDF)
- 🧠 NLP-Based Resume Parsing
- 🎯 ATS Score Calculation
- 🔍 Keyword Matching with Job Description
- 🤖 AI-Based Resume Feedback
- 📊 Detailed Result Dashboard

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **NLP Processing:** Custom ATS Engine  
- **Environment Management:** python-dotenv  
- **Deployment Ready**

---

## 📂 Project Structure
ai-resume-ats/
│
├── app.py
├── config.py
├── services/
│ ├── ats_engine.py
│ ├── parser.py
│ ├── ai_feedback.py
│ ├── utils.py
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── result.html
│
├── static/
│ ├── css/
│ ├── js/
│
├── uploads/
├── requirements.txt
├── .env.example
└── README.md



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-ats.git
cd ai-resume-ats

### 2️⃣ Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate  # Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Create .env File
Create a file named .env in root directory:
API_KEY=your_api_key_here

⚠️ Do NOT upload .env to GitHub.

### 5️⃣ Run the Application
python app.py

Open:
http://127.0.0.1:5000/



Add these badges at the top (optional but professional):

```markdown
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![License](https://img.shields.io/badge/License-MIT-green)
