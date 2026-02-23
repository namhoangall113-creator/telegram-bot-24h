import telebot
import json
import os
import random
import time

TOKEN = "DAN_TOKEN_CUA_BAN_VAO_DAY"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user(data, user_id):
    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "last_qc": 0,
            "last_reward": 0
        }
    return data[user_id]

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Số dư", "📺 Xem quảng cáo")
    markup.add("🎁 Nhận thưởng", "🎮 Mini game")
    markup.add("💸 Rút tiền")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))
    save_data(data)
    bot.send_message(message.chat.id, "Chào mừng đến bot kiếm xu!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "💰 Số dư")
def balance(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))
    bot.send_message(message.chat.id, f"Số dư: {user['balance']} xu")

@bot.message_handler(func=lambda m: m.text == "📺 Xem quảng cáo")
def xem_qc(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))

    if time.time() - user["last_qc"] < 30:
        bot.send_message(message.chat.id, "Vui lòng đợi 30 giây!")
        return

    user["balance"] += 10
    user["last_qc"] = time.time()
    save_data(data)

    bot.send_message(message.chat.id, "Bạn nhận 10 xu!")

@bot.message_handler(func=lambda m: m.text == "🎁 Nhận thưởng")
def reward(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))

    if time.time() - user["last_reward"] < 3600:
        bot.send_message(message.chat.id, "1 tiếng mới nhận lại được!")
        return

    user["balance"] += 50
    user["last_reward"] = time.time()
    save_data(data)

    bot.send_message(message.chat.id, "Bạn nhận 50 xu!")

@bot.message_handler(func=lambda m: m.text == "🎮 Mini game")
def game(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))

    if user["balance"] < 20:
        bot.send_message(message.chat.id, "Cần 20 xu để chơi!")
        return

    user["balance"] -= 20

    if random.randint(1, 2) == 1:
        user["balance"] += 40
        bot.send_message(message.chat.id, "Bạn thắng! +40 xu")
    else:
        bot.send_message(message.chat.id, "Bạn thua!")

    save_data(data)

@bot.message_handler(func=lambda m: m.text == "💸 Rút tiền")
def withdraw(message):
    data = load_data()
    user = get_user(data, str(message.from_user.id))

    if user["balance"] < 500:
        bot.send_message(message.chat.id, "Cần 500 xu để rút!")
        return

    user["balance"] -= 500
    save_data(data)

    bot.send_message(message.chat.id, "Yêu cầu rút tiền đã được ghi nhận!")

bot.infinity_polling()
