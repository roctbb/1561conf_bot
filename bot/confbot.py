import json
import random

import telebot
from config import TOKEN
import uuid
from tools import count_red, qr_decode

bot = telebot.TeleBot(TOKEN)

data = {
    "prizes": [],
    "codes": [],
    "results": {},
    "topics": []
}


def load():
    for key in data:
        try:
            with open(key + ".json") as source:
                data[key] = json.load(source)
        except:
            pass


def save():
    for key in data:
        try:
            with open(key + ".json", 'w') as source:
                json.dump(data[key], source, ensure_ascii=False)
        except:
            pass


def store_photo_for_message(message):
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    downloaded_file = bot.download_file(path.file_path)

    # узнаем расширение и случайное придумываем имя
    extn = '.' + str(path.file_path).split('.')[-1]
    name = 'images/' + str(uuid.uuid4()) + extn

    # создаем файл и записываем туда данные
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    return name


@bot.message_handler(content_types=["photo"])
def process_photo(message):
    chat_id = message.chat.id
    name = store_photo_for_message(message)

    code = qr_decode(name)
    if not code:
        bot.send_message(chat_id, "👀 Я не вижу QR кода на фотографии, попробуй прислать более аккуратную фотографию. ")

    elif code not in data['codes']:
        bot.send_message(chat_id, "🧐 Похоже, QR код на фотке не мой... ")

    elif code in data['results']:
        if data['results'][code] == 'ничего':
            bot.send_message(chat_id, f"🥸 Ты уже прислал свой билет! ")
        else:
            bot.send_message(chat_id, f"🤡 Ты уже прислал свой билет, твой приз - {data['results'][code]}.")
    else:
        bot.send_message(chat_id, "🎰🎰🎰")
        count = count_red(name)

        if count == 0:
            bot.send_message(chat_id, f"🤡 Я не вижу печатей на бланке. Если это не так, обратись к организаторам.")
        else:
            available_prizes_nums = [-1]

            for i, prize in enumerate(data['prizes']):
                if prize['q'] > 0 and prize['min_signs'] <= count:
                    available_prizes_nums.append(i)

            choice = random.choice(available_prizes_nums)

            if choice == -1:
                bot.send_message(chat_id, f"😭 К сожалению, ты ничего не выиграл. Ничего, повезет в следующий раз!")
                data['results'][chat_id] = 'ничего'
            else:
                prize = data['prizes'][choice]
                prize['q'] -= 1
                data['results'][code] = prize['name']

                bot.send_message(chat_id, f"🎁 Поздравляем!!! Твой приз - {prize['name']}!")
                bot.send_message(chat_id, f"🥳 Чтобы получить приз, покажи это сообщение на столике организаторов Бинго!")

            bot.send_message(chat_id, "🦾 В любом случае, вот твоя идея для проекта / исследования от ChatGPT:")
            bot.send_message(chat_id, random.choice(data['topics']))
            bot.send_message(chat_id, "📝 Если хочешь получить другую идею для работы, просто напиши /idea, у нас их много!")

            save()

@bot.message_handler(commands=['idea'])
def idea(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "🦾 Вот еще одна идея для проекта / исследования от ChatGPT:")
    bot.send_message(chat_id, random.choice(data['topics']))

@bot.message_handler(commands=['start', 'help'])
def help(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "👋 Привет! Я бот, который разыгрывает призы Проектного Бинго!")
    bot.send_message(chat_id, "🔥 Чтобы принять участие, просто получи билет с QR кодом у организаторов на входе и выполняй задания / отвечай на вопросы участников конференции, чтобы получить печати. Чем больше печатей, тем больше вероятность получить приз!")
    bot.send_message(chat_id, "📒 В конце конференции (не раньше) пришли мне аккуратную фотографию своего билета (чтобы на фотографии был только билет), а я в ответ пришлю тебе идею для проекта от ChatGPT и, возможно, приятный сувенир.")

load()
print(data['codes'])

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
