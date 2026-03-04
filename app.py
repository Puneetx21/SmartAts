from collections import OrderedDict
from datetime import datetime, timedelta
from io import BytesIO
from uuid import uuid4

from flask import Flask, render_template, request, send_file, abort
from config import ROLE_CONFIG, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from services.utils import allowed_file, save_upload
from services.parser import parse_resume
from services.ats_engine import compute_ats_score
from services.feedback_generator import generate_feedback
from services.report_pdf import generate_report_pdf


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

REPORT_CACHE_MAX_ITEMS = 100
REPORT_CACHE_TTL_MINUTES = 30
report_cache = OrderedDict()


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
        "experience_level": ats_details["experience_level"],
        "strong_areas": feedback["strong_areas"],
        "weak_points": feedback["weak_points"],
        "improvement_suggestions": feedback["improvement_suggestions"],
        "template_feedback": feedback["template_feedback"],
        "score_explanation": feedback["score_explanation"],
    }

@app.route("/", methods=["GET"])
def home():
    roles = [role["label"] for role in ROLE_CONFIG.values()]
    return render_template("index.html", roles=roles)

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
        return "Only PDF files are allowed", 400

    filepath = save_upload(file)

    parsed = parse_resume(filepath)
    ats_details = compute_ats_score(parsed, role_key)
    feedback = generate_feedback(role_label, parsed, ats_details)
    report_data = _build_report_data(role_label, parsed, ats_details, feedback)
    report_id = _store_report_data(report_data)

    return render_template(
        "result.html",
        report_id=report_id,
        role=role_label,
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
        experience_level=ats_details["experience_level"],
        strong_areas=feedback["strong_areas"],
        weak_points=feedback["weak_points"],
        improvement_suggestions=feedback["improvement_suggestions"],
        template_feedback=feedback["template_feedback"],
        score_explanation=feedback["score_explanation"],
    )


@app.route("/download-report/<report_id>", methods=["GET"])
def download_report(report_id):
    _cleanup_expired_reports()
    cache_item = report_cache.get(report_id)
    if not cache_item:
        return abort(404, description="Report not found. Please re-analyze your resume.")

    report_data = cache_item["report_data"]

    pdf_bytes = generate_report_pdf(report_data)
    candidate_name = (report_data.get("name") or "candidate").replace(" ", "_")
    filename = f"smartats_report_{candidate_name}.pdf"

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(debug=True)
