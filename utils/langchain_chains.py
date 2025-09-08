# utils/langchain_chains.py
import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# ----------------------------
# PROMPTS (lightweight)
# ----------------------------

resume_prompt = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template=(
       """You are an expert resume writer and ATS optimizer.  
Your task is to create a complete professional resume from the provided candidate details and job description.  
The output must strictly follow the structured format below.

Output Format Rules:
- Return the resume in plain text only.
- Use clear section headers in ALL CAPS (e.g., SUMMARY, SKILLS, EXPERIENCE).
- Each job experience must have: Job Title, Company, Location, Dates, and 3–5 bullet points with measurable achievements.
- Skills should be grouped into categories (e.g., Programming, Tools, Soft Skills).
- Education must include Degree, Institution, and Year.
- Do not include explanations, commentary, or extra text outside the resume.

================== RESUME TEMPLATE ==================
NAME: [Candidate Full Name]  
CONTACT: [Email] | [Phone] | [LinkedIn] | [GitHub]

SUMMARY  
[3-4 sentences highlighting experience, key skills, and career goals.]

SKILLS  
- Programming: [List]  
- Tools/Frameworks: [List]  
- Soft Skills: [List]

EXPERIENCE  
Job Title — Company | Location | Start Date – End Date  
- Achievement 1 (quantifiable result, ATS keywords)  
- Achievement 2  
- Achievement 3  

Job Title — Company | Location | Start Date – End Date  
- Achievement 1  
- Achievement 2  
- Achievement 3  

EDUCATION  
Degree — Institution | Year  

PROJECTS  
Project Name  
- 1-2 bullet points describing impact, technologies used, and results.

CERTIFICATIONS  
[List relevant certifications from the resume, if any]

ACHIEVEMENTS  
[List major achievements from the resume, if any]
=====================================================

Candidate Resume:  
{resume_text}

Job Description:  
{job_description}"""
    ),
)

cover_prompt = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template=(
        "You are a professional cover letter writer.\n"
        "Write a one-page, ATS-friendly, tailored cover letter for the candidate using the resume and job description below.\n"
        "Tone: professional, confident, concise. Include a short opening, 2-3 paragraphs demonstrating fit, and a closing. Do not add extra headings.\n\n"
        "Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\n"
        "Return only the cover letter text."
    ),
)

# ----------------------------
# Lazy loader for Groq
# ----------------------------
def get_llm():
    """Initialize Groq LLM only when needed."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.7
    )

# ----------------------------
# Wrappers
# ----------------------------
def generate_resume_improvement(resume_text: str, job_description: str) -> str:
    llm = get_llm()
    resume_chain = LLMChain(llm=llm, prompt=resume_prompt)
    return resume_chain.run({"resume_text": resume_text, "job_description": job_description})

def generate_cover_letter(resume_text: str, job_description: str) -> str:
    llm = get_llm()
    cover_chain = LLMChain(llm=llm, prompt=cover_prompt)
    return cover_chain.run({"resume_text": resume_text, "job_description": job_description})
