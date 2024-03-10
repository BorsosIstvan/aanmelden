import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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

# Functies voor het lezen en schrijven van berichten
def read_messages():
    try:
        with open('messages.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []
    return messages

def write_messages(messages):
    with open('messages.json', 'w') as file:
        json.dump(messages, file)

def get_messages_for_user(sender, recipient):
    messages = read_messages()
    return [message for message in messages if (message['sender'] == sender and message['recipient'] == recipient) or (message['recipient'] == sender and message['sender'] == recipient)]

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
            'password': hashed_password
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

# Gebruikerspagina
@app.route('/users')
def users():
    users_list = read_users()
    return render_template('users.html', users=users_list)

# Chatpagina
@app.route('/chat/<recipient>', methods=['GET', 'POST'])
def chat(recipient):
    if request.method == 'POST':
        sender = session['username']
        text = request.form['message']
        status = 'sent'  # Het bericht wordt verzonden

        # Voeg het bericht toe aan messages.json
        messages = read_messages()
        messages.append({
            'sender': sender,
            'recipient': recipient,
            'text': text,
            'status': status
        })
        write_messages(messages)

    messages = get_messages_for_user(session['username'], recipient)
    return render_template('chat.html', recipient=recipient, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

