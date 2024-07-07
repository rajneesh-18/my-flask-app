# app/models.py

# Importing SQLAlchemy from Flask
from flask_sqlalchemy import SQLAlchemy

# Initializing the SQLAlchemy instance
db = SQLAlchemy()


# Defining the Portfolio modelline
class Portfolio(db.Model):
    # Unique identifier for each portfolio item
    id = db.Column(db.Integer, primary_key=True)
    
    # Title of the portfolio item
    title = db.Column(db.String(100), nullable=False)
    
    # Description of the portfolio item
    description = db.Column(db.String(200), nullable=False)
    
    # URL to an image representing the portfolio item
    image_url = db.Column(db.String(200), nullable=False)
