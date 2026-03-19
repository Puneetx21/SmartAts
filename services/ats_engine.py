from config import ROLE_CONFIG
import re

TERM_VARIANTS = {
    "node": {"node", "node.js", "node js", "nodejs"},
    "react": {"react", "react.js", "reactjs"},
    "nextjs": {"nextjs", "next.js", "next js"},
    "vue": {"vue", "vue.js", "vuejs"},
    "angular": {"angular", "angular.js"},
    "c#": {"c#", "c sharp", "csharp"},
    "c++": {"c++", "cpp"},
    "dotnet": {"dotnet", ".net", ".net core", "asp.net", "asp net"},
    "spring": {"spring", "spring framework"},
    "spring boot": {"spring boot", "springboot"},
    "mongodb": {"mongodb", "mongo", "mongo db", "mongo-db"},
    "express": {"express", "express.js", "expressjs"},
    "django": {"django", "django framework"},
    "flask": {"flask", "flask framework"},
    "fastapi": {"fastapi", "fast api"},
    "postgresql": {"postgresql", "postgres", "postgre sql", "psql"},
    "rest api": {"rest api", "restful api", "rest api design", "rest"},
    "typescript": {"typescript", "ts"},
    "jwt": {"jwt", "json web token", "json web tokens"},
    "junit": {"junit", "j unit"},
    "golang": {"golang", "go"},
    "rest": {"rest", "rest api", "restful", "restful api"},
    "ci/cd": {"ci/cd", "ci cd", "cicd"},
}

DEFAULT_SCORING_WEIGHTS = {
    "keyword": 0.45,
    "sections": 0.18,
    "action_verbs": 0.12,
    "technical_depth": 0.10,
    "consistency": 0.08,
    "length": 0.04,
    "formatting": 0.03,
}

ROLE_SCORING_WEIGHTS = {
    "python_fullstack_developer": {
        "keyword": 0.43,
        "sections": 0.17,
        "action_verbs": 0.10,
        "technical_depth": 0.13,
        "consistency": 0.08,
        "length": 0.05,
        "formatting": 0.04,
    },
    "mern_developer": {
        "keyword": 0.44,
        "sections": 0.14,
        "action_verbs": 0.12,
        "technical_depth": 0.14,
        "consistency": 0.07,
        "length": 0.05,
        "formatting": 0.04,
    },
    "java_fullstack_developer": {
        "keyword": 0.44,
        "sections": 0.16,
        "action_verbs": 0.10,
        "technical_depth": 0.14,
        "consistency": 0.08,
        "length": 0.05,
        "formatting": 0.03,
    },
}


def _normalize_for_match(text: str) -> str:
    normalized = text.lower()
    normalized = re.sub(r"\r\n|\r", "\n", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"[^a-z0-9+#.\-\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _normalize_term(term: str) -> str:
    return _normalize_for_match(term)


def _term_variants(term: str) -> set:
    base = _normalize_term(term)
    variants = {base}

    mapped = TERM_VARIANTS.get(base)
    if mapped:
        variants.update({_normalize_term(v) for v in mapped})

    if "." in base:
        variants.add(base.replace(".", ""))
        variants.add(base.replace(".", " "))

    if "-" in base:
        variants.add(base.replace("-", " "))

    return {v for v in variants if v}


def _contains_term(text: str, skills_set: set, term: str) -> bool:
    for variant in _term_variants(term):
        pattern = rf"(?<![a-z0-9+#.]){re.escape(variant)}(?![a-z0-9+#.])"
        if re.search(pattern, text):
            return True

        if variant in skills_set:
            return True

    return False


def _get_scoring_weights(role_key: str) -> dict:
    return ROLE_SCORING_WEIGHTS.get(role_key, DEFAULT_SCORING_WEIGHTS)


def keyword_match_score(skills: list, full_text: str, role_key: str) -> dict:
    """Role-aware keyword matching using normalized text for PDF/DOCX stability."""
    config = ROLE_CONFIG[role_key]
    normalized_text = _normalize_for_match(full_text)
    normalized_skills = {_normalize_term(s) for s in skills}

    present_required, missing_required = [], []
    for kw in config["required_skills"]:
        if _contains_term(normalized_text, normalized_skills, kw):
            present_required.append(kw)
        else:
            missing_required.append(kw)

    present_nice = []
    for kw in config["nice_to_have"]:
        if _contains_term(normalized_text, normalized_skills, kw):
            present_nice.append(kw)

    required_coverage = len(present_required) / max(1, len(config["required_skills"])) * 100
    nice_coverage = len(present_nice) / max(1, len(config["nice_to_have"])) * 100 if config["nice_to_have"] else 0
    coverage = (required_coverage * 0.85) + (nice_coverage * 0.15)
    role_alignment = (required_coverage * 0.9) + (nice_coverage * 0.1)

    return {
        "required_present": present_required,
        "required_missing": missing_required,
        "nice_present": present_nice,
        "coverage": coverage,
        "required_coverage": required_coverage,
        "nice_coverage": nice_coverage,
        "role_alignment": role_alignment,
        "total_skills_matched": len(present_required) + len(present_nice),
    }


def section_completeness(sections: dict) -> dict:
    """Evaluate section presence and depth using quality-adjusted scoring."""
    expected = ["skills", "education", "experience", "projects"]
    present, missing = [], []
    section_quality = {}

    for section in expected:
        content = sections.get(section, "")

        if content and content.strip():
            present.append(section)
            words = len(content.split())

            if section == "skills":
                quality = 1.0 if words >= 15 else 0.75 if words >= 8 else 0.5
            elif section in {"experience", "projects"}:
                quality = 1.0 if words >= 80 else 0.75 if words >= 35 else 0.5
            else:
                quality = 1.0 if words >= 30 else 0.75 if words >= 15 else 0.5

            section_quality[section] = quality
        else:
            missing.append(section)
            section_quality[section] = 0.0

    presence_score = len(present) / len(expected) * 100
    quality_average = sum(section_quality.values()) / len(section_quality)
    completeness = (presence_score * 0.75) + (quality_average * 100 * 0.25)

    return {
        "present": present,
        "missing": missing,
        "completeness": completeness,
        "quality_scores": section_quality,
        "quality_average": quality_average,
    }


def length_score(full_text: str) -> float:
    """Length scoring centered on an optimal one-page to one-and-half-page resume."""
    words = len(full_text.split())
    target_words = 550
    score = 100 - abs(words - target_words) * 0.12

    if words < 220:
        score = min(score, 55)
    elif words > 1200:
        score = min(score, 60)

    return max(40.0, min(100.0, score))


def formatting_score(full_text: str, sections: dict) -> float:
    """Format scoring designed to be stable across equivalent PDF and DOCX content."""
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    if not lines:
        return 40.0

    bullet_lines = [line for line in lines if re.match(r"^([\-•*]|\d+[.)])\s+", line)]
    quantified_lines = [line for line in lines if re.search(r"\b\d+(?:\.\d+)?%?\b", line)]
    avg_line_words = sum(len(line.split()) for line in lines) / len(lines)
    heading_count = len([h for h in ["summary", "skills", "experience", "projects", "education"] if sections.get(h)])

    bullet_ratio = len(bullet_lines) / len(lines)
    score = 55.0

    if 0.08 <= bullet_ratio <= 0.45:
        score += 18
    elif bullet_ratio > 0:
        score += 10

    score += min(14, len(quantified_lines) * 1.2)
    score += min(10, heading_count * 2)

    if 4 <= avg_line_words <= 16:
        score += 10
    else:
        score += 5

    return min(100.0, score)


def experience_level_detection(full_text: str) -> dict:
    """Detect experience level from years and seniority signals."""
    text = full_text.lower()

    year_mentions = [int(num) for num in re.findall(r"\b(\d{1,2})\+?\s*(?:years|year|yrs)\b", text)]
    years_estimate = max(year_mentions) if year_mentions else None

    senior_score = len(re.findall(r"\b(senior|principal|architect|director|head|lead)\b", text))
    mid_score = len(re.findall(r"\b(mid|intermediate|specialist|team lead)\b", text))
    junior_score = len(re.findall(r"\b(junior|entry|fresher|graduate|intern)\b", text))

    if years_estimate is not None:
        if years_estimate >= 8:
            tier = "senior"
            level = "Senior (8+ YoE)"
        elif years_estimate >= 4:
            tier = "mid"
            level = "Mid-level (4-7 YoE)"
        elif years_estimate >= 1:
            tier = "junior"
            level = "Junior (1-3 YoE)"
        else:
            tier = "entry"
            level = "Entry Level"
    elif senior_score >= max(mid_score, junior_score) and senior_score > 0:
        tier = "senior"
        level = "Senior (inferred)"
    elif mid_score >= junior_score and mid_score > 0:
        tier = "mid"
        level = "Mid-level (inferred)"
    elif junior_score > 0:
        tier = "junior"
        level = "Junior (inferred)"
    else:
        tier = "entry"
        level = "Entry Level"

    description = (
        f"Estimated from {years_estimate}+ years and role keywords"
        if years_estimate is not None
        else "Estimated from role titles and experience signals"
    )

    return {
        "level": level,
        "tier": tier,
        "description": description,
        "years_estimate": years_estimate,
        "senior_score": senior_score,
        "mid_score": mid_score,
        "junior_score": junior_score,
    }


def action_verb_score(full_text: str) -> float:
    """Score impact-oriented writing using verb diversity and usage frequency."""
    action_stems = [
        "develop", "design", "implement", "create", "build", "architect", "lead", "manage",
        "coordinate", "optimiz", "improv", "enhanc", "resolv", "debug", "deploy", "configur",
        "maintain", "test", "automat", "integrat", "accelerat", "achiev", "deliver", "engineer",
        "execut", "innov", "increas", "moderniz", "monitor",
    ]

    text = full_text.lower()
    matched_stems = set()
    total_matches = 0

    for stem in action_stems:
        pattern = rf"\b{stem}(?:e|ed|es|ing|ion|ions)?\b"
        matches = re.findall(pattern, text)
        if matches:
            matched_stems.add(stem)
            total_matches += len(matches)

    diversity = len(matched_stems) / len(action_stems)
    frequency = min(1.0, total_matches / 14)
    score = (diversity * 70) + (frequency * 30)

    return min(100.0, max(35.0, score))


def technical_depth_score(skills: list, role_key: str, keyword_data: dict) -> float:
    """Technical depth emphasizes required-role coverage plus relevant breadth."""
    req_cov = keyword_data["required_coverage"]
    nice_cov = keyword_data["nice_coverage"]
    unique_skills = len({_normalize_term(skill) for skill in skills if skill.strip()})

    breadth_component = min(100.0, unique_skills * 4.0)
    depth = (req_cov * 0.7) + (nice_cov * 0.2) + (breadth_component * 0.1)

    return min(100.0, depth)


def consistency_score(full_text: str, sections: dict) -> float:
    """Professional consistency checks with contact info, structure, and style signals."""
    score = 45.0
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]

    if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text):
        score += 12

    if re.search(r"\+?\d[\d\s().-]{8,}\d", full_text):
        score += 10

    if re.search(r"linkedin|github|portfolio|https?://", full_text.lower()):
        score += 6

    if sections.get("experience") and sections.get("education") and sections.get("skills"):
        score += 12

    all_caps_lines = sum(1 for line in lines if len(line) > 4 and line.isupper())
    if all_caps_lines / max(1, len(lines)) < 0.2:
        score += 8

    return min(100.0, score)


def compute_ats_score(parsed: dict, role_key: str) -> dict:
    """Comprehensive ATS score computation with role-focused weighted metrics."""
    full_text = parsed["full_text"]
    sections = parsed["sections"]
    skills = parsed["skills"]

    km = keyword_match_score(skills, full_text, role_key)
    sc = section_completeness(sections)
    ls = length_score(full_text)
    fs = formatting_score(full_text, sections)
    exp_level = experience_level_detection(full_text)
    av_score = action_verb_score(full_text)
    td_score = technical_depth_score(skills, role_key, km)
    cons_score = consistency_score(full_text, sections)

    weights = _get_scoring_weights(role_key)
    score_components = {
        "keyword": weights["keyword"] * km["coverage"],
        "sections": weights["sections"] * sc["completeness"],
        "action_verbs": weights["action_verbs"] * av_score,
        "technical_depth": weights["technical_depth"] * td_score,
        "consistency": weights["consistency"] * cons_score,
        "length": weights["length"] * ls,
        "formatting": weights["formatting"] * fs,
    }
    score = sum(score_components.values())

    return {
        "ats_score": round(min(100.0, score), 2),
        "keyword_match": km,
        "sections": sc,
        "length_score": round(ls, 1),
        "formatting_score": round(fs, 1),
        "action_verb_score": round(av_score, 1),
        "technical_depth_score": round(td_score, 1),
        "consistency_score": round(cons_score, 1),
        "experience_level": exp_level,
        "scoring_weights": weights,
        "score_components": {k: round(v, 2) for k, v in score_components.items()},
    }
