from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'random_secret_key'
app.config['GITHUB_CLIENT_ID'] = 'your_github_client_id'
app.config['GITHUB_CLIENT_SECRET'] = 'your_github_client_secret'

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
    session.pop('github_token')
    session.pop('user')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error'],
            request.args['error_description']
        )

    session['github_token'] = (response['access_token'], '')
    user = github.get('user')
    session['user'] = user.data['login']

    return redirect(url_for('index'))

@app.route('/fetch_github_data')
def fetch_github_data():
    if 'github_token' not in session:
        return redirect(url_for('login'))
    
    resp = github.get('user/repos')
    if resp.status != 200:
        return jsonify({'message': 'Failed to fetch GitHub repositories'}), resp.status
    
    return jsonify(resp.data)

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == '__main__':
    app.run()
