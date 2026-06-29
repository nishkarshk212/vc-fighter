# vc-fighter
A versatile command and control center (CCC) for DDoS Botnet Attack Simulation &amp; Load Generation.

**Disclaimer**
---

_The use of this software and scripts downloaded on this repository is done at your own discretion and risk and with agreement that you will be solely responsible for any damage to your or other computer system or availability disruption that results from such activities. You are solely responsible for the usage in connection with any of the software, and the author will not be liable for any damages that you may suffer or incur availability disruption on other systems in connection with using, modifying or distributing any of this software. No advice or information, whether oral or written, obtained by you from the author or from this website shall create any warranty for the software._

What is _NetBot_?
--
- Proof-of-Concept code that simulates a Client-Server botnet environment.
- Easily helps setting up a botnet chain that reports to your CCC.
- Assists in simulating DDoS attacks towards the target. (_Experimental/Research Usage Only_)
- **NEW**: Now supports Telegram-based control for remote command and control!

Requirements
--
- Python 3
- python-telegram-bot (for Telegram version)

Supports
--
- Tested on Debian, Ubuntu, CentOS and MacOS High Sierra.

FYI - *Prototype Warning*
--
- This is simply a prototype code and may not fully work up to your expectations. Feel free to fork the project and modify it to meet your needs. 
- Currently working on making it more robust execution, look and feel features.
- (_under development_) more attack vectors and variants. (_as of now supports HTTP Flooding & Ping Flood only._)


Source Code
--
- _netbot_server.py_ : This is the actual CCC Server (TCP-based).
- _netbot_config.py_ : CCC loads the information about the targets to attack. 
- _netbot_client.py_ : This is the client code (bots) (TCP-based).
- _netbot_telegram_server.py_ : Telegram-based CCC Server.
- _netbot_telegram_client.py_ : Telegram-based client code (bots).
- _telegram_config.py_ : Telegram bot configuration.

How do I setup/test _NetBot_ (Telegram Version)?
--
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a Telegram Bot**:
   - Open Telegram and search for @BotFather
   - Send `/newbot` and follow the instructions
   - Copy the bot token provided

3. **Get Your Telegram User ID**:
   - Search for @userinfobot on Telegram
   - Send any message to get your user ID

4. **Configure the Bot**:
   - Edit `telegram_config.py`
   - Replace `YOUR_BOT_TOKEN_HERE` with your bot token
   - Replace `YOUR_TELEGRAM_USER_ID` with your user ID

5. **Configure Attack Settings**:
   - Edit `netbot_config.py`
   - Set target host, port, attack type, and other parameters

6. **Run the Telegram Server**:
   ```bash
   python3 netbot_telegram_server.py
   ```

7. **Control via Telegram**:
   - Open your Telegram bot
   - Use commands like `/start`, `/launch`, `/halt`, `/status`, etc.

Available Telegram Commands:
- `/start` - Show welcome message and available commands
- `/status` - Show bot connection status
- `/launch` - Start attack
- `/halt` - Stop attack immediately
- `/hold` - Hold/wait for commands
- `/update` - Update client code
- `/config` - Show current attack configuration
- `/bots` - List connected bots

How do I setup/test _NetBot_ (Original TCP Version)?
--
- You can test this software in a single machine itself, but the ultimate point of this software to deploy the client (bots) on different machines and the server code (CCC) on your machine.
  - **very important** Make sure you modify the CCC server address on the _netbot_client.py_ code, else the bots will not connect to your CCC.
- More to be added in Wiki section soon.



NetBot CCC Server
--
![netbot intro](https://raw.githubusercontent.com/skavngr/netbot/main/netbot_server.PNG)
