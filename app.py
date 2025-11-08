import os
import shutil
import subprocess
import win32com.client
from flask import Flask, render_template, request, redirect, url_for
 
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
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == "__main__":
    app.run(debug=True)