# app/auth.py
from flask import Blueprint, redirect, url_for, session, flash, request
from flask_oauthlib.client import OAuth

auth = Blueprint('auth', __name__)
oauth = OAuth()
github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@auth.route('/login')
def login():
    return github.authorize(callback=url_for('auth.authorized', _external=True))

@auth.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@auth.route('/login/authorized')
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

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')
