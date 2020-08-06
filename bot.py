import telebot
import config
import random

from telebot import types
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(config.TOKEN)

#main keyboard
markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton("Обо мне")
item2 = types.KeyboardButton("Связаться")
item3 = types.KeyboardButton("Сыграть в игру?")

markup.add(item1, item2, item3)
#

#second keyboard
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1v2 = types.KeyboardButton("Проекты")
item2v2 = types.KeyboardButton("Фотографии")
item3v2 = types.KeyboardButton("Резюме")
item4v2 = types.KeyboardButton("В начало")

markup2.add(item1v2, item2v2, item3v2, item4v2)
#

#contacts keyboard

markup3 = types.ReplyKeyboardMarkup(resize_keyboard =True)
item1v3 = types.KeyboardButton("VK")
item2v3 = types.KeyboardButton("Telegram")
item3v3 = types.KeyboardButton("Email")
item4v3 = types.KeyboardButton("В начало")

markup3.add(item1v3, item2v3, item3v3, item4v3)

#
cvtext = open('static/CVtext.txt', mode = 'r', encoding = 'UTF-8')
cv = cvtext.read()
aboutText = open('static/About.txt', 'r', encoding = 'UTF-8')
about = aboutText.read()

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id,
    "Добро пожаловать, {0.first_name}!\nЯ - бот помощник. Я хочу продемонстрировать вам резюме Артёма Минченкова. Для просмотра всех команд введите <b>/help</b>".format(message.from_user),
    parse_mode='html', reply_markup = markup)

@bot.message_handler(commands = ['help'])
def botmes(message):
    bot.send_message(message.chat.id, "Для работы с ботом используйте встроенную клавиатуру, либо команды, что вы видите ниже!\n<b>/contacts - связаться со мной!</b>\n <i>-/vk\n -/telegram\n -/email</i>\n<b>/about - обо мне.</b>\n <i>-/projects - расскажу и покажу про свой бэкграунд 🙃\n -/photo - немного фотографий со мной.\n -/CV - резюме!</i>\n<b>/game - игра</b>",
    parse_mode = 'html')


@bot.message_handler(content_types = ['text'])
def main(message):
    photo_1 = open('static/photo1.jpg', 'rb')
    photo_2 = open('static/photo2.jpg', 'rb')

    if message.text == 'Сыграть в игру?' or message.text == '/game':
        msg = bot.send_message(message.chat.id, "Введите число от 1 до 6. Если вы угадали число, которое я загадал. Я отправлю Вам исходный код бота (.py)\n\nДля выхода из игры напишите: !stop", parse_mode ='html')
        text = message.text
        bot.register_next_step_handler(msg, game)


        #######
    if message.text == 'Связаться' or message.text == '/contacts':
        bot.send_message(message.chat.id, "Каким способом Вы хотели бы связаться?", reply_markup = markup3)
    elif message.text == 'VK' or message.text == '/vk':
        bot.send_message(message.chat.id, "<b>https://vk.com/vsetvoidruziya</b>", parse_mode = 'html')
    elif message.text == 'Telegram' or message.text == '/telegram':
        bot.send_message(message.chat.id, "<b>@artemminchenkov</b>", parse_mode = 'html')
    elif message.text == 'Email' or message.text == '/email':
        bot.send_message(message.chat.id, "<b>vavilon50a@gmail.com</b>", parse_mode = 'html')
    elif message.text == "В начало":
        bot.send_message(message.chat.id, "Идём в начало...🤔", reply_markup = markup)

        #######
    if message.text == 'Обо мне' or message.text == '/about':
        bot.send_message(message.chat.id, "Что Вас интересует?", reply_markup = markup2)
    elif message.text == 'Проекты' or message.text == '/projects':
        bot.send_message(message.chat.id, "https://github.com/Artemqas - здесь я храню свои исходники", reply_markup = markup2)
    elif message.text == 'Фотографии' or message.text == '/photo':
        bot.send_media_group(message.from_user.id, [InputMediaPhoto(photo_1), InputMediaPhoto(photo_2)])
        #bot.send_photo(message.chat.id, photo_1, reply_markup = markup2)
        #bot.send_photo(message.chat.id, photo_2, reply_markup = markup2)
    elif message.text == 'Резюме' or message.text == '/CV':
        bot.send_message(message.chat.id, cv)
        bot.send_message(message.chat.id, about ,reply_markup = markup2)
        #cvfile = open('/static/kek.pdf')
        #bot.send_file(message.chat.id, cvfile )

def game(message):
    ran = random.randint(1,6)
    if str(message.text) == str(ran):
        bot.send_message(message.chat.id, "А вы упорный, так и быть, держите:\nGame over, you win!")
        botFile = open('static/botcopy.py', 'rb')
        bot.send_document(message.chat.id, botFile)
    elif message.text == 'Обо мне' or message.text == 'Связаться':
        msg1 = bot.send_message(message.chat.id, "Мы в игре! Если хотите выйти, напишите: !stop")
        bot.register_next_step_handler(msg1, game)
    elif message.text == 'Сыграть в игру?':
        bot.send_message(message.chat.id, "Мы уже играем, просто введите число от 1 до 6. Если хотите выйти, напишите: !stop")
    elif message.text == '!stop':
        main(message)
    else:
        msg = bot.send_message(message.chat.id, "Можете попробовать еще раз, просто введите число заново :)\n\nДля выхода из игры напишите: !stop", parse_mode ='html')
        bot.register_next_step_handler(msg, game)
        return

#RUN
bot.polling(none_stop=True)
