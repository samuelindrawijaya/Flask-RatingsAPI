
from app.config.connector import db  # Import db from extensions.py
from datetime import datetime
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Correct ForeignKey reference
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    
    def __repr__(self):
        return f'<Review {self.content[:20]}>'
    
    def to_dict(self):
        """
        Convert the Review object to a dictionary for easy JSON serialization.
        """
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'user': {
                'id': self.user.id,
                'username': self.user.username
            },
            'created_at': self.created_at.isoformat()
        }