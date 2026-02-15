
# 🚀 AI Resume ATS – Smart Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Status](https://img.shields.io/badge/Project-Active-success)

An AI-powered Resume Analysis System built using Flask that evaluates resumes based on ATS (Applicant Tracking System) scoring, keyword matching, and intelligent feedback generation.

This system helps job seekers optimize their resumes according to job descriptions using NLP-based analysis.

---

## 🌟 Features

- 📄 Resume Upload (PDF Support)
- 📄 Drag and Drop feature for uploading
- 🧠 NLP-Based Resume Parsing
- 🎯 ATS Score Calculation
- 🔍 Keyword Matching with Job Description
- 🤖 AI-Generated Resume Feedback
- 📊 Detailed Analysis Dashboard

---

## 🛠 Tech Stack

**Backend**
- Python
- Flask

**Frontend**
- HTML
- CSS
- JavaScript

**Other Tools**
- python-dotenv
- PDF parsing libraries

---

## 📂 Project Structure

```

ai-resume-ats/
│
├── app.py
├── config.py
├── services/
│   ├── ats_engine.py
│   ├── parser.py
│   ├── ai_feedback.py
│   └── utils.py
│
├── templates/
├── static/
├── uploads/
├── requirements.txt
├── .env.example
└── README.md

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-ats.git
cd ai-resume-ats
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```
API_KEY=your_api_key_here
```

⚠️ Never upload `.env` to GitHub.

### 5️⃣ Run the Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 📸 Application Screenshots

### 🏠 Home Page

<img width="1791" height="767" alt="image" src="https://github.com/user-attachments/assets/f0d76e96-f7e8-46dc-b97f-2f38f82cd164" />

### 📊 ATS Result Dashboard

<img width="1142" height="865" alt="image" src="https://github.com/user-attachments/assets/64566bea-02ea-442b-8f24-b766a5c27586" />


---

## 🔐 Security Notice

* API keys are stored using environment variables.
* `.env` is excluded using `.gitignore`.
* No sensitive credentials are stored in the repository.

---

## 🚀 Future Enhancements

* User authentication system
* Resume formatting suggestions
* AI-powered resume improvement rewriting
* Cloud deployment with CI/CD
* Database integration

---

## 👨‍💻 Author

**Punit Chauhan**
B.Tech Computer Science
Aspiring Software Engineer

---

## 📄 License

This project is developed for academic and demonstration purposes.



