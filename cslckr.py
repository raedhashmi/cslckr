import os
import requests
from flask import Flask, send_file, request, redirect, url_for
 
app = Flask(__name__)
messages = []

@app.route('/', methods=['GET', 'POST'])
def home():
    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'create_shortcut', 'data': {'none': 'none'}})
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
    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'shutdown', 'data': {'none': 'none'}})
    return send_file('templates/failure.html')

@app.route('/resources/<path>')
def resources(path):
    return send_file(os.path.join('templates', path))

@app.route('/messages', methods=['POST', 'GET'])
def handle_messages():
    if request.method == 'POST':
        message = request.get_json()
        messages.append(message)
        return {'status': 'success'}
    else:
        return messages
        messages.clear()

if __name__ == "__main__":
    app.run(host='localhost', port=8004, debug=True)