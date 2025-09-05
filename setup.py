import os

# Define your folder structure
folders = [
    "migrations",
    "uploads",
    "templates",
    "utils"
]

files = {
    "app.py": "",
    "config.py": "",
    "requirements.txt": "",
    ".env": "",
    os.path.join("templates", "base.html"): "",
    os.path.join("templates", "index.html"): "",
    os.path.join("templates", "register.html"): "",
    os.path.join("templates", "login.html"): "",
    os.path.join("templates", "results.html"): "",
    os.path.join("utils", "groq_llm.py"): "",
    os.path.join("utils", "langchain_chains.py"): "",
    os.path.join("utils", "resume_parser.py"): "",
    os.path.join("utils", "semantic_matcher.py"): "",
    os.path.join("utils", "ats.py"): "",
    os.path.join("utils", "job_scraper.py"): "",
    os.path.join("utils", "models.py"): ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Created folder: {folder}")

# Create files
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Created file: {filepath}")

print("\n🎉 Project structure is ready inside 'career_assistant'")
