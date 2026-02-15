from config import ROLE_CONFIG
import re

def keyword_match_score(skills: list, full_text: str, role_key: str) -> dict:
    config = ROLE_CONFIG[role_key]
    text_lower = full_text.lower()

    present_required, missing_required = [], []
    for kw in config["required_skills"]:
        if kw in text_lower:
            present_required.append(kw)
        else:
            missing_required.append(kw)

    present_nice = [kw for kw in config["nice_to_have"] if kw in text_lower]

    coverage = len(present_required) / max(1, len(config["required_skills"])) * 100

    return {
        "required_present": present_required,
        "required_missing": missing_required,
        "nice_present": present_nice,
        "coverage": coverage,
    }

def section_completeness(sections: dict) -> dict:
    expected = ["skills", "education", "experience", "projects"]
    present, missing = [], []

    for e in expected:
        if e == "experience":
            ok = sections.get("experience") or sections.get("work experience")
        else:
            ok = sections.get(e)
        if ok and ok.strip():
            present.append(e)
        else:
            missing.append(e)

    completeness = len(present) / len(expected) * 100
    return {
        "present": present,
        "missing": missing,
        "completeness": completeness,
    }

def length_score(full_text: str) -> float:
    words = len(full_text.split())
    if 350 <= words <= 800:
        return 100.0
    elif 250 <= words < 350 or 800 < words <= 1100:
        return 75.0
    else:
        return 50.0

def formatting_score(full_text: str) -> float:
    lines = full_text.splitlines()
    bullet_lines = [l for l in lines if re.match(r"^\s*[-•*]", l)]
    ratio = len(bullet_lines) / max(1, len(lines))

    if 0.05 <= ratio <= 0.4:
        return 90.0
    elif ratio > 0.4:
        return 70.0
    else:
        return 60.0

def compute_ats_score(parsed: dict, role_key: str) -> dict:
    full_text = parsed["full_text"]
    sections = parsed["sections"]
    skills = parsed["skills"]

    km = keyword_match_score(skills, full_text, role_key)
    sc = section_completeness(sections)
    ls = length_score(full_text)
    fs = formatting_score(full_text)

    score = (
        0.5 * km["coverage"] +
        0.25 * sc["completeness"] +
        0.15 * ls +
        0.10 * fs
    )

    return {
        "ats_score": round(score, 1),
        "keyword_match": km,
        "sections": sc,
        "length_score": round(ls, 1),
        "formatting_score": round(fs, 1),
    }
