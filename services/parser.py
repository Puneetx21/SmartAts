import fitz  # PyMuPDF
import re
import os
from docx import Document

SECTION_HEADER_ALIASES = {
    "summary": "summary",
    "professional summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "core skills": "skills",
    "technologies": "skills",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "projects": "projects",
    "project experience": "projects",
    "education": "education",
    "academic background": "education",
    "certifications": "certifications",
    "certificates": "certifications",
}


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\u2013\u2014\u2212]", "-", text)
    text = re.sub(r"[\u2022\u25CF\u25E6\u00B7]", "•", text)

    normalized_lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if cleaned:
            normalized_lines.append(cleaned)

    return "\n".join(normalized_lines)

def extract_text_from_pdf(filepath: str) -> str:
    doc = fitz.open(filepath)
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    return "\n".join(parts)


def extract_text_from_docx(filepath: str) -> str:
    doc = Document(filepath)
    paragraphs = []

    for p in doc.paragraphs:
        if not p.text or not p.text.strip():
            continue
        line = p.text.strip()
        style_name = (p.style.name or "").lower() if p.style else ""
        if "list" in style_name and not re.match(r"^[-•*]", line):
            line = f"• {line}"
        paragraphs.append(line)

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text and cell.text.strip()]
            if cells:
                paragraphs.append(" | ".join(cells))

    return "\n".join(paragraphs)


def _normalize_header_candidate(line: str) -> str:
    line = line.strip().lower()
    line = re.sub(r"[:\-]+$", "", line).strip()
    line = re.sub(r"\s+", " ", line)
    return line


def _detect_section_header(line: str) -> str:
    candidate = _normalize_header_candidate(line)
    return SECTION_HEADER_ALIASES.get(candidate, "")

def split_sections(text: str) -> dict:
    lines = text.splitlines()
    sections = {}
    current = "other"
    sections[current] = []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        detected_header = _detect_section_header(clean)
        if detected_header:
            current = detected_header
            sections.setdefault(current, [])
            continue

        sections.setdefault(current, []).append(clean)

    final_sections = {}
    for key, value in sections.items():
        final_sections[key] = "\n".join(value).strip()

    return final_sections


def extract_name(text: str) -> str:
    for line in text.splitlines():
        clean = line.strip()
        if not clean:
            continue

        if re.search(r"@|https?://|linkedin|github|portfolio", clean.lower()):
            continue

        if re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", clean):
            continue

        if _detect_section_header(clean):
            continue

        if 2 <= len(clean.split()) <= 6:
            return clean
    return ""


def extract_skills(skills_text: str) -> list:
    if not skills_text:
        return []

    raw = re.split(r"[,•;|/\n]+", skills_text)
    cleaned = set()

    for token in raw:
        skill = token.strip().lower()
        skill = re.sub(r"\s+", " ", skill)
        skill = re.sub(r"^[\-:]+|[\-:]+$", "", skill).strip()
        if len(skill) < 2:
            continue
        cleaned.add(skill)

    return sorted(cleaned)

def parse_resume(filepath: str) -> dict:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(filepath)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

    full_text = normalize_text(raw_text)

    sections = split_sections(full_text)

    name = extract_name(full_text)
    skills_text = sections.get("skills", "")
    skills = extract_skills(skills_text)

    return {
        "name": name,
        "full_text": full_text,
        "sections": sections,
        "skills": skills,
    }
