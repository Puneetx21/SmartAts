from flask import Flask, render_template, request, redirect, url_for
from config import ROLE_CONFIG, UPLOAD_FOLDER, MAX_CONTENT_LENGTH 
from services.utils import allowed_file, save_upload
from services.parser import parse_resume
from services.ats_engine import compute_ats_score  
from services.ai_feedback import get_ai_feedback


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

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
    ai = get_ai_feedback(role_label, parsed, ats_details)

    return render_template(
        "result.html",
        role=role_label,
        role_config=ROLE_CONFIG[role_key],
        name=parsed["name"],
        ats_score=ats_details["ats_score"],
        keyword_match=ats_details["keyword_match"],
        section_info=ats_details["sections"],
        length_score=ats_details["length_score"],
        formatting_score=ats_details["formatting_score"],
        strong_areas=ai["strong_areas"],
        weak_points=ai["weak_points"],
        improvement_suggestions=ai["improvement_suggestions"],
        template_feedback=ai["template_feedback"],
    )



if __name__ == "__main__":  # ADD THESE 3 LINES
    app.run(debug=True)
