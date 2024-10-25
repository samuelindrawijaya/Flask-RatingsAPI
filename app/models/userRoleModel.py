from datetime import datetime

from flask_login import UserMixin
from app.config.connector import db  # Import db from extensions.py
from werkzeug.security import generate_password_hash, check_password_hash

# Define the association table between users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),  # Correct 'users.id' to match __tablename__
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)   # Correct 'roles.id' to match __tablename__
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'roles': [role.to_dict() for role in self.roles]  # Serializing roles
        }
    

class Role(db.Model):
    __tablename__ = 'roles'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
