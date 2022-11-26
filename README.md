# Botnet
## Description

Basic botnet, combining http and socket server, for mantaining access to target devices

Completely written in python3, made just for learning purposes, I'm not responsible for any misuse that may be made of it

## Features

- Check current connected bots
- Execute system commands in all bots
- Host files in a webserver and download them in bots
- Send basic ddos attacks, (UDP and SYN floods)
- In a real use case, bots connect via dns so if your cnc server is taken down, bots won't be lost

## Installation

[Command and control (CNC)](https://en.wikipedia.org/wiki/Command_and_control) server made for linux, but should be working also on windows machines
Bot script tested and working for both operating systems

Install the python requirements

```
pip install -r requirements.txt
```

Run setup file and select Web and Socket addresses and ports

Default addresses are 0.0.0.0 (all), I recommend using this

Default ports are 80 for Web server and 30120 for Socket server (In a real use case we'll need to open this ports)

Anyways run this file to make sure all the configurations is complete

```
python3 setup.py
```

Set up domain, in this case we'll ve using a virtual host, but in real use cases, we'll be using a common DNS

We modify /etc/hosts file to point our vhost

(botnet.test will be our domain, modify it if you want)
```
sudo su
echo '127.0.0.1 botnet.test' >> /etc/hosts
```
If you have modified the botnet.test domain, open bot/bot.py and modify it in line 8
```
nano bot/bot.py
(change line 8 to your domain in case you have changed it)
```

## Usage

After all of this, our Botnet is ready to work

Run CNC server with:
```
cd server
python3 cnc.py
```
Use the following commands to control bots:
| COMMAND | EXPLANATION |
| ------ | ------ |
| help | List all commands with description |
| active | Get current number of connected bots |
| exec | Execute os command in all bots  |
| download | Download file in all bots |
| ddos | Send ddos attack with all bots |

All files in server/public/ will be exposed at http://botnet.test/download/yourfile.exe

Use this for hosting files and downloading them into bots with download command

Now run bot/bot.py, and it's done!

In real use cases bot/bot.py must be compiled and should have an autostart option, so you won't loose that bot once target computer is restarted, and obviously should be run in the background to prevent our victim from detecting our intrussion

## About me

This is just a simple project, no porpouse with it, just learning

If you have any dudes or suggestions contact me at Telegram: @geas0

BTC address for donations:
18osyF2EpYArL58tXgwPp3cjWJz64u5fhv
