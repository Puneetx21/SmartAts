from config import ROLE_CONFIG
import re

def keyword_match_score(skills: list, full_text: str, role_key: str) -> dict:
    """Enhanced keyword matching with phrase detection"""
    config = ROLE_CONFIG[role_key]
    text_lower = full_text.lower()

    present_required, missing_required = [], []
    for kw in config["required_skills"]:
        # Check for exact keyword or word boundary
        pattern = rf"\b{re.escape(kw)}\b"
        if re.search(pattern, text_lower):
            present_required.append(kw)
        else:
            missing_required.append(kw)

    present_nice = []
    for kw in config["nice_to_have"]:
        pattern = rf"\b{re.escape(kw)}\b"
        if re.search(pattern, text_lower):
            present_nice.append(kw)
    
    # Weighted coverage: required skills are more important
    required_coverage = len(present_required) / max(1, len(config["required_skills"])) * 100
    nice_coverage = len(present_nice) / max(1, len(config["nice_to_have"])) * 100 if config["nice_to_have"] else 0
    
    # Combined coverage with more weight on required skills
    coverage = (required_coverage * 0.8) + (nice_coverage * 0.2)

    return {
        "required_present": present_required,
        "required_missing": missing_required,
        "nice_present": present_nice,
        "coverage": coverage,
        "required_coverage": required_coverage,
        "nice_coverage": nice_coverage,
        "total_skills_matched": len(present_required) + len(present_nice),
    }

def section_completeness(sections: dict) -> dict:
    """Evaluate resume section completeness with scoring"""
    expected = ["skills", "education", "experience", "projects"]
    present, missing = [], []
    section_quality = {}

    for e in expected:
        if e == "experience":
            ok = sections.get("experience") or sections.get("work experience")
        else:
            ok = sections.get(e)
        
        if ok and ok.strip():
            present.append(e)
            # Score quality of section (word count)
            word_count = len(ok.split())
            if word_count > 50:
                section_quality[e] = 1.0
            elif word_count > 20:
                section_quality[e] = 0.8
            else:
                section_quality[e] = 0.6
        else:
            missing.append(e)
            section_quality[e] = 0.0

    completeness = len(present) / len(expected) * 100
    
    return {
        "present": present,
        "missing": missing,
        "completeness": completeness,
        "quality_scores": section_quality,
        "quality_average": sum(section_quality.values()) / len(section_quality),
    }

def length_score(full_text: str) -> float:
    """Score based on resume length with optimized ranges"""
    words = len(full_text.split())
    if 400 <= words <= 750:
        return 100.0
    elif 300 <= words < 400 or 750 < words <= 850:
        return 90.0
    elif 250 <= words < 300 or 850 < words <= 1000:
        return 75.0
    elif words < 250:
        return 50.0
    else:
        return 60.0

def formatting_score(full_text: str) -> float:
    """Score based on resume formatting and structure"""
    lines = full_text.splitlines()
    bullet_lines = [l for l in lines if re.match(r"^\s*[-•*]", l)]
    ratio = len(bullet_lines) / max(1, len(lines))

    if 0.1 <= ratio <= 0.35:
        return 95.0
    elif 0.05 <= ratio < 0.1 or 0.35 < ratio <= 0.45:
        return 85.0
    elif ratio > 0.45:
        return 75.0
    else:
        return 60.0

def experience_level_detection(full_text: str) -> dict:
    """Detect experience level from resume with better accuracy"""
    text_lower = full_text.lower()
    
    # Keywords for different experience levels with weights
    senior_keywords = [
        ("senior", 2), ("lead", 2), ("principal", 3), ("architect", 3), 
        ("director", 3), ("head of", 3), ("10+ years", 2), ("15+ years", 2),
        ("vp ", 3), ("c-level", 3), ("management", 1)
    ]
    mid_keywords = [
        ("mid-level", 2), ("intermediate", 1), ("5+ years", 2), 
        ("7+ years", 2), ("specialist", 1), ("team lead", 2)
    ]
    junior_keywords = [
        ("junior", 2), ("entry-level", 1), ("entry level", 1), 
        ("0-2 years", 1), ("1-3 years", 1), ("graduate", 1), ("fresher", 1)
    ]
    
    senior_score = sum(w for kw, w in senior_keywords if kw in text_lower)
    mid_score = sum(w for kw, w in mid_keywords if kw in text_lower)
    junior_score = sum(w for kw, w in junior_keywords if kw in text_lower)
    
    if senior_score > mid_score and senior_score > junior_score:
        level = "Senior (5-10+ YoE)"
        tier = "senior"
    elif mid_score > junior_score:
        level = "Mid-level (3-5 YoE)"
        tier = "mid"
    elif junior_score > 0:
        level = "Junior (0-3 YoE)"
        tier = "junior"
    else:
        level = "Entry Level"
        tier = "entry"
    
    return {
        "level": level,
        "tier": tier,
        "senior_score": senior_score,
        "mid_score": mid_score,
        "junior_score": junior_score,
    }

def action_verb_score(full_text: str) -> float:
    """Score based on presence and diversity of action verbs"""
    action_verbs = [
        "developed", "designed", "implemented", "created", "built", "architected",
        "led", "managed", "coordinated", "optimized", "improved", "enhanced",
        "resolved", "debugged", "deployed", "configured", "maintained", "tested",
        "automated", "integrated", "solved", "pioneered", "spearheaded",
        "accelerated", "achieved", "collaborated", "delivered", "engineered",
        "established", "executed", "expanded", "facilitated", "formulated",
        "generated", "governed", "guided", "innovated", "increased",
        "maximized", "minimized", "modernized", "monitored", "negotiated"
    ]
    
    text_lower = full_text.lower()
    found_verbs = set()
    verb_count = 0
    
    for verb in action_verbs:
        pattern = rf"\b{verb}\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            found_verbs.add(verb)
            verb_count += matches
    
    # Score based on verb diversity and frequency
    diversity_score = len(found_verbs) / len(action_verbs) * 100
    frequency_score = min(100, verb_count / 8 * 100)
    
    combined = (diversity_score * 0.4) + (frequency_score * 0.6)
    
    if combined >= 75:
        return 95.0
    elif combined >= 60:
        return 85.0
    elif combined >= 45:
        return 70.0
    elif combined >= 30:
        return 55.0
    else:
        return 40.0

def technical_depth_score(skills: list, role_key: str) -> float:
    """Assess technical depth based on skill diversity and quality"""
    config = ROLE_CONFIG[role_key]
    all_required = set(config["required_skills"])
    all_nice = set(config["nice_to_have"])
    all_expected = all_required.union(all_nice)
    
    relevant_skills = [s for s in skills if s in all_expected]
    
    if not all_expected:
        return 50.0
    
    # Coverage of expected skills
    skill_coverage = len(set(relevant_skills)) / len(all_expected) * 100
    
    # Bonus for having more unique skills (beyond expected)
    unique_skills = len(set(relevant_skills)) / max(1, len(skills)) * 100
    
    depth = (skill_coverage * 0.7) + (unique_skills * 0.3)
    
    return min(100.0, depth * 1.05)

def consistency_score(full_text: str, sections: dict) -> float:
    """Score the consistency and professionalism of resume"""
    score = 50.0
    
    # Check for proper capitalization
    lines = full_text.splitlines()
    capitalized_lines = sum(1 for line in lines if line and line[0].isupper())
    if capitalized_lines / max(1, len(lines)) > 0.7:
        score += 10
    
    # Check for consistent formatting
    if sections.get("skills") and sections.get("experience"):
        score += 10
    
    # Check for professional email pattern
    if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text):
        score += 10
    
    # Check for phone number pattern
    if re.search(r"\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", full_text):
        score += 10
    
    return min(100.0, score)

def compute_ats_score(parsed: dict, role_key: str) -> dict:
    """Comprehensive ATS score computation with advanced metrics"""
    full_text = parsed["full_text"]
    sections = parsed["sections"]
    skills = parsed["skills"]

    # Compute individual scores
    km = keyword_match_score(skills, full_text, role_key)
    sc = section_completeness(sections)
    ls = length_score(full_text)
    fs = formatting_score(full_text)
    exp_level = experience_level_detection(full_text)
    av_score = action_verb_score(full_text)
    td_score = technical_depth_score(skills, role_key)
    cons_score = consistency_score(full_text, sections)

    # Enhanced weighted scoring
    score = (
        0.40 * km["coverage"] +         # Keywords most important
        0.20 * sc["completeness"] +     # Complete sections needed
        0.15 * av_score +               # Action verbs show impact
        0.10 * td_score +               # Technical depth matters
        0.07 * cons_score +             # Professionalism important
        0.05 * ls +                     # Length matters less
        0.03 * fs                       # Formatting matters less
    )

    return {
        "ats_score": round(min(100.0, score), 1),
        "keyword_match": km,
        "sections": sc,
        "length_score": round(ls, 1),
        "formatting_score": round(fs, 1),
        "action_verb_score": round(av_score, 1),
        "technical_depth_score": round(td_score, 1),
        "consistency_score": round(cons_score, 1),
        "experience_level": exp_level,
    }
