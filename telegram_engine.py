import telebot
import bot_rick
f = open("api_token")
token = f.readline()

bot = telebot.TeleBot(token)

model, dialog_df = bot_rick.precompute_data()
print("telegram bot running")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.strip() == "":
         bot.send_message(message.from_user.id, "WTF Morty?!")
    else:
        bot.send_message(message.from_user.id, "Rick: " + bot_rick.get_ans(message.text, model, dialog_df))

bot.polling(none_stop=True, interval=0.2)