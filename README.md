# SmartATS - Rule-Based Resume ATS Analyzer

SmartATS is a Flask web app that analyzes resumes against role-specific ATS criteria and generates actionable feedback without external AI/API calls.

The analyzer is fully local, rule-based, and supports downloadable PDF reports.

## What Changed Recently

Major updates were added to improve scoring quality, role coverage, and resume parsing reliability:

- Improved scoring logic with role-aware weighted components
- Smoother keyword coverage scoring for long skill lists
- Role condition support (for example, "at least one backend language")
- New ATS-friendliness sub-score with detailed breakdown
- Role-signal scoring for portfolio/profile/impact evidence
- Developer calibration bonus for strong technical resumes
- Expanded role catalog with grouped role selector in UI
- Added DOCX resume support in addition to PDF
- Improved parsing of section aliases and technical skill variants
- Improved report download handling and serverless-safe cleanup
- Upgraded PDF report to A4-based professional layout with visual hierarchy
- Added footer with generation timestamp and page number on every page
- Converted Keyword Analysis to text-based bullets with adaptive 2-column layout
- Ensured full Prioritized Suggestions, Strong Areas, and Resume Format Best Practices are included in report output

## Built With

- Python 3.8+
- Flask
- PyMuPDF (PDF extraction)
- python-docx (DOCX extraction)
- ReportLab (PDF report generation)

## Core Features

- ATS score calculation (0-100)
- Role-based keyword matching:
  - Required skills
  - Nice-to-have skills
  - Conditional skill groups
- Section completeness and section depth checks
- Action verb and writing impact analysis
- Technical depth and consistency scoring
- ATS-friendliness analysis (heading/contact/bullets/readability)
- Experience-level inference (entry, junior, mid, senior)
- Role-signal analysis (GitHub, LinkedIn, portfolio, certifications, project links)
- Prioritized, role-aware improvement suggestions
- Downloadable analysis report in PDF format
- A4 professional report style with color-coded sections and clear typography hierarchy

## Scoring Model

SmartATS calculates the final score using weighted components from `services/ats_engine.py`:

- `keyword`
- `sections`
- `action_verbs`
- `technical_depth`
- `consistency`
- `length`
- `formatting`
- `role_signals`
- `ats_friendliness`

Default scoring weights:

```txt
keyword:         0.43
sections:        0.19
action_verbs:    0.10
technical_depth: 0.08
consistency:     0.07
length:          0.04
formatting:      0.03
role_signals:    0.01
ats_friendliness:0.05
```

Some roles (for example `mern_developer`, `data_scientist`, `ui_ux_designer`) use custom weights.

## Supported Roles

The project currently includes 33 role configurations across engineering, data, QA, infrastructure, and product/design domains.

Examples include:

- Software Engineer
- Full Stack Developer
- Frontend Developer
- Backend Developer
- MERN Stack Developer
- Python Developer
- Java Developer
- C++ Developer
- C Developer
- Ruby Developer
- .NET Developer
- PHP Developer
- Go Developer
- Data Analyst
- Data Scientist
- ML Engineer
- QA Engineer
- Automation Test Engineer
- DevOps Engineer
- Cloud Engineer
- Android Developer
- iOS Developer
- UI/UX Designer
- Product Manager

Complete role definitions and skill requirements are maintained in `config.py` under `ROLE_CONFIG`.

## Installation

```bash
cd p:\PythonProject\smartats
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5000

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the app with `python app.py`.
4. Open the app in the browser.
5. Select target role.
6. Upload resume file (`.pdf` or `.docx`).
7. Review analysis and download the PDF report.

## Dependencies

```txt
Flask>=2.3.0
pymupdf==1.23.26
reportlab>=4.0.0
python-docx>=1.1.2
```

## No .env Required

This project does not require `.env` for scoring logic.

- No API keys
- No third-party AI service integration
- No network dependency for ATS evaluation

## How It Works

1. User selects a role.
2. User uploads a PDF or DOCX resume.
3. Parser extracts normalized text, sections, skills, and profile signals.
4. ATS engine computes weighted scoring metrics.
5. Feedback generator creates role-specific strengths, weak points, and actions.
6. Result page displays full analysis.
7. User downloads PDF report using report id/token flow.

## Project Structure

```txt
smartats/
|-- app.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- vercel.json
|
|-- api/
|   |-- index.py
|
|-- services/
|   |-- ats_engine.py
|   |-- feedback_generator.py
|   |-- parser.py
|   |-- report_pdf.py
|   |-- utils.py
|   |-- __init__.py
|
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- result.html
|
|-- static/
|   |-- css/
|   |   |-- style.css
|   |   |-- circular-progress.css
|   |-- js/
|       |-- main.js
|
|-- uploads/
    |-- logs/
```

## Main Modules

- `app.py`: routes, role grouping, analysis flow, report cache, tokenized report fallback
- `services/parser.py`: PDF/DOCX parsing, section detection, skill extraction, profile signal extraction
- `services/ats_engine.py`: complete scoring engine and weighted score assembly
- `services/feedback_generator.py`: role-aware feedback and prioritized suggestions
- `services/report_pdf.py`: PDF report generation
- `config.py`: upload config and complete role/skill configuration

## Report Download

- Result page provides a Download PDF Report action.
- Endpoint: `/download-report/<report_id>`
- Uses in-memory cache and signed token fallback.
- Cache policy:
  - Max 100 report objects
  - TTL 30 minutes with periodic cleanup

## PDF Report Layout

- Page size: A4
- Footer: left side shows report generation date/time, right side shows page number
- Header hierarchy:
  - Main headers: bold + underlined
  - Subheaders: bold
  - Content: regular body text
- Keyword Analysis rendering:
  - Text-only bullet format (no tables)
  - Uses 2-column bullets only when a list has 3 or more items
- Content inclusion:
  - Strong Areas: full list included
  - Prioritized Suggestions: full list included
  - Resume Format Best Practices: full list included

## Deployment (Vercel)

SmartATS is configured for Vercel serverless deployment:

- `vercel.json` routes traffic to Python app
- `api/index.py` provides serverless entry point
- Uploads use `/tmp/uploads` for serverless-safe writes
- Uploaded files are deleted after processing
- PDF reports are generated in memory

Quick deploy:

```bash
npm install -g vercel
vercel --prod
```

Deployment steps and troubleshooting are documented in this README.

## Live App

https://smart-ats-three.vercel.app

## Troubleshooting

- PowerShell activation blocked:
  - `Set-ExecutionPolicy -Scope Process Bypass`
- Package install issues:
  - `python -m pip install --upgrade pip`
- Parsing issues with scanned/image PDFs:
  - Re-export as a text-based PDF or use DOCX
