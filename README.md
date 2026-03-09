# SmartATS — Logic-Based Resume ATS Analyzer

SmartATS is a Flask web app that analyzes PDF resumes against role-specific ATS criteria and generates actionable feedback **without any external AI/API calls**.

It is fully local, rule-based, and supports **PDF export of the analysis report**.😊
## 🛠 Built With

- 🐍 **Python 3.8+**
- 🌐 **Flask**
- 📄 **PyMuPDF (Resume Text Extraction)**
- 🧾 **ReportLab (PDF Report Generation)**

## Project Overview 
<img width="1347" height="863" alt="image" src="https://github.com/user-attachments/assets/e88b6256-0044-4871-973a-7c49b5c45c68" />

## Features

- ATS score calculation (0–100)
- Role-based keyword matching (required + nice-to-have)
- Section completeness checks
- Action-verb quality scoring
- Technical depth and consistency scoring
- Experience-level detection
- Prioritized improvement suggestions
- Responsive UI with dark/light theme
- Downloadable analysis report in PDF format

## Installation

```bash
cd p:\PythonProject\smartats
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:5000`

## Quick Start (New User)

1. Open the project folder.
2. Create and activate virtual environment:
  - Windows PowerShell: `.venv\Scripts\activate`
3. Install packages: `pip install -r requirements.txt`
4. Run app: `python app.py`
5. Open `http://localhost:5000`
6. Select role → upload PDF resume → view analysis → download PDF report

## Requirements

Current minimal dependencies:

```txt
Flask>=2.3.0
pymupdf>=1.23.0
reportlab>=4.0.0
```

## No `.env` Needed

This project is fully logic-based and **does not require `.env`**.

- No API keys
- No OpenAI/third-party AI integrations
- No cloud/network dependency for scoring logic

If a `.env` file exists locally, the app ignores it (safe to keep or delete).

## How It Works

1. User selects a target role.
2. User uploads a PDF resume.
3. Resume parser extracts text and structured information.
4. ATS engine computes score + sub-metrics.
5. Feedback generator creates role-aware suggestions.
6. Results page shows detailed analysis.
7. User can download a PDF report from the result page.

## Project Structure

```txt
smartats/
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── ats_engine.py
│   ├── feedback_generator.py
│   ├── parser.py
│   ├── report_pdf.py
│   ├── utils.py
│   └── __init__.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── circular-progress.css
│   └── js/
│       └── main.js
│
└── uploads/
    └── logs/
```

## Main Modules

- `app.py`: Flask routes, analysis flow, and report-download endpoint
- `services/parser.py`: PDF resume parsing
- `services/ats_engine.py`: scoring engine and ATS metrics
- `services/feedback_generator.py`: rule-based feedback logic
- `services/report_pdf.py`: PDF report builder
- `config.py`: role configurations and upload settings

## Report Download

- Result page includes **Download PDF Report** button
- Endpoint: `/download-report/<report_id>`
- Report cache is in-memory with:
  - max 100 reports
  - 30-minute expiry cleanup

## Notes

- Uploaded resumes are stored in `uploads/`.
- Keep uploads/logs out of version control as needed.
- For production, set `debug=False` and run behind a proper WSGI server.

## 🚀 Deployment to Vercel

SmartATS is fully compatible with Vercel's serverless platform:

### Quick Deploy
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### What's Vercel-Ready?
✅ **In-memory PDF generation** - No file writes needed  
✅ **Automatic file cleanup** - Uploads deleted after processing  
✅ **Serverless configuration** - `vercel.json` included  
✅ **/tmp storage** - Compatible with Vercel's ephemeral filesystem  

### Important Notes for Vercel:
- PDF downloads work via in-memory BytesIO (no disk writes)
- Report cache is per-instance (acceptable for this use case)
- Uploaded files auto-deleted after parsing to save /tmp space
- Free tier supports ~1,200 analyses/month

**For detailed deployment instructions, troubleshooting, and optimization tips, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## 🌐 Live Deployment

The application is deployed and publicly accessible using **Vercel**.

🚀 **Try it here:**  
👉 https://smart-ats-three.vercel.app

## Troubleshooting

- If activation is blocked in PowerShell, run: `Set-ExecutionPolicy -Scope Process Bypass`
- If install fails, upgrade pip first: `python -m pip install --upgrade pip`
- If PDF parsing fails for a resume, re-export the resume as a standard text-based PDF and retry
