import hashlib

from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Verander dit naar een geheime sleutel

# Functie om gebruikers uit het JSON-bestand te lezen
def read_users():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    return users

# Functie om gebruikers naar het JSON-bestand te schrijven
def write_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=2)

# Indexpagina
@app.route('/')
def index():
    username = session.get('username')

    return render_template('index.html', username=username)

# Aanmeldpagina
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Verkrijg gebruikersgegevens van het formulier
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # Hash het wachtwoord voordat het wordt opgeslagen
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()


        # Voeg nieuwe gebruiker toe aan gebruikerslijst
        users = read_users()
        users.append({
            'name': name,
            'surname': surname,
            'email': email,
            'username': username,
            'password': hashed_password  # Let op: wachtwoorden moeten worden gehasht voordat ze worden opgeslagen in een echt project
        })
        write_users(users)

        return redirect(url_for('index'))

    return render_template('signup.html')

# Inlogpagina
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verkrijg gebruikersgegevens van het formulier
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Controleer of gebruiker bestaat in de gebruikerslijst
        users = read_users()
        for user in users:
            if user['username'] == username and user['password'] == hashed_password:
                session['username'] = username
                return redirect(url_for('index'))

    return render_template('login.html')

# Uitlogpagina
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#if __name__ == '__main__':
#    app.run(debug=True)
if __name__ == '__main__':
    app.run( host='0.0.0.0', port=8000)