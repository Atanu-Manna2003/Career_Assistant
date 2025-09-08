import os
from typing import List, Dict
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
    temperature=0.6
)

# Update your chatbot prompt for better responses
# Update your chatbot prompt for better responses
chatbot_prompt = PromptTemplate(
    input_variables=["resume_text", "user_query"],
    template=(
        """You are a career assistant chatbot designed to help job seekers.  
You are given:
- Candidate's Resume: {resume_text}

Your role is to provide helpful, professional advice about:
1. How the candidate's resume matches with the job opportunities
2. Skills they should highlight based on the job requirements
3. Career advice tailored to their profile
4. Interview preparation tips
5. Resume improvement suggestions

Always be specific and reference both the resume and job postings when possible.
Provide structured, concise, and practical advice.

If the user is just greeting (hi/hello or simple message that is not related to resume), respond concisely with a friendly greeting.
Otherwise, provide full professional advice.

User Question: {user_query}

Answer in a helpful, professional tone:"""
    ),
)

# Create the chain
chatbot_chain = LLMChain(llm=LLM, prompt=chatbot_prompt)

# Wrapper
def ask_chatbot(resume_text: str, user_query: str) -> str:
    """
    Ask chatbot a question based on resume .
   
    """
    # Format jobs as text
    # jobs_text = "\n".join(
    #     [f"{i+1}. {job.get('title')} at {job.get('company')}\n{job.get('description')}"
    #      for i, job in enumerate(jobs)]
    # )

    return chatbot_chain.run({
        "resume_text": resume_text[:4000],  # safety limit
        # "jobs": jobs_text[:6000],
        "user_query": user_query
    })

