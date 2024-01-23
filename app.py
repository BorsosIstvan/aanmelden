from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Voeg een geheime sleutel toe voor sessies

# Dummygebruikers om mee te beginnen (let op: wachtwoorden zijn gehasht)
dummy_users = [
    {'username': 'admin', 'password': '5f4dcc3b5aa765d61d8327deb882cf99'},  # 'password'
    {'username': 'user1', 'password': '81dc9bdb52d04dc20036dbd8313ed055'},  # '1234'
    {'username': 'user2', 'password': '4a8a08f09d37b73795649038408b5f33'}   # 'password123'
]

# Schrijf de dummygebruikers naar het JSON-bestand
with open('users.json', 'w') as file:
    json.dump(dummy_users, file, indent=2)

# Functie voor het hashen van wachtwoorden
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_username = request.form['username']
        login_password = request.form['password']

        # Laad gebruikersgegevens uit JSON-bestand
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        # Controleer of de gebruikersnaam en het gehashte wachtwoord overeenkomen
        for user in users:
            if user['username'] == login_username and user['password'] == hash_password(login_password):
                # Sla de gebruikersnaam op in de sessie
                session['username'] = login_username
                return redirect(url_for('chat'))

        return 'Invalid login credentials.'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
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
        new_user = {'username': username, 'password': hash_password(password)}
        users.append(new_user)

        # Sla de bijgewerkte gebruikersgegevens op naar het JSON-bestand
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=2)

        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/chat')
def chat():
    # Controleer of de gebruiker is ingelogd
    if 'username' in session:
        username = session['username']
        return f'<h1>Welcome to the chat, {username}!</h1>'
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
