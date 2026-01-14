from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscription(db.Model):
    """Modell für eine Subscription/ein Abo"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    cycle = db.Column(db.String(20), nullable=False)  # 'monthly', 'yearly', 'quarterly'
    due_date = db.Column(db.Date, nullable=False)  # Nächstes Fälligkeitsdatum
    login = db.Column(db.String(255))
    password = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Subscription {self.name}>'
