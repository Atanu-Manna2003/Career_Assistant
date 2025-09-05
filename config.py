# config.py
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


class Config:
   SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
   SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///career_assistant.db")
   SQLALCHEMY_TRACK_MODIFICATIONS = False


   GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
   RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


   BASE_DIR = Path(__file__).parent
   UPLOAD_FOLDER = BASE_DIR / "uploads"


   @staticmethod
   def ensure_dirs():
     os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)