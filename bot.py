# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from io import BytesIO
import sys
import logging
import pickle
import os
from urllib2 import urlopen, URLError, HTTPError
import random

import settings

#TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TOKEN = '529411976:AAGkvuxGf9YRSI_Hy_HxWUV488Mvk-o6hGo'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self):
        self.last_command = None
        self.waiting = False
        self.uploaded_audio = 0
        self.beat_file_name = 'beat'+str(random.randrange(1,8))

        self.logger = logging.getLogger(__name__)

        self.updater = Updater(TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        help_handler = CommandHandler('help', self.help)
        newteam_handler = CommandHandler('newteam', self.newteam)
        message_handler = MessageHandler(Filters.text, self.text_handler)

        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(newteam_handler)


        self.dispatcher.add_error_handler(self.error)

        print "starting "
        self.updater.start_polling()

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def text_handler(self, bot, update):
        print 'Text Handler'
        print self.last_command
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        message = bot.send_message(text="Cейчас все будет...",
                                   chat_id=chat_id)

    def newteam(self,bot,update):
        print 'New Team Handler'
        self.last_command = 'newteam'
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        message = bot.send_message(text="Создаем новую команду",
                                   chat_id=chat_id)

    @staticmethod
    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.HELP_MESSAGE)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    bio = BytesIO()
    bot = Bot()
