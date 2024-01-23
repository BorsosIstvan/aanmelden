from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    # Load existing user data from JSON file
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Check if the username is already taken
    for user in users:
        if user['username'] == username:
            return 'Username already taken!'

    # Add the new user to the list
    new_user = {'username': username, 'password': password}
    users.append(new_user)

    # Save the updated user data to the JSON file
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=2)

    return redirect(url_for('home'))

# ... (rest of the code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
