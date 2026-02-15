from config import ROLE_CONFIG


def get_ai_feedback(role_label: str, parsed: dict, ats_details: dict) -> dict:
    # Find role config
    role_config = next((v for v in ROLE_CONFIG.values() if v["label"] == role_label), None)

    if not role_config:
        return {
            "strong_areas": ["Role not configured"],
            "weak_points": [],
            "improvement_suggestions": [],
            "template_feedback": []
        }

    missing_skills = ats_details["keyword_match"]["required_missing"]
    missing_sections = ats_details["sections"]["missing"]
    score = ats_details["ats_score"]

    # Role-specific advice
    role_key = next(k for k, v in ROLE_CONFIG.items() if v["label"] == role_label)

    advice = {
        "cpp_developer": {
            "strong": ["C++ knowledge detected"],
            "weak": ["Missing STL expertise"] + missing_skills,
            "suggestions": ["Practice STL containers", "Solve LeetCode C++", "Learn multithreading"],
            "template": ["Add code samples"]
        },
        "java_developer": {
            "strong": ["Java foundation solid"],
            "weak": ["Missing Spring Boot"] + missing_skills,
            "suggestions": ["Learn Spring Boot 3", "Microservices project", "Maven/Gradle"],
            "template": ["Enterprise format good"]
        },
        # Add more or use generic
    }.get(role_key, {
        "strong": [f"Solid ATS score: {score}%"],
        "weak": missing_skills + [f"Missing: {', '.join(missing_sections)}"],
        "suggestions": [
            f"Add: {', '.join(missing_skills[:3])}",
            f"Complete: {', '.join(missing_sections)}",
            "Use action verbs"
        ],
        "template": ["Arial 10-12pt", "Skills at top", "No tables"]
    })

    return {
        "strong_areas": advice["strong"],
        "weak_points": advice["weak"],
        "improvement_suggestions": advice["suggestions"],
        "template_feedback": advice["template"]
    }


