from flask import Flask, render_template, request, redirect, url_for, flash, session,Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from utils.chatbot import ask_chatbot
from utils.resume_parser import parse_resume
from utils.semantic_matcher import semantic_similarity

from utils.job_scraper import fetch_jobs
from utils.langchain_chains import generate_resume_improvement, generate_cover_letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from io import BytesIO
import subprocess
import tempfile
import os
import shutil
from utils.models import User, SavedJob,db  # Import after db initialization
app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)



# ------------------- AUTH ROUTES -------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            # flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


# ------------------- MAIN ROUTES -------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_title = request.form["job_title"]
        location = request.form["location"]
        resume_file = request.files["resume"]

        if resume_file:
            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)

            resume_text = parse_resume(resume_path)
            jobs = fetch_jobs(job_title, location)
            
            matched_jobs = semantic_similarity(resume_text, jobs)
            print(type(matched_jobs))
            
            session["jobs"] =  matched_jobs
            # print(session["jobs"])
            return render_template(
                "results.html",
                jobs=matched_jobs,
                
                resume_text=resume_text,
            )

    return render_template("index.html")


@app.route("/save_job/<job_id>", methods=["POST"])
def save_job(job_id):
    if "user_id" not in session:
        flash("Login required to save jobs", "warning")
        return redirect(url_for("login"))

    saved_job = SavedJob(
        user_id=session["user_id"],
        job_title=request.form["job_title"],
        company=request.form["company"],
        job_url=request.form["job_url"],
        match_score=None
    )
    db.session.add(saved_job)
    db.session.commit()

    flash("Job saved successfully", "success")
    return redirect(url_for("index"))



@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    resume_text = request.form["resume_text"]
    job_desc = request.form["job_desc"]

    improved_resume = generate_resume_improvement(resume_text, job_desc)
    # Store in session for download
    session["improved_resume"] = improved_resume
    session["job_title"] = job_desc.split(" at ")[0] if " at " in job_desc else "Improved_Resume"
    return render_template("generated_content.html", 
                         content=improved_resume, 
                         title="Improved Resume",
                         type="resume")


@app.route("/generate_cover_letter", methods=["POST"])
def generate_cover_letter_route():
    resume_text = request.form["resume_text"]
    job_desc = request.form["job_desc"]

    cover_letter = generate_cover_letter(resume_text, job_desc)
     # Store in session for download
    session["cover_letter"] = cover_letter
    session["job_title"] = job_desc.split(" at ")[0] if " at " in job_desc else "Cover_Letter"
    return render_template("generated_content.html", 
                         content=cover_letter, 
                         title="Cover Letter",
                         type="cover_letter")
def create_pdf(content, title="Generated Document", max_pages=2):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=50, bottomMargin=50, leftMargin=50, rightMargin=50)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        alignment=1,  # Center
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='CustomContent',
        fontName="Helvetica",
        fontSize=10,
        leading=14
    ))

    elements = []
    elements.append(Paragraph(title, styles['CustomTitle']))

    # Split content into paragraphs
    paragraphs = [p.strip() for p in content.split("\n") if p.strip()]

    # Approximate max number of paragraphs per page (depends on font & page size)
    max_paragraphs_per_page = 45  # adjust if needed

    for i, para in enumerate(paragraphs):
        elements.append(Paragraph(para, styles['CustomContent']))
        # Only add spacer if not last paragraph
        if i != len(paragraphs) - 1:
            elements.append(Spacer(1, 6))

        # Add page break if exceeding max paragraphs per page and still within max_pages
        if (i + 1) % max_paragraphs_per_page == 0 and len(elements) // max_paragraphs_per_page < max_pages:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer
@app.route("/download/<document_type>")
def download_document(document_type):
    if document_type == "resume" and "improved_resume" in session:
        content = session["improved_resume"]
        filename = f"{session.get('job_title', 'Improved_Resume')}.pdf"
        title = "IMPROVED RESUME"
    elif document_type == "cover_letter" and "cover_letter" in session:
        content = session["cover_letter"]
        filename = f"{session.get('job_title', 'Cover_Letter')}.pdf"
        title = "COVER LETTER"
    else:
        flash("Document not found", "danger")
        return redirect(url_for("index"))
    
    # Create PDF
    pdf_buffer = create_pdf(content, title)
    
    return Response(
        pdf_buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    # Prefer improved resume if available, else fallback to original
    resume_text = session.get("improved_resume", session.get("resume_text", ""))
    
    if not resume_text:
        flash("Please upload and parse a resume first.", "warning")
        return redirect(url_for("index"))

    # Initialize chat history in session if not exists
    if "chat_history" not in session:
        session["chat_history"] = []

    response = None
    if request.method == "POST":
        user_query = request.form["user_query"]
        
        # Add user query to chat history
        session["chat_history"].append({"type": "user", "content": user_query})
        
        try:
            response = ask_chatbot(resume_text, user_query)
            # Add bot response to chat history
            session["chat_history"].append({"type": "bot", "content": response})
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            session["chat_history"].append({"type": "bot", "content": error_msg})
            response = error_msg
        
        # Save the updated session
        session.modified = True

    return render_template("chatbot.html", 
                         response=response, 
                         chat_history=session.get("chat_history", []))
if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
    with app.app_context():
        db.create_all()

    # ✅ Render needs this
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
