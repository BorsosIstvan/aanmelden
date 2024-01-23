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

# Dummylijst met online gebruikers
online_users = []

# Dummylijst met chatberichten
chat_messages = []

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
                # Voeg gebruiker toe aan de lijst met online gebruikers
                online_users.append(login_username)
                # Sla de gebruikersnaam op in de sessie
                session['username'] = login_username
                return redirect(url_for('chat'))

        return 'Invalid login credentials.'

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Controleer of de gebruiker is ingelogd
    if 'username' in session:
        username = session['username']
        # Verwijder de gebruiker uit de lijst met online gebruikers
        online_users.remove(username)
        # Wis de sessie
        session.clear()
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    # Controleer of de gebruiker is ingelogd
    if 'username' in session:
        username = session['username']
        return render_template('chat.html', username=username, users=online_users)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
