import os
from collections import OrderedDict
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional
from uuid import uuid4

from flask import Flask, render_template, request, send_file, abort
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from config import ROLE_CONFIG, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from services.utils import allowed_file, save_upload
from services.parser import parse_resume
from services.ats_engine import compute_ats_score
from services.feedback_generator import generate_feedback
from services.report_pdf import generate_report_pdf


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "smartats-dev-secret-change-in-prod")

REPORT_CACHE_MAX_ITEMS = 100
REPORT_CACHE_TTL_MINUTES = 30
report_cache = OrderedDict()
report_token_serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

ROLE_DROPDOWN_GROUPS = [
    (
        "Engineering",
        [
            "Software Engineer",
            "C++ Developer",
            "C Developer",
            "Ruby Developer",
            "Full Stack Developer",
            "Python Fullstack Developer",
            "Java Full-Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "Web Developer",
            "MERN Stack Developer",
            "Python Developer",
            "Java Developer",
            ".NET Developer",
            "PHP Developer",
            "Go Developer",
        ],
    ),
    (
        "Data",
        [
            "Data Analyst",
            "Data Scientist",
            "ML Engineer",
        ],
    ),
    (
        "QA",
        [
            "QA Engineer",
            "Software Tester",
            "Automation Test Engineer",
        ],
    ),
    (
        "Infra",
        [
            "Android Developer",
            "iOS Developer",
            "DevOps Engineer",
            "Cloud Engineer",
            "System Administrator",
            "Network Engineer",
            "Database Administrator",
            "Cybersecurity Analyst",
        ],
    ),
    (
        "Product/Design",
        [
            "Business Analyst",
            "Product Manager",
            "UI/UX Designer",
        ],
    ),
]


def _build_role_groups() -> list:
    available_labels = {role["label"] for role in ROLE_CONFIG.values()}
    grouped = []
    used_labels = set()

    for category, labels in ROLE_DROPDOWN_GROUPS:
        filtered_labels = [label for label in labels if label in available_labels]
        if filtered_labels:
            grouped.append({"category": category, "roles": filtered_labels})
            used_labels.update(filtered_labels)

    leftovers = sorted(available_labels - used_labels)
    if leftovers:
        grouped.append({"category": "Other", "roles": leftovers})

    return grouped


def _cleanup_expired_reports() -> None:
    now = datetime.utcnow()
    expired_ids = [
        report_id
        for report_id, cache_item in report_cache.items()
        if cache_item["expires_at"] <= now
    ]
    for report_id in expired_ids:
        report_cache.pop(report_id, None)


def _store_report_data(report_data: dict) -> str:
    _cleanup_expired_reports()
    report_id = str(uuid4())
    report_cache[report_id] = {
        "report_data": report_data,
        "expires_at": datetime.utcnow() + timedelta(minutes=REPORT_CACHE_TTL_MINUTES),
    }
    report_cache.move_to_end(report_id)

    while len(report_cache) > REPORT_CACHE_MAX_ITEMS:
        report_cache.popitem(last=False)

    return report_id


def _build_report_data(role_label: str, parsed: dict, ats_details: dict, feedback: dict) -> dict:
    return {
        "role": role_label,
        "name": parsed["name"],
        "ats_score": ats_details["ats_score"],
        "keyword_match": ats_details["keyword_match"],
        "section_info": ats_details["sections"],
        "length_score": ats_details["length_score"],
        "formatting_score": ats_details["formatting_score"],
        "action_verb_score": ats_details["action_verb_score"],
        "technical_depth_score": ats_details["technical_depth_score"],
        "consistency_score": ats_details["consistency_score"],
        "ats_friendliness_score": ats_details["ats_friendliness_score"],
        "ats_friendliness_breakdown": ats_details["ats_friendliness_breakdown"],
        "role_signal_score": ats_details["role_signal_score"],
        "role_signal_analysis": ats_details["role_signal_analysis"],
        "experience_level": ats_details["experience_level"],
        "strong_areas": feedback["strong_areas"],
        "weak_points": feedback["weak_points"],
        "improvement_suggestions": feedback["improvement_suggestions"],
        "template_feedback": feedback["template_feedback"],
        "score_explanation": feedback["score_explanation"],
    }


def _create_report_token(report_data: dict) -> str:
    return report_token_serializer.dumps(report_data, salt="report-download")


def _read_report_token(token: str, max_age_seconds: int) -> Optional[dict]:
    try:
        return report_token_serializer.loads(
            token,
            salt="report-download",
            max_age=max_age_seconds,
        )
    except (BadSignature, SignatureExpired):
        return None

@app.route("/", methods=["GET"])
def home():
    role_groups = _build_role_groups()
    return render_template("index.html", role_groups=role_groups)

@app.route("/analyze", methods=["POST"])
def analyze():
    role_label = request.form.get("role")
    if not role_label:
        return "Please select a role", 400

    # Find role_key from label
    role_key = None
    for key, config in ROLE_CONFIG.items():
        if config["label"] == role_label:
            role_key = key
            break

    if not role_key:
        return f"Invalid role: {role_label}", 400

    file = request.files.get("resume")
    if not file or file.filename == "":
        return "No file uploaded", 400
    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are allowed", 400

    original_filename = os.path.basename(file.filename)

    filepath = None
    try:
        filepath = save_upload(file)
        parsed = parse_resume(filepath)
        ats_details = compute_ats_score(parsed, role_key)
        feedback = generate_feedback(role_label, parsed, ats_details)
        report_data = _build_report_data(role_label, parsed, ats_details, feedback)
        report_id = _store_report_data(report_data)
        report_token = _create_report_token(report_data)

        return render_template(
            "result.html",
            report_id=report_id,
            report_token=report_token,
            role=role_label,
            resume_filename=original_filename,
            role_config=ROLE_CONFIG[role_key],
            name=parsed["name"],
            ats_score=ats_details["ats_score"],
            keyword_match=ats_details["keyword_match"],
            section_info=ats_details["sections"],
            length_score=ats_details["length_score"],
            formatting_score=ats_details["formatting_score"],
            action_verb_score=ats_details["action_verb_score"],
            technical_depth_score=ats_details["technical_depth_score"],
            consistency_score=ats_details["consistency_score"],
            ats_friendliness_score=ats_details["ats_friendliness_score"],
            ats_friendliness_breakdown=ats_details["ats_friendliness_breakdown"],
            role_signal_score=ats_details["role_signal_score"],
            role_signal_analysis=ats_details["role_signal_analysis"],
            experience_level=ats_details["experience_level"],
            strong_areas=feedback["strong_areas"],
            weak_points=feedback["weak_points"],
            improvement_suggestions=feedback["improvement_suggestions"],
            template_feedback=feedback["template_feedback"],
            score_explanation=feedback["score_explanation"],
        )
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        return f"Error analyzing resume: {str(e)}", 500
    finally:
        # Clean up uploaded file to save /tmp space on Vercel
        if filepath:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temp file {filepath}: {cleanup_error}")


@app.route("/download-report/<report_id>", methods=["GET", "POST"])
def download_report(report_id):
    _cleanup_expired_reports()
    cache_item = report_cache.get(report_id)
    report_data = cache_item["report_data"] if cache_item else None

    if not report_data:
        token = request.values.get("token", "")
        report_data = _read_report_token(token, REPORT_CACHE_TTL_MINUTES * 60) if token else None

    if not report_data:
        return abort(404, description="Report not found or expired. Please re-analyze your resume.")

    try:
        pdf_bytes = generate_report_pdf(report_data)
        candidate_name = (report_data.get("name") or "candidate").replace(" ", "_")
        role_name = (report_data.get("role") or "role").replace(" ", "_")
        filename = f"{candidate_name}_{role_name}.pdf"

        # Create BytesIO object from bytes
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)  # Reset pointer to beginning
        
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return abort(500, description=f"Error generating PDF report: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
