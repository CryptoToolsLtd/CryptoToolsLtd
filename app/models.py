from flask_login import UserMixin # type: ignore
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    jobs = db.relationship('Job', secondary="jobs_by_users", back_populates='users', lazy='dynamic')

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ended_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(db.String(255), nullable=False)
    input = db.Column(LONGTEXT, nullable=True)
    output = db.Column(LONGTEXT, nullable=True)
    users = db.relationship('User', secondary="jobs_by_users", back_populates='jobs', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'started_at': self.started_at.timestamp(),
            'ended_at': self.ended_at.timestamp(),
            'status': self.status,
            'input': self.input,
            'output': self.output,
        }

class JobByUser(db.Model):
    __tablename__ = 'jobs_by_users'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
