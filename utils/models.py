from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)
  saved_jobs = db.relationship('SavedJob', backref='user', lazy=True)


  def set_password(self, password: str):
    self.password_hash = generate_password_hash(password)


  def check_password(self, password: str) -> bool:
     return check_password_hash(self.password_hash, password)


class SavedJob(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  job_title = db.Column(db.String(255))
  company = db.Column(db.String(255))
  job_url = db.Column(db.String(512))
  match_score = db.Column(db.Float)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

