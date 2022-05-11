# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import telebot
from telebot import types
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    bot = telebot.TeleBot("5205547272:AAG13BXkVQHURrh9PvQfltDOuTgZe1jh9A0")

    f = open('titles.txt', 'r', encoding='UTF-8')
    titlesrows = f.read().split('\n')
    f.close()

    title_name_pos = 0
    episode_num_pos = 1
    release_date_pos = 2
    picture_link_pos = 3
    separator = "|"



    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🔥 Что сегодня выйдет?")
        item2 = types.KeyboardButton("🤔 Что посмотреть?")
        item3 = types.KeyboardButton("Настроить")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(m.chat.id, "Чего желаете?",  reply_markup=markup)


    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        answer = ""
        picture_link = ""
        if message.text.strip() == '🔥 Что сегодня выйдет?':
            for item in titlesrows:
                if "17.04.22" in item:
                    answer += item.split(separator)[title_name_pos] + ", " + item.split(separator)[episode_num_pos]
                    picture_link = item.split(separator)[picture_link_pos]
            bot.send_photo(message.chat.id,
                           picture_link,
                           caption="📢 " + answer)

        elif message.text.strip() == '🤔 Что посмотреть?':
            answer_row = random.choice(titlesrows)
            answer = answer_row.split(separator)[title_name_pos]
            picture_link = answer_row.split(separator)[picture_link_pos]
            keyboard = types.InlineKeyboardMarkup()
            key_seen = types.InlineKeyboardButton(text='Видел', callback_data='seen');  # кнопка «Да»
            keyboard.add(key_seen);  # добавляем кнопку в клавиатуру
            key_will_watch = types.InlineKeyboardButton(text='Посмотрю', callback_data='will_watch');
            keyboard.add(key_will_watch);
            bot.send_photo(message.chat.id,
                           picture_link,
                           caption="👀 " + answer,
                           reply_markup=keyboard)
        elif message.text.strip() == 'Настроить':
            answer = "Настроил"
        print(answer)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "seen":  # call.data это callback_data, которую мы указали при объявлении кнопки
                answer_seen = "Понял, а как насчет этого?\n"
                seen_answer_row = random.choice(titlesrows)
                answer_seen += seen_answer_row.split(separator)[title_name_pos]
                picture_link = seen_answer_row.split(separator)[picture_link_pos]
                keyboard = types.InlineKeyboardMarkup()
                key_seen = types.InlineKeyboardButton(text='Видел', callback_data='seen');  # кнопка «Да»
                keyboard.add(key_seen);  # добавляем кнопку в клавиатуру
                key_will_watch = types.InlineKeyboardButton(text='Посмотрю', callback_data='will_watch');
                keyboard.add(key_will_watch);
                bot.send_photo(call.message.chat.id,
                               picture_link,
                               caption="👀 " + answer_seen,
                               reply_markup=keyboard)
            elif call.data == "will_watch":
                bot.send_message(call.message.chat.id, "Приятного просмотра!")
        # Отсылаем юзеру сообщение в его чат
        # bot.send_message(message.chat.id, answer)
        # bot.send_photo(message.chat.id, "https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/88a3134f-b55d-46dc-b28b-0573f33db7f4/300x450", caption="📢 " + answer)

    bot.polling(none_stop=True, interval=0)
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_item = types.KeyboardButton("START")
    bot.send_message()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
