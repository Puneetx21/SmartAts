"""Pure Python feedback generator for resume analysis - Enhanced"""
from config import ROLE_CONFIG


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
    missing_sections = ats_details["sections"]["missing"]
    score = ats_details["ats_score"]
    experience_level = ats_details.get("experience_level", {})
    action_verb_score = ats_details.get("action_verb_score", 50)
    consistency_score = ats_details.get("consistency_score", 50)
    keyword_coverage = ats_details["keyword_match"]["required_coverage"]
    
    strong_areas = []
    weak_points = []
    improvement_suggestions = []
    template_feedback = []
    
    # ============= SCORE EXPLANATION =============
    if score >= 85:
        score_explanation = "🌟 EXCELLENT - Your resume is highly optimized for ATS systems"
    elif score >= 75:
        score_explanation = "✅ VERY GOOD - Your resume passes ATS filters well"
    elif score >= 65:
        score_explanation = "👍 GOOD - Your resume is reasonably ATS-optimized"
    elif score >= 55:
        score_explanation = "➡️ FAIR - Your resume needs some optimization"
    elif score >= 45:
        score_explanation = "⚠️ NEEDS WORK - Your resume has significant ATS issues"
    else:
        score_explanation = "🔴 CRITICAL - Your resume requires major improvements"
    
    # ============= STRONG AREAS ANALYSIS =============
    
    # 1. Overall score feedback
    if score >= 85:
        strong_areas.append(f"🌟 Exceptional ATS score of {score}/100")
    elif score >= 75:
        strong_areas.append(f"✅ Excellent ATS score of {score}/100")
    elif score >= 65:
        strong_areas.append(f"👍 Good ATS score of {score}/100")
    
    # 2. Keyword coverage
    if keyword_coverage >= 90:
        strong_areas.append("🎯 Outstanding keyword coverage - you have most required skills")
    elif keyword_coverage >= 80:
        strong_areas.append("🎯 Strong keyword coverage - excellent skill alignment")
    elif keyword_coverage >= 70:
        strong_areas.append("📌 Good keyword presence - most required skills are listed")
    
    # 3. Present required skills
    if len(present_skills) >= 4:
        strong_areas.append(f"✔️ {len(present_skills)} required technical skills detected")
    
    # 4. Nice-to-have skills
    if len(nice_skills) >= 3:
        strong_areas.append(f"⭐ {len(nice_skills)} bonus skills found - nice job!")
    
    # 5. Section completeness
    if ats_details["sections"]["completeness"] >= 90:
        strong_areas.append("📋 Complete resume structure - all key sections present")
    elif ats_details["sections"]["completeness"] >= 75:
        strong_areas.append("📑 Well-organized - most important sections included")
    
    # 6. Action verbs
    if action_verb_score >= 85:
        strong_areas.append("💪 Excellent use of powerful action verbs")
    elif action_verb_score >= 75:
        strong_areas.append("💼 Good professional language and impact words")
    
    # 7. Consistency
    if consistency_score >= 85:
        strong_areas.append("🎨 Professional and consistent formatting")
    
    # 8. Experience level
    exp_tier = experience_level.get("tier", "entry")
    if exp_tier == "senior":
        strong_areas.append("👔 Senior-level experience clearly demonstrated")
    elif exp_tier == "mid":
        strong_areas.append("🚀 Mid-career profile well-represented")
    
    # ============= WEAK POINTS ANALYSIS =============
    
    # 1. Critical score issues
    if score < 45:
        weak_points.append(f"🔴 CRITICAL: Very low ATS score ({score}/100) - major issues present")
    elif score < 55:
        weak_points.append(f"⚠️ Low ATS score ({score}/100) - significant issues to address")
    elif score < 65:
        weak_points.append(f"➡️ Below-optimal ATS score ({score}/100) - improvements needed")
    
    # 2. Keyword gaps
    if keyword_coverage < 50:
        weak_points.append("🚫 Critical skill gap - less than 50% keyword coverage")
    elif keyword_coverage < 70:
        weak_points.append(f"⚠️ Keyword coverage at {keyword_coverage:.0f}% - add more relevant skills")
    
    # 3. Missing critical skills
    if len(missing_skills) > 0:
        if len(missing_skills) <= 2:
            skills_str = ", ".join(missing_skills)
            weak_points.append(f"❌ Missing critical skill: {skills_str}")
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
    elif word_count > 1000:
        weak_points.append(f"📄 Resume too long ({word_count} words) - consider condensing")
    
    # 7. Formatting
    if ats_details["formatting_score"] < 70:
        weak_points.append("🎯 Formatting needs improvement - use more bullet points")
    
    # 8. Consistency
    if consistency_score < 70:
        weak_points.append("🎨 Formatting inconsistencies detected - needs professional polish")
    
    # ============= IMPROVEMENT SUGGESTIONS =============
    
    # Priority-based suggestions
    priority_num = 1
    
    # P1: Critical keyword gaps
    if len(missing_skills) > 0:
        priority_skills = missing_skills[:2]
        improvement_suggestions.append(
            f"🎯 PRIORITY {priority_num}: Add these critical skills: {', '.join(priority_skills)}"
        )
        priority_num += 1
    
    # P2: Missing sections
    if missing_sections:
        improvement_suggestions.append(
            f"📋 PRIORITY {priority_num}: Add missing '{missing_sections[0].title()}' section"
        )
        priority_num += 1
    
    # P3: Language improvement
    if action_verb_score < 80:
        improvement_suggestions.append(
            f"💪 PRIORITY {priority_num}: Replace weak verbs with powerful action words (e.g., 'architected' instead of 'created')"
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
        improvement_suggestions.append("")  # Blank line
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
