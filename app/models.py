from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    jobs = db.relationship('Job', secondary="jobs_by_users", back_populates='users')

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ended_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(db.String(255), nullable=False)
    input = db.Column(LONGTEXT, nullable=True)
    output = db.Column(LONGTEXT, nullable=True)
    users = db.relationship('User', secondary="jobs_by_users", back_populates='jobs')

class JobByUser(db.Model):
    __tablename__ = 'jobs_by_users'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
