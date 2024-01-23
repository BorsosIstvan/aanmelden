from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Voeg een geheime sleutel toe voor sessies

# Dummygebruikers om mee te beginnen
dummy_users = [
    {'username': 'admin', 'password': 'admin123'},
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

# Schrijf de dummygebruikers naar het JSON-bestand
with open('users.json', 'w') as file:
    json.dump(dummy_users, file, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    # Laad bestaande gebruikersgegevens uit JSON-bestand
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Controleer of de gebruikersnaam al in gebruik is
    for user in users:
        if user['username'] == username:
            return 'Username already taken!'

    # Voeg de nieuwe gebruiker toe aan de lijst
    new_user = {'username': username, 'password': password}
    users.append(new_user)

    # Sla de bijgewerkte gebruikersgegevens op naar het JSON-bestand
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=2)

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    login_username = request.form['login_username']
    login_password = request.form['login_password']

    # Laad gebruikersgegevens uit JSON-bestand
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
