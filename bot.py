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
from model import Model

#TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TOKEN = '529411976:AAGkvuxGf9YRSI_Hy_HxWUV488Mvk-o6hGo'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self):
        self.last_command = None
        self.waiting = False
        self.team = {}
        self.resume= {}
        self.uploaded_audio = 0
        self.model = Model()

        self.logger = logging.getLogger(__name__)

        self.updater = Updater(TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        help_handler = CommandHandler('help', self.help)
        newteam_handler = CommandHandler('newteam', self.newteam)
        search_handler = CommandHandler('search', self.search)
        cancel = CommandHandler('cancel', self.search)
        message_handler = MessageHandler(Filters.text, self.text_handler)

        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(newteam_handler)
        self.dispatcher.add_handler(search_handler)


        self.dispatcher.add_error_handler(self.error)

        print "Bot: start polling"
        self.updater.start_polling()

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)
    def cancel(self, bot, update, error):
        self.last_command = 'cancel'

    def text_handler(self, bot, update):
        print 'Bot: Text Handler'
        print self.last_command
        chat_id = update.message.chat_id
        text = update.message.text.lower()
        if self.last_command == 'newteam':
            self.team[self.data_type] = text
            if self.data_type == 'name':
                self.data_type = 'idea'
            elif self.data_type == 'idea':
                self.data_type = 'people'
            elif self.data_type == 'people':
                text = text.split(',')
                print "He needs %i people"%len(text)
                self.team[self.data_type] = text
                self.data_type = 'budget'
            elif self.data_type == 'budget':
                self.data_type = 'done'
                self.last_command = 'done'
                self.model.find(self.team)
                message=bot.send_message(text="Ваш персональный адрес проекта:\n "+
                                     'http://10.10.188.11:3000/'+self.team['name'],
                                   chat_id=chat_id)
            print self.team
            message=bot.send_message(text=settings.CREATE_TEAM[self.data_type],
                                   chat_id=chat_id)
        elif self.last_command == 'search':
            self.resume[self.data_type] = text
            if self.data_type == 'name':
                self.data_type = 'about'
            elif self.data_type == 'about':
                self.data_type = 'passion'
            elif self.data_type == 'passion':
                self.data_type = 'schedule'
            elif self.data_type == 'schedule':
                self.data_type = 'link'
            elif self.data_type == 'link':
                self.data_type = 'done'
            print self.resume
            message=bot.send_message(text=settings.SEARCH_TEAM[self.data_type],
                                   chat_id=chat_id)

    def search(self,bot,update):
        print ' Search Handler'
        self.last_command = 'search'
        self.data_type= 'name'
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        message = bot.send_message(text="Найдем вам тимлида! Как Вас зовут?",
                                   chat_id=chat_id)
    def newteam(self,bot,update):
        print 'New Team Handler'
        self.last_command = 'newteam'
        self.data_type= 'name'
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        message = bot.send_message(text="Создаем новую команду! \cancel чтобы отментить \n Как назывется проект? ",
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
