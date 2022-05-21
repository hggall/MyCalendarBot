#!usr/bin/env python

import os
import json
from datetime import datetime
from telegram import Update, ForceReply, User
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

'''
First try on a bot on telegram that works as a calendar: create events and get remainders
TODO:
	-Store events in a plain file
	-Get remainders -> Get another script written in Python scheduled in CRON that reads the events every 5 minutes and then sends message
	for the upcoming event.
'''

token = open('HTTP_Access_Token.txt', 'r')
JSON_events = 'EventStorage.json'
open_token = token.read()
EVENT, TIME, RESULT = range(3)
name_event = ''
# if not os.path.exists(JSON_events):
#    	EventStorage = open(JSON_events, 'w')
#    	events_stored = {}
#    	EventStorage.close()
# else:
#    	EventStorage = open(JSON_events, 'r')
#    	events_stored = json.load(EventStorage)
#    	EventStorage.close()

events_stored = {}
# ANSWER = None

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\! Im a calendar bot, create events and get reminders\! Use the \/help command for more information",
        reply_markup=ForceReply(selective=True),
    )

def event_creation(update: Update, context: CallbackContext) -> str:
    """Users will insert an event to be later stored, the information will be the name of the event, 
    it will be given an ID, later, the user will be prompted to insert the date and time of this event"""
    update.message.reply_text('What name are you giving the event?')
    return EVENT
    

def event_created(update: Update, context: CallbackContext) -> str:
    """"""
    global name_answer
    name_answer = str(update.message.text)
    # print(name_answer)
    update.message.reply_text('Cool! Now gimme a date for that (Format-> DD/MM/YYYY HH:MM:SS)')
    return TIME

def event_created_with_name(update: Update, context: CallbackContext) -> str:
    """"""
    global timestamp, user_id
    time = update.message.text
    timestamp = datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
    user_id = User.id
    update.message.reply_text('Time: ' + str(timestamp) + '\nName of the event: ' + name_answer + '\nDo you confirm this?')
    return RESULT

def store_event(update: Update, context: CallbackContext) -> None:
    """"""
    answer = update.message.text

    if answer=='Y':
    	update.message.reply_text('Okay. Event stored!')
    	info_stored_in_dict = name_answer + "_" + str(timestamp)
    	if user_id in events_stored.keys():
    		events_stored[user_id] += [info_stored_in_dict]	    		
    	else:
    		events_stored[user_id] = [info_stored_in_dict]
    	
    	# with open(JSON_events, 'a') as file_object:
    	# 		json.dump(events_stored, file_object)
    else:
    	update.message.reply_text('Event will not be stored.')

    return ConversationHandler.END 

def error(update: Update, context: CallbackContext) -> None:
	""""""
	update.message.reply_text('There was an error. Try again!')
	
	return ConversationHandler.END 


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def main() -> None:

	updater = Updater(open_token)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", help_command))

	dispatcher.add_handler(ConversationHandler(
		entry_points=[
			CommandHandler("newevent", event_creation)
		],
		states={
			EVENT: [MessageHandler(Filters.text , event_created)],
			TIME: [MessageHandler(Filters.regex(r'^[0-3][0-9]\/[0-1][0-9]\/20[0-9][0-9]\s[0-2][0-9]\:[0-5][0-9]\:[0-5][0-9]$') , event_created_with_name)],
			RESULT: [MessageHandler(Filters.regex(r'^[Y|N]$') , store_event)]
		},
		fallbacks=[MessageHandler(Filters.text , error)]
		))
	updater.start_polling()
	updater.idle()



if __name__ == '__main__':
	main()
	