import os
from flask import Flask, redirect, url_for, session, request, render_template, jsonify, flash
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'random_secret_key')
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')

# Initialize OAuth
oauth = OAuth(app)
github = oauth.remote_app(
    'github',
    consumer_key=app.config['GITHUB_CLIENT_ID'],
    consumer_secret=app.config['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args.get('error'),
            request.args.get('error_description')
        ), 'error')
        return redirect(url_for('index'))

    session['github_token'] = (response['access_token'], '')
    user = github.get('user')
    session['user'] = user.data['login']

    return redirect(url_for('index'))

@app.route('/fetch_github_data')
def fetch_github_data():
    if 'github_token' not in session:
        flash('Please log in to fetch GitHub data.', 'warning')
        return redirect(url_for('login'))
    
    try:
        resp = github.get('user/repos')
        resp.raise_for_status()  # Raises an HTTPError for bad responses
    except Exception as e:
        return jsonify({'message': 'Failed to fetch GitHub repositories', 'error': str(e)}), 500
    
    return jsonify(resp.data)

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for better error messages and auto-reload
