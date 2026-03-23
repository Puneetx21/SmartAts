"""Pure Python feedback generator for resume analysis - Enhanced"""
import re

from config import ROLE_CONFIG


SKILL_ACTION_HINTS = {
    "api": "Add a bullet describing at least one API you designed or integrated, with scale/latency impact.",
    "api integration": "Show frontend-backend integration details and measurable UX/performance outcome.",
    "authentication": "Mention auth flow implementation (JWT/OAuth/session) and role-based authorization.",
    "microservices": "Include one microservice split decision and how it improved deployment or scalability.",
    "docker": "Add containerization details and deployment workflow in CI/CD.",
    "kubernetes": "Describe orchestration use case (autoscaling, rollout strategy, health checks).",
    "ci/cd": "Add your build-test-deploy pipeline steps and release frequency improvement.",
    "testing": "Mention unit/integration test stack and coverage or defect reduction.",
    "sql": "Include query optimization work with before/after performance metric.",
    "data visualization": "Add dashboard examples with business decision impact.",
    "model evaluation": "Report model metrics (F1/AUC/RMSE) and validation approach.",
    "design systems": "Show reusable components and consistency improvements across screens.",
}

ROLE_SIGNAL_HINTS = {
    "kaggle": "Add a Kaggle profile link and 1-2 competition or notebook results.",
    "huggingface": "Add a Hugging Face profile/model card to show ML deployment capability.",
    "portfolio": "Add a public portfolio with project case studies and outcomes.",
    "behance": "Include Behance case studies highlighting design process and final impact.",
    "dribbble": "Include Dribbble shots that map to shipped features.",
    "figma_link": "Add a Figma prototype or design file link for proof of execution.",
    "certifications_count": "Add relevant, recent certifications (cloud/security/testing) to strengthen credibility.",
    "project_links_count": "Add at least one live/demo/repo link per flagship project.",
    "has_quantified_impact": "Add measurable outcomes (e.g., reduced latency 35%, improved conversion 18%).",
    "github": "Add GitHub profile/repo links with readable project structure and README.",
    "linkedin": "Add an updated LinkedIn URL aligned with resume role and achievements.",
}

PORTFOLIO_RECOMMENDED_ROLES = {
    "Frontend Developer",
    "Web Developer",
    "Full Stack Developer",
    "Python Fullstack Developer",
    "Java Full-Stack Developer",
    "UI/UX Designer",
    "Data Scientist",
    "Data Analyst",
    "Android Developer",
    "iOS Developer",
}


def generate_feedback(role_label: str, parsed: dict, ats_details: dict) -> dict:
    """Generate comprehensive feedback based on ATS analysis using pure Python logic"""

    role_config = next((v for v in ROLE_CONFIG.values() if v["label"] == role_label), None)

    if not role_config:
        return {
            "strong_areas": ["Role configuration not found"],
            "weak_points": [],
            "improvement_suggestions": [],
            "template_feedback": [],
            "score_explanation": "Please select a valid role"
        }
    
    missing_skills = ats_details["keyword_match"]["required_missing"]
    present_skills = ats_details["keyword_match"]["required_present"]
    nice_skills = ats_details["keyword_match"]["nice_present"]
    met_conditions = ats_details["keyword_match"].get("condition_present", [])
    missing_conditions = ats_details["keyword_match"].get("condition_missing", [])
    inferred_backend_language = ats_details["keyword_match"].get("inferred_backend_language", "not_detected")
    missing_sections = ats_details["sections"]["missing"]
    score = ats_details["ats_score"]
    experience_level = ats_details.get("experience_level", {})
    action_verb_score = ats_details.get("action_verb_score", 50)
    consistency_score = ats_details.get("consistency_score", 50)
    keyword_coverage = ats_details["keyword_match"]["required_coverage"]
    role_alignment = ats_details["keyword_match"].get("role_alignment", keyword_coverage)
    section_completeness = ats_details["sections"].get("completeness", 0)
    role_signal_data = ats_details.get("role_signal_analysis", {})
    role_signal_score = ats_details.get("role_signal_score", 0)
    missing_role_signals = role_signal_data.get("missing", [])
    missing_required_role_signals = role_signal_data.get("required_missing", [])
    profile_signals = parsed.get("profile_signals", {})
    full_text = parsed.get("full_text", "")
    ats_friendly_score = ats_details.get("ats_friendliness_score", 50)
    ats_friendly_breakdown = ats_details.get("ats_friendliness_breakdown", {})

    # Treat portfolio evidence broadly: explicit portfolio flag, creative profile links,
    # project/demo links, or known personal-site style hosts in resume text.
    has_portfolio_evidence = any([
        bool(profile_signals.get("portfolio")),
        bool(profile_signals.get("behance")),
        bool(profile_signals.get("dribbble")),
        bool(profile_signals.get("figma_link")),
        int(profile_signals.get("project_links_count", 0) or 0) > 0,
        bool(re.search(r"portfolio|github\.io|netlify\.app|vercel\.app|wixsite\.com|wordpress\.com|notion\.site", full_text.lower())),
    ])

    signal_has_evidence = {
        "portfolio": has_portfolio_evidence,
        "github": bool(profile_signals.get("github")) or bool(re.search(r"github\.com|\bgithub\b", full_text.lower())),
        "linkedin": bool(profile_signals.get("linkedin")) or bool(re.search(r"linkedin\.com|\blinkedin\b", full_text.lower())),
        "kaggle": bool(profile_signals.get("kaggle")) or bool(re.search(r"kaggle\.com|\bkaggle\b", full_text.lower())),
        "huggingface": bool(profile_signals.get("huggingface")) or bool(re.search(r"huggingface\.co|\bhugging face\b", full_text.lower())),
        "figma_link": bool(profile_signals.get("figma_link")) or bool(re.search(r"figma\.com|\bfigma\b", full_text.lower())),
        "behance": bool(profile_signals.get("behance")) or bool(re.search(r"behance\.net|\bbehance\b", full_text.lower())),
        "dribbble": bool(profile_signals.get("dribbble")) or bool(re.search(r"dribbble\.com|\bdribbble\b", full_text.lower())),
    }

    strong_areas = []
    weak_points = []
    improvement_suggestions = []
    template_feedback = []

    # ============= SCORE EXPLANATION =============
    if score >= 85:
        score_explanation = "🌟 EXCELLENT - Highly optimized for ATS and role relevance"
    elif score >= 75:
        score_explanation = "✅ VERY GOOD - Strong ATS performance with minor improvement areas"
    elif score >= 65:
        score_explanation = "👍 GOOD - ATS-ready, but role-targeted refinement will help"
    elif score >= 55:
        score_explanation = "➡️ FAIR - Needs targeted optimization for better ATS match"
    elif score >= 45:
        score_explanation = "⚠️ NEEDS WORK - Significant ATS and role-fit gaps detected"
    else:
        score_explanation = "🔴 CRITICAL - Your resume requires major improvements"

    # ============= STRONG AREAS ANALYSIS =============

    # 1. Overall score feedback
    if score >= 85:
        strong_areas.append(f"🌟 Exceptional ATS score of {score:.2f}/100")
    elif score >= 75:
        strong_areas.append(f"✅ Excellent ATS score of {score:.2f}/100")
    elif score >= 65:
        strong_areas.append(f"👍 Good ATS score of {score:.2f}/100")

    # 2. Role alignment and keyword coverage
    if role_alignment >= 90:
        strong_areas.append("🎯 Outstanding role alignment - profile is strongly tailored")
    elif role_alignment >= 80:
        strong_areas.append("🎯 Strong role alignment with good skill targeting")
    elif keyword_coverage >= 70:
        strong_areas.append("📌 Good required keyword coverage for the selected role")

    # 3. Present required skills
    if len(present_skills) >= 4:
        strong_areas.append(f"✔️ {len(present_skills)} required technical skills detected")

    # 4. Nice-to-have skills
    if len(nice_skills) >= 3:
        strong_areas.append(f"⭐ {len(nice_skills)} role-relevant bonus skills detected")

    # 5a. Conditional requirement checks
    if met_conditions:
        strong_areas.append(f"🧩 Role conditions satisfied: {len(met_conditions)}")

    if inferred_backend_language in {"python", "java", "node"}:
        strong_areas.append(f"🛠️ Backend language detected: {inferred_backend_language.title()}")
    elif inferred_backend_language == "multi_stack":
        strong_areas.append("🛠️ Multi-stack backend profile detected")

    # 5. Section completeness
    if section_completeness >= 90:
        strong_areas.append("📋 Complete resume structure - all key sections present")
    elif section_completeness >= 75:
        strong_areas.append("📑 Well-organized structure with solid section coverage")

    # 6. Action verbs
    if action_verb_score >= 85:
        strong_areas.append("💪 Excellent use of powerful action verbs")
    elif action_verb_score >= 75:
        strong_areas.append("💼 Good professional language and impact words")

    # 7. Consistency
    if consistency_score >= 85:
        strong_areas.append("🎨 Professional and consistent formatting")

    if ats_friendly_score >= 85:
        strong_areas.append("🤖 ATS-friendly formatting and layout signals are strong")

    if role_signal_score >= 85:
        strong_areas.append("🔎 Helpful supporting evidence signals detected")

    # 8. Experience level
    exp_tier = experience_level.get("tier", "entry")
    if exp_tier == "senior":
        strong_areas.append("👔 Senior-level experience clearly demonstrated")
    elif exp_tier == "mid":
        strong_areas.append("🚀 Mid-career profile well-represented")

    # ============= WEAK POINTS ANALYSIS =============

    # 1. Critical score issues
    if score < 45:
        weak_points.append(f"🔴 CRITICAL: Very low ATS score ({score:.2f}/100) - major issues present")
    elif score < 55:
        weak_points.append(f"⚠️ Low ATS score ({score:.2f}/100) - significant issues to address")
    elif score < 65:
        weak_points.append(f"➡️ Below-optimal ATS score ({score:.2f}/100) - improvements needed")

    # 2. Role alignment and keyword gaps
    if role_alignment < 55:
        weak_points.append("🚫 Role alignment is low - resume is not sufficiently tailored to the selected role")
    elif role_alignment < 70:
        weak_points.append(f"⚠️ Role alignment at {role_alignment:.0f}% - tune content toward target role")

    if keyword_coverage < 50:
        weak_points.append("🚫 Critical skill gap - less than 50% keyword coverage")
    elif keyword_coverage < 70:
        weak_points.append(f"⚠️ Keyword coverage at {keyword_coverage:.0f}% - add more relevant skills")

    if missing_conditions:
        weak_points.append(f"🧩 Missing role condition(s): {', '.join(missing_conditions[:2])}")

    # 3. Missing critical skills
    if len(missing_skills) > 0:
        if len(missing_skills) <= 2:
            skills_str = ", ".join(missing_skills)
            weak_points.append(f"❌ Missing critical role skill: {skills_str}")
        else:
            skills_str = ", ".join(missing_skills[:3])
            remaining = len(missing_skills) - 3
            weak_points.append(f"❌ Missing {len(missing_skills)} key skills: {skills_str}{'...' if remaining > 0 else ''}")

    # 4. Missing sections
    if missing_sections:
        if len(missing_sections) == 1:
            weak_points.append(f"📌 Missing section: {missing_sections[0].title()}")
        else:
            sections_str = ", ".join([s.title() for s in missing_sections[:2]])
            weak_points.append(f"📌 Missing sections: {sections_str}")

    # 5. Action verb issues
    if action_verb_score < 60:
        weak_points.append("⚠️ Weak language - limited use of impact verbs")
    elif action_verb_score < 75:
        weak_points.append("💭 Could use stronger action verbs to highlight achievements")

    # 6. Length issues
    word_count = len(parsed["full_text"].split())
    if word_count < 300:
        weak_points.append(f"📄 Resume too short ({word_count} words) - add more details")
    elif word_count > 1100:
        weak_points.append(f"📄 Resume too long ({word_count} words) - consider condensing")

    # 7. Formatting
    if ats_details["formatting_score"] < 70:
        weak_points.append("🎯 Formatting needs improvement - use more bullet points")

    # 8. Consistency
    if consistency_score < 70:
        weak_points.append("🎨 Formatting inconsistencies detected - needs professional polish")

    if ats_friendly_score < 70:
        weak_points.append("🤖 ATS parseability is below target - improve headings, bullets, and contact clarity")

    # ============= IMPROVEMENT SUGGESTIONS =============

    # Priority-based suggestions
    priority_num = 1

    # P1: Critical keyword gaps
    if len(missing_skills) > 0:
        priority_skills = missing_skills[:3]
        improvement_suggestions.append(
            f"🎯 PRIORITY {priority_num}: Add these missing role-critical skills: {', '.join(priority_skills)}"
        )
        priority_num += 1

        for skill in priority_skills:
            hint = SKILL_ACTION_HINTS.get(skill.lower(), "Add one quantified project bullet proving this skill in real work.")
            improvement_suggestions.append(f"🛠️ ACTION: {skill} -> {hint}")

    if missing_conditions:
        improvement_suggestions.append(
            f"🧩 PRIORITY {priority_num}: Satisfy role condition(s): {', '.join(missing_conditions[:2])}"
        )
        priority_num += 1

    if missing_required_role_signals:
        for signal_key in missing_required_role_signals[:1]:
            hint = ROLE_SIGNAL_HINTS.get(signal_key, "Add concrete proof for this role-evidence requirement.")
            improvement_suggestions.append(f"💡 OPTIONAL: {signal_key.replace('_', ' ')} -> {hint}")

    if missing_role_signals and not missing_required_role_signals:
        actionable_optional_signal = None
        for signal_key in missing_role_signals:
            if not signal_has_evidence.get(signal_key, False):
                actionable_optional_signal = signal_key
                break

        if actionable_optional_signal:
            optional_signal = actionable_optional_signal.replace("_", " ")
            improvement_suggestions.append(f"💡 OPTIONAL: Add {optional_signal} evidence to strengthen credibility")

    if role_label in PORTFOLIO_RECOMMENDED_ROLES and not has_portfolio_evidence:
        improvement_suggestions.append(
            "💡 OPTIONAL: Portfolio missing - add one portfolio or project showcase link to improve recruiter trust"
        )

    # P2: Missing sections
    if missing_sections:
        improvement_suggestions.append(
            f"📋 PRIORITY {priority_num}: Add missing '{missing_sections[0].title()}' section"
        )
        priority_num += 1

    section_scores = ats_details["sections"].get("quality_scores", {})
    weakest_section = None
    weakest_score = 1.0
    for section_name, section_score in section_scores.items():
        if section_name in missing_sections:
            continue
        if section_score < weakest_score:
            weakest_section = section_name
            weakest_score = section_score

    if weakest_section and weakest_score < 0.75:
        section_hint = ats_details["sections"].get("section_feedback", {}).get(
            weakest_section,
            "Add clearer, role-relevant details to this section.",
        )
        improvement_suggestions.append(
            f"🧱 PRIORITY {priority_num}: Strengthen '{weakest_section.title()}' section - {section_hint}"
        )
        priority_num += 1

    # P3: Language improvement
    if action_verb_score < 80:
        improvement_suggestions.append(
            f"💪 PRIORITY {priority_num}: Rewrite experience bullets with stronger action verbs and measurable outcomes"
        )
        priority_num += 1

    if keyword_coverage < 70:
        improvement_suggestions.append(
            f"📌 PRIORITY {priority_num}: Tailor resume keywords to the job description by mirroring exact tools and role terms"
        )
        priority_num += 1

    # P4: Content depth
    if word_count < 350:
        improvement_suggestions.append(
            f"📝 PRIORITY {priority_num}: Expand resume to 350-800 words for better coverage"
        )
        priority_num += 1

    # Tech-specific suggestions
    if role_config.get("suggestions"):
        for idx, suggestion in enumerate(role_config["suggestions"][:2], 1):
            improvement_suggestions.append(f"💡 TIP {idx}: {suggestion}")

    # Experience-based tips
    if exp_tier == "junior":
        improvement_suggestions.append("📈 TIP: Build GitHub projects to showcase practical skills")
    elif exp_tier == "mid":
        improvement_suggestions.append("🎯 TIP: Add metrics to quantify achievements (e.g., 'improved speed by 40%')")
    elif exp_tier == "senior":
        improvement_suggestions.append("👔 TIP: Highlight leadership and architectural decisions")

    # Formatting tips
    if consistency_score < 85:
        improvement_suggestions.append("🎨 TIP: Use consistent fonts and formatting throughout")

    if ats_details["formatting_score"] < 75:
        improvement_suggestions.append("📄 TIP: Use 2-4 concise bullets per experience entry with one metric in at least half of them")

    if ats_friendly_score < 80:
        if ats_friendly_breakdown.get("heading_structure", 100) < 75:
            improvement_suggestions.append("🤖 ATS TIP: Use explicit headings: Skills, Experience, Projects, Education")
        if ats_friendly_breakdown.get("contact_readability", 100) < 75:
            improvement_suggestions.append("🤖 ATS TIP: Add clearly readable email, phone, and one professional profile link")
        if ats_friendly_breakdown.get("table_density", 100) < 75:
            improvement_suggestions.append("🤖 ATS TIP: Avoid table-like layouts and keep content in plain text bullets")

    # ============= TEMPLATE & LAYOUT FEEDBACK =============

    template_feedback.append("✅ Use standard fonts (Arial, Calibri, Times New Roman)")
    template_feedback.append("✅ Font size 10-12pt for body text")
    template_feedback.append("✅ Single-column layout (avoid multi-column designs)")
    template_feedback.append("✅ Standard margins (0.5-1 inch)")
    template_feedback.append("✅ Use bullet points for better readability")

    if ats_details["formatting_score"] < 80:
        template_feedback.append("⚠️ Add more bullet points for better ATS parsing")

    template_feedback.append("⚠️ Avoid tables, images, and graphics")
    template_feedback.append("⚠️ Don't use headers/footers with content")
    template_feedback.append("✅ Save as PDF with embedded fonts")
    template_feedback.append("✅ Filename: FirstName_LastName_Role.pdf")

    # Ensure we always have feedback
    if not strong_areas:
        strong_areas.append("Resume analysis completed")

    return {
        "strong_areas": strong_areas,
        "weak_points": weak_points,
        "improvement_suggestions": improvement_suggestions,
        "template_feedback": template_feedback,
        "score_explanation": score_explanation
    }
