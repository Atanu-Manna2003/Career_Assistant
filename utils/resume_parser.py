# utils/resume_parser.py
import re
import os
import docx
from PyPDF2 import PdfReader
from typing import Dict, List, Optional
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Initialize Groq LLM
LLM = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0.1
)

# Skill extraction prompt
skill_extraction_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=(
        "Analyze the following resume text and extract all technical skills, programming languages, "
        "tools, frameworks, and technologies mentioned. Return only a JSON array of skills without any additional text.\n\n"
        "Resume Text:\n{resume_text}\n\n"
        "Return only a valid JSON array of strings."
    ),
)

skill_chain = LLMChain(llm=LLM, prompt=skill_extraction_prompt)

SEED_SKILLS = [
    "python", "sql", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "nlp", "computer vision", "docker", "kubernetes", "aws", "azure", "gcp",
    "flask", "fastapi", "git", "linux", "tableau", "power bi"
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")

def extract_text_from_file(path: str) -> str:
    """Extract text from various file formats: pdf, txt, docx"""
    ext = os.path.splitext(path)[1].lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext == '.txt':
        return extract_text_from_txt(path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            texts.append("")
    return "\n".join(texts)

def extract_text_from_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def detect_skills_llm(text: str) -> List[str]:
    """Use LangChain with Groq LLM to extract skills from resume text"""
    try:
        # Limit text length to avoid token limits
        truncated_text = text[:4000] if len(text) > 4000 else text
        
        # Use LangChain to extract skills
        result = skill_chain.run({"resume_text": truncated_text})
        
        # Try to parse the result as JSON
        try:
            import json
            # Extract JSON array from the response
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                skills = json.loads(json_match.group(0))
                print("hello")
                return skills if isinstance(skills, list) else []
        except (json.JSONDecodeError, AttributeError):
            # If JSON parsing fails, fall back to traditional method
            pass
        
        return detect_skills_traditional(text)
            
    except Exception as e:
        print(f"Error in LLM skill extraction: {e}")
        # Fall back to the traditional method if LLM fails
        return detect_skills_traditional(text)

def detect_skills_traditional(text: str) -> List[str]:
    """Traditional skill detection method as fallback"""
    text_l = text.lower()
    found = [s for s in SEED_SKILLS if s in text_l]
    return found

def detect_skills(text: str, use_llm: bool = True) -> List[str]:
    """Detect skills using LLM if available, otherwise use traditional method"""
    if use_llm and GROQ_API_KEY:
        return detect_skills_llm(text)
    else:
        return detect_skills_traditional(text)

def parse_resume(path: str, use_llm: bool = True) -> Dict:
    text = extract_text_from_file(path)
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    skills = detect_skills(text, use_llm)

    return {
        "raw_text": text,
        "emails": emails,
        "phones": phones,
        "skills": skills,
    }