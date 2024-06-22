from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy event system
db = SQLAlchemy(app)

# Define your database model
class GitHubRepo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    html_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<GitHubRepo {self.name}>'

# Create tables based on defined models (run once)
db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_github_data')
def fetch_github_data():
    # Example data to simulate fetching from GitHub API
    sample_data = [
        {'name': 'Repo 1', 'description': 'First repository', 'html_url': 'https://github.com/user/repo1'},
        {'name': 'Repo 2', 'description': 'Second repository', 'html_url': 'https://github.com/user/repo2'}
    ]

    # Save sample data to database (replace with actual database insertion)
    for data in sample_data:
        repo = GitHubRepo(name=data['name'], description=data['description'], html_url=data['html_url'])
        db.session.add(repo)
    db.session.commit()

    return 'GitHub data fetched and saved to database successfully!'

@app.route('/get_github_repos')
def get_github_repos():
    # Query all GitHub repositories from database
    repos = GitHubRepo.query.all()

    # Convert to dictionary for JSON response
    repo_list = []
    for repo in repos:
        repo_data = {
            'name': repo.name,
            'description': repo.description,
            'html_url': repo.html_url
        }
        repo_list.append(repo_data)

    return jsonify(repo_list)

if __name__ == '__main__':
    app.run(debug=True)
