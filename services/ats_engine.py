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
    "rails": {"rails", "ruby on rails", "ror"},
    "kotlin": {"kotlin"},
    "swift": {"swift"},
    "swiftui": {"swiftui", "swift ui"},
    "uikit": {"uikit", "ui kit"},
    "android": {"android", "android sdk", "android development"},
    "php": {"php"},
    "laravel": {"laravel"},
    "symfony": {"symfony"},
    "go": {"go", "golang"},
    "grpc": {"grpc", "g rpc"},
    "gin": {"gin", "gin-gonic"},
    "gorm": {"gorm"},
    "entity framework": {"entity framework", "ef core", "entityframework"},
}

DEFAULT_SCORING_WEIGHTS = {
    "keyword": 0.43,
    "sections": 0.19,
    "action_verbs": 0.10,
    "technical_depth": 0.08,
    "consistency": 0.07,
    "length": 0.04,
    "formatting": 0.03,
    "role_signals": 0.01,
    "ats_friendliness": 0.05,
}

ROLE_SCORING_WEIGHTS = {
    "mern_developer": {
        "keyword": 0.42,
        "sections": 0.14,
        "action_verbs": 0.12,
        "technical_depth": 0.14,
        "consistency": 0.07,
        "length": 0.05,
        "formatting": 0.04,
        "role_signals": 0.01,
    },
    "data_scientist": {
        "keyword": 0.40,
        "sections": 0.17,
        "action_verbs": 0.11,
        "technical_depth": 0.14,
        "consistency": 0.08,
        "length": 0.05,
        "formatting": 0.03,
        "role_signals": 0.01,
    },
    "ui_ux_designer": {
        "keyword": 0.40,
        "sections": 0.17,
        "action_verbs": 0.12,
        "technical_depth": 0.09,
        "consistency": 0.10,
        "length": 0.05,
        "formatting": 0.03,
        "role_signals": 0.01,
    },
}

DEVELOPER_ROLE_KEYS = {
    "software_engineer",
    "full_stack_developer",
    "frontend_developer",
    "backend_developer",
    "web_developer",
    "python_fullstack_developer",
    "java_fullstack_developer",
    "python_developer",
    "java_developer",
    "mern_developer",
    "cpp_developer",
    "c_developer",
    "ruby_developer",
    "android_developer",
    "ios_developer",
    "dotnet_developer",
    "php_developer",
    "go_developer",
}

ROLE_SIGNAL_RULES = {
    "default": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("linkedin", 1), ("github", 1)]],
        "weighted": [
            ("has_quantified_impact", 25, 1),
            ("linkedin", 15, 1),
            ("github", 15, 1),
            ("project_links_count", 20, 1),
            ("certifications_count", 10, 1),
            ("portfolio", 5, 1),
        ],
    },
    "data_scientist": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("kaggle", 1), ("github", 1), ("huggingface", 1)]],
        "weighted": [
            ("kaggle", 20, 1),
            ("huggingface", 20, 1),
            ("github", 15, 1),
            ("project_links_count", 20, 1),
            ("has_quantified_impact", 25, 1),
        ],
    },
    "data_analyst": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("linkedin", 1), ("project_links_count", 1)]],
        "weighted": [
            ("project_links_count", 25, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 15, 1),
            ("certifications_count", 10, 1),
            ("github", 10, 1),
        ],
    },
    "ui_ux_designer": {
        "required_all": [("project_links_count", 1)],
        "required_any": [[("behance", 1), ("dribbble", 1), ("figma_link", 1)]],
        "weighted": [
            ("portfolio", 10, 1),
            ("behance", 20, 1),
            ("dribbble", 20, 1),
            ("figma_link", 15, 1),
            ("project_links_count", 20, 1),
        ],
    },
    "cloud_engineer": {
        "required_all": [("certifications_count", 1), ("has_quantified_impact", 1)],
        "required_any": [[("linkedin", 1), ("github", 1)]],
        "weighted": [
            ("certifications_count", 35, 1),
            ("has_quantified_impact", 25, 1),
            ("linkedin", 10, 1),
            ("github", 10, 1),
            ("project_links_count", 20, 1),
        ],
    },
    "cybersecurity_analyst": {
        "required_all": [("certifications_count", 1), ("has_quantified_impact", 1)],
        "required_any": [[("linkedin", 1), ("github", 1)]],
        "weighted": [
            ("certifications_count", 35, 1),
            ("has_quantified_impact", 25, 1),
            ("linkedin", 10, 1),
            ("github", 10, 1),
            ("project_links_count", 20, 1),
        ],
    },
    "cpp_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 25, 1),
            ("project_links_count", 25, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 10, 1),
        ],
    },
    "c_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("project_links_count", 30, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 10, 1),
        ],
    },
    "ruby_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("project_links_count", 25, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 10, 1),
        ],
    },
    "python_fullstack_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("project_links_count", 25, 1),
            ("portfolio", 15, 1),
            ("has_quantified_impact", 30, 1),
        ],
    },
    "java_fullstack_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("project_links_count", 25, 1),
            ("portfolio", 10, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 10, 1),
        ],
    },
    "android_developer": {
        "required_all": [("project_links_count", 1)],
        "required_any": [[("github", 1), ("portfolio", 1)]],
        "weighted": [
            ("project_links_count", 30, 1),
            ("github", 20, 1),
            ("portfolio", 20, 1),
            ("has_quantified_impact", 20, 1),
        ],
    },
    "ml_engineer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("huggingface", 1), ("kaggle", 1)]],
        "weighted": [
            ("huggingface", 25, 1),
            ("kaggle", 20, 1),
            ("github", 20, 1),
            ("project_links_count", 15, 1),
            ("has_quantified_impact", 20, 1),
        ],
    },
    "ios_developer": {
        "required_all": [("project_links_count", 1)],
        "required_any": [[("github", 1), ("portfolio", 1)]],
        "weighted": [
            ("project_links_count", 30, 1),
            ("github", 20, 1),
            ("portfolio", 20, 1),
            ("has_quantified_impact", 20, 1),
        ],
    },
    "dotnet_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("linkedin", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("linkedin", 15, 1),
            ("project_links_count", 20, 1),
            ("certifications_count", 10, 1),
            ("has_quantified_impact", 25, 1),
        ],
    },
    "php_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 20, 1),
            ("project_links_count", 25, 1),
            ("portfolio", 10, 1),
            ("has_quantified_impact", 30, 1),
        ],
    },
    "go_developer": {
        "required_all": [("has_quantified_impact", 1)],
        "required_any": [[("github", 1), ("project_links_count", 1)]],
        "weighted": [
            ("github", 25, 1),
            ("project_links_count", 20, 1),
            ("has_quantified_impact", 30, 1),
            ("linkedin", 10, 1),
        ],
    },
}


def _signal_present(signals: dict, signal_key: str, min_value: int = 1) -> bool:
    raw_value = signals.get(signal_key)
    if isinstance(raw_value, bool):
        return raw_value
    if isinstance(raw_value, (int, float)):
        return raw_value >= min_value
    return bool(raw_value)


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


def _detect_backend_language(normalized_text: str, normalized_skills: set) -> str:
    backend_languages = ["python", "java", "node"]
    detected = []
    for language in backend_languages:
        if _contains_term(normalized_text, normalized_skills, language):
            detected.append(language)

    if not detected:
        return "not_detected"

    if len(detected) == 1:
        return detected[0]

    return "multi_stack"


def _evaluate_required_groups(config: dict, normalized_text: str, normalized_skills: set) -> tuple:
    groups = config.get("any_of_skill_groups", [])
    group_results = []
    group_present_labels = []
    group_missing_labels = []
    matched_units = 0
    total_units = 0

    for group in groups:
        skills = group.get("skills", [])
        group_name = group.get("name", "Skill Group")
        min_required = max(1, int(group.get("min_required", 1)))
        is_required = bool(group.get("required", True))

        matched_skills = [skill for skill in skills if _contains_term(normalized_text, normalized_skills, skill)]
        matched_count = len(matched_skills)
        satisfied = matched_count >= min_required

        result = {
            "name": group_name,
            "required": is_required,
            "skills": skills,
            "matched": matched_skills,
            "matched_count": matched_count,
            "min_required": min_required,
            "satisfied": satisfied,
        }
        group_results.append(result)

        if is_required:
            total_units += min_required
            matched_units += min(matched_count, min_required)

            options = " OR ".join(skills)
            if satisfied:
                group_present_labels.append(f"{group_name}: {', '.join(matched_skills[:min_required])}")
            else:
                group_missing_labels.append(f"{group_name} (need {min_required}: {options})")

    return group_results, group_present_labels, group_missing_labels, matched_units, total_units


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

    (
        group_results,
        group_present_labels,
        group_missing_labels,
        group_matched_units,
        group_total_units,
    ) = _evaluate_required_groups(config, normalized_text, normalized_skills)

    total_required_units = len(config["required_skills"]) + group_total_units
    matched_required_units = len(present_required) + group_matched_units

    # ATS-friendly smoothing: long role skill lists should not over-penalize candidates.
    base_required = len(config["required_skills"])
    effective_required_total = min(base_required, 10) + max(0, base_required - 10) * 0.35 + group_total_units
    effective_required_matched = min(len(present_required), 10) + max(0, len(present_required) - 10) * 0.35 + group_matched_units

    required_coverage = effective_required_matched / max(1, effective_required_total) * 100
    nice_coverage = len(present_nice) / max(1, len(config["nice_to_have"])) * 100 if config["nice_to_have"] else 0
    coverage = (required_coverage * 0.85) + (nice_coverage * 0.15)
    role_alignment = (required_coverage * 0.9) + (nice_coverage * 0.1)
    inferred_backend_language = _detect_backend_language(normalized_text, normalized_skills)

    combined_present = present_required + group_present_labels
    combined_missing = missing_required + group_missing_labels

    return {
        "required_present": combined_present,
        "required_missing": combined_missing,
        "base_required_present": present_required,
        "base_required_missing": missing_required,
        "condition_present": group_present_labels,
        "condition_missing": group_missing_labels,
        "condition_results": group_results,
        "nice_present": present_nice,
        "coverage": coverage,
        "required_coverage": required_coverage,
        "nice_coverage": nice_coverage,
        "role_alignment": role_alignment,
        "total_skills_matched": len(combined_present) + len(present_nice),
        "inferred_backend_language": inferred_backend_language,
    }


def section_completeness(sections: dict) -> dict:
    """Evaluate section presence and depth using quality-adjusted scoring."""
    expected = ["skills", "education", "experience", "projects"]
    present, missing = [], []
    section_quality = {}
    section_word_counts = {}
    section_feedback = {}

    for section in expected:
        content = sections.get(section, "")

        if content and content.strip():
            present.append(section)
            words = len(content.split())
            section_word_counts[section] = words

            if section == "skills":
                quality = 1.0 if words >= 12 else 0.75 if words >= 6 else 0.5
                feedback = (
                    "Strong skills coverage"
                    if quality == 1.0
                    else "Add more specific tools, frameworks, and proficiency context"
                )
            elif section in {"experience", "projects"}:
                quality = 1.0 if words >= 55 else 0.75 if words >= 25 else 0.5
                feedback = (
                    "Strong detail depth with room for measurable impact"
                    if quality == 1.0
                    else "Add quantified outcomes and richer role/project context"
                )
            else:
                quality = 1.0 if words >= 22 else 0.75 if words >= 10 else 0.5
                feedback = (
                    "Education section is well detailed"
                    if quality == 1.0
                    else "Add degree, institution, graduation timeline, and notable achievements"
                )

            section_quality[section] = quality
            section_feedback[section] = feedback
        else:
            missing.append(section)
            section_quality[section] = 0.0
            section_word_counts[section] = 0
            section_feedback[section] = "Section missing - add this section with concise, relevant details"

    presence_score = len(present) / len(expected) * 100
    quality_average = sum(section_quality.values()) / len(section_quality)
    completeness = (presence_score * 0.75) + (quality_average * 100 * 0.25)

    return {
        "present": present,
        "missing": missing,
        "completeness": completeness,
        "quality_scores": section_quality,
        "word_counts": section_word_counts,
        "section_feedback": section_feedback,
        "quality_average": quality_average,
    }


def length_score(full_text: str) -> float:
    """Length scoring centered on an optimal one-page to one-and-half-page resume."""
    words = len(full_text.split())
    target_words = 500
    score = 100 - abs(words - target_words) * 0.09

    if words < 180:
        score = min(score, 60)
    elif words > 1350:
        score = min(score, 65)

    return max(50.0, min(100.0, score))


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


def ats_friendliness_score(full_text: str, sections: dict) -> dict:
    """Estimate ATS parseability from format/layout signals that commonly affect screening."""
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    if not lines:
        return {
            "score": 45.0,
            "breakdown": {
                "heading_structure": 0.0,
                "contact_readability": 0.0,
                "bullet_structure": 0.0,
                "table_density": 0.0,
                "line_readability": 0.0,
            },
        }

    heading_structure = len([s for s in ["skills", "education", "experience", "projects"] if sections.get(s)]) / 4 * 100

    has_email = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text))
    has_phone = bool(re.search(r"\+?\d[\d\s().-]{8,}\d", full_text))
    has_link = bool(re.search(r"linkedin|github|https?://", full_text.lower()))
    contact_readability = (has_email * 45) + (has_phone * 35) + (has_link * 20)

    bullet_lines = [line for line in lines if re.match(r"^([\-•*]|\d+[.)])\s+", line)]
    bullet_ratio = len(bullet_lines) / max(1, len(lines))
    if 0.08 <= bullet_ratio <= 0.50:
        bullet_structure = 100.0
    elif bullet_ratio > 0:
        bullet_structure = 70.0
    else:
        bullet_structure = 45.0

    table_like_lines = [line for line in lines if "|" in line or "\t" in line]
    table_ratio = len(table_like_lines) / max(1, len(lines))
    table_density = max(0.0, 100.0 - (table_ratio * 220))

    avg_words_per_line = sum(len(line.split()) for line in lines) / max(1, len(lines))
    if 4 <= avg_words_per_line <= 16:
        line_readability = 100.0
    elif 2 <= avg_words_per_line <= 20:
        line_readability = 80.0
    else:
        line_readability = 60.0

    score = (
        heading_structure * 0.28
        + contact_readability * 0.20
        + bullet_structure * 0.22
        + table_density * 0.15
        + line_readability * 0.15
    )

    return {
        "score": round(min(100.0, max(45.0, score)), 1),
        "breakdown": {
            "heading_structure": round(heading_structure, 1),
            "contact_readability": round(contact_readability, 1),
            "bullet_structure": round(bullet_structure, 1),
            "table_density": round(table_density, 1),
            "line_readability": round(line_readability, 1),
        },
    }


def role_signal_score(parsed: dict, role_key: str) -> dict:
    signals = parsed.get("profile_signals", {})
    rules = ROLE_SIGNAL_RULES.get(role_key, ROLE_SIGNAL_RULES["default"])

    required_all = rules.get("required_all", [])
    required_any = rules.get("required_any", [])
    weighted = rules.get("weighted", [])

    required_present = []
    required_missing = []
    required_any_present = []
    required_any_missing = []
    required_any_groups_met = 0

    for signal_key, min_value in required_all:
        if _signal_present(signals, signal_key, min_value):
            required_present.append(signal_key)
        else:
            required_missing.append(signal_key)

    for group in required_any:
        matched = [signal_key for signal_key, min_value in group if _signal_present(signals, signal_key, min_value)]
        if matched:
            required_any_present.extend(matched)
            required_any_groups_met += 1
        else:
            group_keys = [signal_key for signal_key, _ in group]
            required_any_missing.extend(group_keys)

    mandatory_total = len(required_all) + len(required_any)
    mandatory_met = len(required_present) + required_any_groups_met
    # Keep role evidence as a light supporting signal instead of a strong penalty.
    mandatory_score = 30 + (mandatory_met / max(1, mandatory_total)) * 20

    weighted_total = sum(points for _, points, _ in weighted)
    weighted_earned = 0
    present = set(required_present + required_any_present)

    for signal_key, points, min_value in weighted:
        if _signal_present(signals, signal_key, min_value):
            weighted_earned += points
            present.add(signal_key)

    weighted_score = (weighted_earned / max(1, weighted_total)) * 50
    score = min(100.0, mandatory_score + weighted_score)

    expected = sorted({signal for signal, _ in required_all} | {signal for group in required_any for signal, _ in group} | {signal for signal, _, _ in weighted})
    missing = [signal for signal in expected if signal not in present]

    return {
        "score": score,
        "expected": expected,
        "present": sorted(present),
        "missing": missing,
        "required_present": required_present,
        "required_missing": required_missing,
        "required_any_missing": required_any_missing,
        "raw_signals": signals,
    }


def developer_role_calibration_bonus(role_key: str, keyword_data: dict, section_data: dict, action_score: float, consistency: float) -> float:
    """Apply a small ATS-friendly uplift for clearly strong developer resumes without masking gaps."""
    if role_key not in DEVELOPER_ROLE_KEYS:
        return 0.0

    req_cov = keyword_data.get("required_coverage", 0)
    sec_cov = section_data.get("completeness", 0)
    missing_required = len(keyword_data.get("required_missing", []))
    condition_missing = len(keyword_data.get("condition_missing", []))
    structure_score = (action_score + consistency) / 2

    bonus = 0.0

    # Core fit and structure thresholds.
    if req_cov >= 88 and sec_cov >= 85 and missing_required <= 2:
        bonus += 4.0
    elif req_cov >= 78 and sec_cov >= 75 and missing_required <= 3:
        bonus += 2.5
    elif req_cov >= 68 and sec_cov >= 68 and missing_required <= 4:
        bonus += 1.2

    # Reward polished writing/consistency mildly.
    if structure_score >= 82:
        bonus += 1.2
    elif structure_score >= 72:
        bonus += 0.6

    # Preserve accuracy when conditional role requirements are still missing.
    if condition_missing > 0:
        bonus -= min(1.5, condition_missing * 0.6)

    return round(max(0.0, min(5.2, bonus)), 2)


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
    ats_friendly = ats_friendliness_score(full_text, sections)
    rs = role_signal_score(parsed, role_key)
    calibration_bonus = developer_role_calibration_bonus(role_key, km, sc, av_score, cons_score)

    weights = _get_scoring_weights(role_key)
    score_components = {
        "keyword": weights["keyword"] * km["coverage"],
        "sections": weights["sections"] * sc["completeness"],
        "action_verbs": weights["action_verbs"] * av_score,
        "technical_depth": weights["technical_depth"] * td_score,
        "consistency": weights["consistency"] * cons_score,
        "length": weights["length"] * ls,
        "formatting": weights["formatting"] * fs,
        "role_signals": weights["role_signals"] * rs["score"],
        "ats_friendliness": weights.get("ats_friendliness", 0) * ats_friendly["score"],
    }
    score = sum(score_components.values())
    score += calibration_bonus

    return {
        "ats_score": round(min(100.0, score), 2),
        "keyword_match": km,
        "sections": sc,
        "length_score": round(ls, 1),
        "formatting_score": round(fs, 1),
        "action_verb_score": round(av_score, 1),
        "technical_depth_score": round(td_score, 1),
        "consistency_score": round(cons_score, 1),
        "ats_friendliness_score": ats_friendly["score"],
        "ats_friendliness_breakdown": ats_friendly["breakdown"],
        "role_signal_score": round(rs["score"], 1),
        "role_signal_analysis": rs,
        "calibration_bonus": calibration_bonus,
        "experience_level": exp_level,
        "scoring_weights": weights,
        "score_components": {k: round(v, 2) for k, v in score_components.items()},
    }
