import fitz  # PyMuPDF[web:29]
import re

SECTION_HEADERS = [
    "summary", "profile",
    "skills", "technical skills",
    "experience", "work experience",
    "projects",
    "education",
    "certifications",
]

def extract_text_from_pdf(filepath: str) -> str:
    doc = fitz.open(filepath)
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    return "\n".join(parts)

def split_sections(text: str) -> dict:
    lines = text.splitlines()
    sections = {}
    current = "other"
    sections[current] = []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        low = clean.lower()
        matched = False
        for header in SECTION_HEADERS:
            pattern = rf"^{header}\b"
            if re.match(pattern, low):
                current = header
                sections.setdefault(current, [])
                matched = True
                break
        if matched:
            continue
        sections.setdefault(current, []).append(clean)

    return {k: "\n".join(v).strip() for k, v in sections.items()}

def extract_name(text: str) -> str:
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            return clean
    return ""

def extract_skills(skills_text: str) -> list:
    if not skills_text:
        return []
    raw = re.split(r"[,•;|/-]", skills_text)
    return sorted({s.strip().lower() for s in raw if s.strip()})

def parse_resume(filepath: str) -> dict:
    full_text = extract_text_from_pdf(filepath)
    sections = split_sections(full_text)

    name = extract_name(full_text)
    skills_text = (
        sections.get("skills") or
        sections.get("technical skills") or
        ""
    )
    skills = extract_skills(skills_text)

    return {
        "name": name,
        "full_text": full_text,
        "sections": sections,
        "skills": skills,
    }
