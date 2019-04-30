from telebot import TeleBot, types  # подключаем модуль
from config_rating import token
import logic_rating
import os
import time

bot = TeleBot(token)  # создаём объект телеграм бота с нашим ключом (токеном)

#
# Следующая часть относится к регистрации и авторизации пользователя
#

@bot.message_handler(func=lambda message: int(message.chat.id)<0)
def error_in_chat(message):
    bot.send_message(message.chat.id,
                     'Вызов данного бота в чатах запрещён')

@bot.message_handler(commands=['start'])  # хэндлер он же перехватчик или обработчик
def start(message):
    if logic_rating.get_user_status(message.from_user.id) == 0:
        logic_rating.set_user_status(message.from_user.id, 1)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*logic_rating.names())
        logic_rating.save_delete_message(message.from_user.id, bot.send_message(message.from_user.id, 'Представься, пожалуйста!', reply_markup=keyboard).message_id)
    elif logic_rating.get_user_status(message.from_user.id) == 25:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*logic_rating.names())
        keyboard.add(types.InlineKeyboardButton(text='Результат урока', callback_data=-25))
        logic_rating.save_delete_message(message.from_user.id,
                                         bot.send_message(message.from_user.id, 'Здравствуй, учитель! Здесь можно поставить дополнительные баллы!',
                                                          reply_markup=keyboard).message_id)

@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if logic_rating.get_user_status(c.message.chat.id) < 2:
        logic_rating.save_id(c.message.chat.id, c.data)
        bot.send_message(c.message.chat.id, "Отлично")
        try:
            bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
        except:
            pass
        logic_rating.set_user_status(c.message.chat.id, 2)
        keyboard_names = types.InlineKeyboardMarkup(row_width=1)
        keyboard_names.add(*logic_rating.buttons(c.message.chat.id))
        logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Выбери одноклассника для оценки.",
                                                      reply_markup=keyboard_names).message_id)
    elif logic_rating.get_user_status(c.message.chat.id) == 2:
        if logic_rating.get_student_status(c.data) == 0:
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            logic_rating.set_user_status(c.message.chat.id, 3)
            keyboard_names = types.InlineKeyboardMarkup(row_width=1)
            keyboard_names.add(*logic_rating.save(c.message.chat.id, c.data))
            keyboard_names.add(types.InlineKeyboardButton(text='Сохранить', callback_data=-5))
            logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Отлично",
                         reply_markup=keyboard_names).message_id)
        else:
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            keyboard_names = types.InlineKeyboardMarkup(row_width=1)
            keyboard_names.add(*logic_rating.buttons(c.message.chat.id))
            logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Извини, кто-то уже выбрал его для оценивания. Выбери одноклассника для оценки.",
                             reply_markup=keyboard_names).message_id)
    elif logic_rating.get_user_status(c.message.chat.id) == 3:
        if int(c.data) != -5:
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            keyboard_names = types.InlineKeyboardMarkup(row_width=1)
            keyboard_names.add(*logic_rating.save_student(c.message.chat.id, c.data))
            keyboard_names.add(types.InlineKeyboardButton(text='Сохранить', callback_data=-5))
            logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Отлично",
                         reply_markup=keyboard_names).message_id)
        else:
            logic_rating.set_user_status(c.message.chat.id, 4)
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            keyboard_names = types.InlineKeyboardMarkup(row_width=1)
            keyboard_names.add(*logic_rating.save(c.message.chat.id, c.data))
            keyboard_names.add(types.InlineKeyboardButton(text='Сохранить', callback_data=-5))
            logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Отлично, а теперь оцени себя!",
                         reply_markup=keyboard_names).message_id)
    elif logic_rating.get_user_status(c.message.chat.id) == 4:
        if int(c.data) != -5:
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            keyboard_names = types.InlineKeyboardMarkup(row_width=1)
            keyboard_names.add(*logic_rating.save_self(c.message.chat.id, c.data))
            keyboard_names.add(types.InlineKeyboardButton(text='Сохранить', callback_data=-5))
            logic_rating.save_delete_message(c.message.chat.id, bot.send_message(c.message.chat.id, "Отлично, а теперь оцени себя!",
                         reply_markup=keyboard_names).message_id)
        else:
            logic_rating.set_user_status(c.message.chat.id, 5)
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            bot.send_message(c.message.chat.id, "Спасибо! На этом всё 🏆")
    elif logic_rating.get_user_status(c.message.chat.id) == 25:
        if c.data != '-25':
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id), chat_id=c.message.chat.id)
            except:
                pass
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*logic_rating.names_and_marks(c.data))
            keyboard.add(types.InlineKeyboardButton(text='Результат урока', callback_data=-25))
            logic_rating.save_delete_message(c.message.chat.id,
                                             bot.send_message(c.message.chat.id,
                                                              'Здравствуй, учитель! Здесь можно поставить дополнительные баллы!',
                                                              reply_markup=keyboard).message_id)
        else:
            logic_rating.set_user_status(c.message.chat.id, 25)
            try:
                bot.delete_message(message_id=logic_rating.get_delete_message(c.message.chat.id),
                                   chat_id=c.message.chat.id)
            except:
                pass
            s = logic_rating.result()
            bot.send_message(c.message.chat.id, s)

while True:
    try:
        bot.polling(none_stop=True)
    # ConnectionError and ReadTimeout because of possible timout of the requests library
    # TypeError for moviepy errors
    # maybe there are others, therefore Exception
    except Exception as e:
        print('\n\n',e,'\n\n')
        time.sleep(1)
# if __name__ == '__main__':
#     bot.polling(none_stop=True)
