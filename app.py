from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Voeg een geheime sleutel toe voor sessies

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    # (hetzelfde als voorheen)

@app.route('/login', methods=['POST'])
def login():
    login_username = request.form['login_username']
    login_password = request.form['login_password']

    # (hetzelfde als voorheen)

    # Controleer of de gebruikersnaam en het wachtwoord overeenkomen
    for user in users:
        if user['username'] == login_username and user['password'] == login_password:
            # Sla de gebruikersnaam op in de sessie
            session['username'] = login_username
            return redirect(url_for('welcome'))

    return 'Invalid login credentials.'

@app.route('/welcome')
def welcome():
    # Controleer of de gebruiker is ingelogd
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        return 'Not logged in.'

# ... (rest van de code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
