from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "POST"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post ({self.id})>"
    
    def __eq__(self, other):
        if not isinstance(other, Post):
            return False
        return self.id == other.id