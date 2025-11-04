# Career Assistant AI 🤖

An intelligent, AI-powered career assistance platform that helps job seekers optimize their job search through resume analysis, smart job matching, and personalized career guidance.

## 🚀 What This Project Does

Career Assistant AI is a full-stack web application that leverages cutting-edge AI technologies to transform your job search experience:

### ✨ Key Features

- **📊 Resume Analysis & Parsing** - Automatically extracts skills, contact information, and experience from resumes (PDF, DOCX, TXT)
- **🎯 Smart Job Matching** - Uses semantic search with Sentence Transformers to find the most relevant jobs based on your profile
- **🤖 AI Career Chatbot** - Get personalized career advice, interview tips, and resume suggestions based on your resume
- **📝 ATS-Optimized Documents** - Generate professionally tailored resumes and cover letters for specific job descriptions
- **💼 Real-time Job Search** - Fetches live job listings from multiple sources using JSearch API
- **🔐 User Management** - Save favorite jobs and track your applications with user accounts

## 🛠️ Tech Stack

- **Backend**: Python, Flask, LangChain, Groq LLM
- **Frontend**: HTML, CSS, JavaScript, Jinja2 Templates
- **AI/ML**: Sentence Transformers, Semantic Similarity, NLP
- **Database**: SQLAlchemy, PostgreSQL/SQLite
- **APIs**: Groq API, JSearch RapidAPI
- **File Processing**: PyPDF2, python-docx, ReportLab

## 📋 Prerequisites

- Python 3.8+
- Groq API account ([Get API key](https://console.groq.com/))
- RapidAPI account ([JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch))

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Atanu-Manna2003/Career_Assistant.git
cd Career-Assistant

python -m venv venv
venv/bin/activate 
pip install -r requirements.txt

# Configure Environment Variables
Create a .env file in the root directory:
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=jsearch.p.rapidapi.com
SECRET_KEY=your_flask_secret_key
DATABASE_URL=sqlite:///career_assistant.db

6. Run the Application
python app.py

Visit http://localhost:5000 in your browser!

🎯 How to Use
1. Upload Your Resume
Go to the homepage and upload your resume (PDF, DOCX, or TXT)

The system automatically parses and extracts your skills and experience

2. Search for Jobs
Enter your desired job title and location

Get AI-ranked job matches based on semantic similarity to your resume

3. Get Career Advice
Chat with the AI career assistant for personalized guidance

Get interview tips and resume improvement suggestions

4. Generate Tailored Documents
Select a job posting to generate an ATS-optimized resume

Create customized cover letters for specific positions

5. Save & Track
Create an account to save favorite jobs

Track your application progress