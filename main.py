import telebot

API_TOKEN = "توکن_ربات_اینجا"

bot = telebot.TeleBot(API_TOKEN)

# آی‌دی عددی مدیر
ADMIN_ID = 5392839162

# دیتا
combos = [
    {"title": "اکانت متیک لجند تستی", "percent": "تستی", "price": 50000, "stock": 5},
    {"title": "اکانت متیک لجند ۷۵٪", "percent": "75٪", "price": 100000, "stock": 3},
    {"title": "اکانت متیک لجند ۸۵٪", "percent": "85٪", "price": 130000, "stock": 2},
    {"title": "اکانت متیک لجند ۱۰۰٪", "percent": "100٪", "price": 190000, "stock": 1},
]

user_balances = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 خرید کمبو", "💳 افزایش موجودی")
    if message.from_user.id == ADMIN_ID:
        markup.row("🛠 پنل مدیریت")
    bot.send_message(message.chat.id, "به ربات فروش کمبولیست خوش اومدی", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💳 افزایش موجودی")
def topup(message):
    bot.send_message(message.chat.id, "برای افزایش موجودی:
"
                                      "مبلغ دلخواه را کارت به کارت کنید به:
"
                                      "6037998198937616
"
                                      "به‌نام: ابولفضل
"
                                      "سپس رسید را ارسال کنید.")
    bot.register_next_step_handler(message, handle_receipt)

def handle_receipt(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "رسید شما برای مدیر ارسال شد. پس از تایید، موجودی شارژ می‌شود.")

@bot.message_handler(func=lambda m: m.text == "🛠 پنل مدیریت" and m.from_user.id == ADMIN_ID)
def admin_panel(message):
    bot.send_message(message.chat.id, "پنل مدیر فعال است.")

@bot.message_handler(func=lambda m: m.text == "🛒 خرید کمبو")
def show_combos(message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)
    text = f"موجودی شما: {balance} تومان

"
    for idx, c in enumerate(combos):
        text += f"{idx+1}. {c['title']}
درصد: {c['percent']}
قیمت: {c['price']} تومان
تعداد: {c['stock']}

"
    text += "برای خرید عدد کمبو مورد نظر را بفرستید (مثلاً 1)"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, handle_buy)

def handle_buy(message):
    user_id = message.from_user.id
    index = int(message.text.strip()) - 1
    if 0 <= index < len(combos):
        combo = combos[index]
        if combo["stock"] > 0:
            if user_balances.get(user_id, 0) >= combo["price"]:
                user_balances[user_id] -= combo["price"]
                combos[index]["stock"] -= 1
                bot.send_message(message.chat.id, f"خرید با موفقیت انجام شد! اکانت: {combo['title']}")
            else:
                bot.send_message(message.chat.id, "موجودی شما کافی نیست.")
        else:
            bot.send_message(message.chat.id, "این کمبو تموم شده.")
    else:
        bot.send_message(message.chat.id, "عدد نامعتبر.")

bot.polling()