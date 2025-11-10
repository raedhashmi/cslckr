import os
import sys
import shutil
import subprocess
from flask import Flask, send_file, request, redirect, url_for
 
app = Flask(__name__)
messages = []


def shutdown():
    subprocess.call(['shutdown', '/s', '/t', '0'])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'nexus':
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failure'))
    return send_file('templates/index.html')

@app.route('/success')
def success():
    return send_file('templates/success.html')

@app.route('/failure')
def failure():
    shutdown()
    return send_file('templates/failure.html')

@app.route('/resources/<path>')
def resources(path):
    return send_file(os.path.join('templates', path))

@app.route('/messages', methods=['POST', 'GET'])
def handle_messages():
    if request.method == 'POST':
        message = request.get_json().get('message')
        messages.append(message)
        return {'status': 'success'}
    else:
        return {'messages': messages}

if __name__ == "__main__":
    app.run(host='localhost', port=8004, debug=True)