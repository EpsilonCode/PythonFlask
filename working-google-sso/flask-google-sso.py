from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import secrets

# Create an instance of the Flask class
app = Flask(__name__)

# Generate a random secret key and set it for the app
app.secret_key = secrets.token_hex(16) # fine for testing, but change to static for production

# OAuth 2 client setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id='UPDATE',
    client_secret='UPDATE',
    client_kwargs={'scope': 'openid email profile'}
)
# Route for home page
@app.route('/')
def homepage():
    user = session.get('user')
    if user:
        return f'Hello, {user["email"]}!'
    return 'Welcome! Please <a href="/login">login</a>.'

# Route for login
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# Route for login callback
@app.route('/login/callback')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    user = resp.json()
    session['user'] = user
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
