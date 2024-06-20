from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Portfolio model for the database
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Portfolio {self.title}>'

# Create the database and the database table here if it does not exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    projects = Portfolio.query.all()
    return render_template('index.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
