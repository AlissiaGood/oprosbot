from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Q1, Q2, Q3, GENDER, CONTACT, FINISH = range(6)


def start(bot, update):
    reply_keyboard = [['Начать опрос']]
    update.message.reply_text(
        """Здравствуйте! Ответьте, пожалуйста, на несколько вопросов. Это займет не более трех минут:)\n
    Для отмены нажмите /cancel""",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q1
    
def q1(bot, update):
    user = update.message.from_user
    reply_keyboard = [['1', '2', '3', '4', '5']]
    update.message.reply_text(
        """Вопрос 1. Оцените, пожалуйста, по шкале от 1 до 5...""",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q2

def skip_Q1(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write('Отказ от ответа/n')
    return Q2


def q2(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write(update.message.text)
    reply_keyboard = [['1', '2', '3']]
    update.message.reply_text(
        """Вопрос 2. Оцените, пожалуйста, по шкале от 1 до 3...', '\n
    Чтобы пропустить вопрос, нажмите /skip""",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q3

def skip_Q2(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write('Отказ от ответа/n')
    return Q3

def q3(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write(update.message.text)
    reply_markup=ReplyKeyboardRemove()
    update.message.reply_text('Открытый вопрос...\n Чтобы пропустить вопрос, нажмите /skip')                          
    return GENDER

def skip_Q3(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write('Отказ от ответа/n')
    return GENDER

def gender(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write(update.message.text)
    reply_keyboard = [['Male', 'Female', 'Other']]
    update.message.reply_text(
        'Ваш пол?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CONTACT   


def contact(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write(update.message.text)
    reply_markup = ReplyKeyboardRemove()
    contact_keyboard = KeyboardButton(text="Поделиться контактом", request_contact=True)
    cancel_keyboard = KeyboardButton(text="Отмена", request_contact=False)
    custom_keyboard = [[ contact_keyboard, cancel]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("""Для проверки введенных данных с Вами свяжется наш оператор./n Если Вы не против, я запишу Ваш номер.""")
    return FINISH

def skip_contact(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write('Респондент не дал свой номер /n')
    return FINISH

def finish(bot, update):
    user = update.message.from_user
    with open('user.txt', 'a') as f:
        f.write(str(update.message.text)) 
    update.message.reply_text('Опрос закончен. Спасибо!')
    bot.send_photo(chat_id=chat_id, photo='http://www.pngall.com/wp-content/uploads/2016/04/Thank-You-Free-PNG-Image.png')
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("Респондент %s отказался от участия в опросе." % user.first_name)
    update.message.reply_text('Ладно, всего доброго!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("434828931:AAG5oYqpmYiHYsyD3dHNMyKwkJq-syn-S9U")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            Q1: [RegexHandler('^(Начать опрос)$', q1),
                     CommandHandler('skip', skip_Q1)],  

            Q2: [RegexHandler('^(1|2|3|4|5)$', q2),
                    CommandHandler('skip', skip_Q2)],

            Q3:[RegexHandler('^(1|2|3)$', q3),
                    CommandHandler('skip', skip_Q3)],

            GENDER: [MessageHandler(Filters.text, gender)],

            CONTACT: [RegexHandler('^(Male|Female|Other)$', contact),
                   CommandHandler('skip', skip_contact)],

            FINISH: [MessageHandler(Filters.contact, finish)]
          },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
