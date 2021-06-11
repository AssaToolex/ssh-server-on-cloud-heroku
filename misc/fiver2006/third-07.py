#!/usr/bin/env python

"""Stage inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler.
Then, those functions are passed to the Dispatcher and registered
at their respective places. Then, the bot is started and runs until
we press Ctrl-C on the command line.

Usage:
Example of a bot that uses inline keyboard that has multiple
CallbackQueryHandlers arranged in a ConversationHandler.

Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""

import logging
import os
from uuid import uuid4

from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, Update,
)
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, CommandHandler,
    ConversationHandler, Filters, MessageHandler, Updater,
)
from telegram.ext.dispatcher import Dispatcher


#
# TELEGRAM_TOKEN from os environment
#
telegram_token = os.getenv('TELEGRAM_TOKEN', default=None)

#
# Web
#
WEB_PORT = int(os.getenv('PORT', default=5000))
HEROKU_APPNAME = os.getenv('HEROKU_APPNAME', default=None)

#
# Enable logging
#
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#
# Common functions
#

def inline_answer_handler(return_state):
    """Inline answer Decorator."""
    def my_decorator(func):
        def wrapper(update: Update, context: CallbackContext):
            update.callback_query.answer()
            func(update, context)
            return return_state
        return wrapper
    return my_decorator


def inlinekeyboard_markup(keyboard_context: dict):
    """InlineKeyboard generator."""
    keyboard = [
        [InlineKeyboardButton(v, callback_data=str(k))
         for k, v in key_lines.items()]
        for key_lines in keyboard_context]
    return InlineKeyboardMarkup(keyboard)


def make_conversation(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: dict = {}) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/
        examples/inlinekeyboard2.py
    """

    states = {
        state_id: [CallbackQueryHandler(
            v["handler"], pattern='^' + str(k) + '$')
            for k, v in state_value.items()]
        for state_id, state_value in function_handlers.items()}
    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states=states)


#
# Menu handlers
#

def start(update: Update, context: CallbackContext) -> int:
    """Send first message on `/start` command."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    update.message.reply_text("Hello, {}!".format(user.first_name))
    f_context = function_handlers["commands"]['start']['start_handler']
    update.message.reply_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))
    # Tell ConversationHandler that we're in state 0=`FIRST` now
    return 0


@inline_answer_handler(return_state=0)
def one(update: Update, context: CallbackContext):
    """One button."""
    f_context = function_handlers["commands"]['start']['handlers'][0][0]
    update.callback_query.edit_message_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))


@inline_answer_handler(return_state=0)
def two(update: Update, context: CallbackContext):
    """Two button."""
    f_context = function_handlers["commands"]['start']['handlers'][0][1]
    update.callback_query.edit_message_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))


@inline_answer_handler(return_state=1)
def three(update: Update, context: CallbackContext):
    """Three button."""
    f_context = function_handlers["commands"]['start']['handlers'][0][2]
    update.callback_query.edit_message_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))


@inline_answer_handler(return_state=0)
def four(update: Update, context: CallbackContext):
    """Four button."""
    f_context = function_handlers["commands"]['start']['handlers'][0][3]
    update.callback_query.edit_message_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))


@inline_answer_handler(return_state=0)
def start_over(update: Update, context: CallbackContext):
    """Over button."""
    f_context = function_handlers["commands"]['start']['handlers'][1][0]
    update.callback_query.edit_message_text(
        text=f_context["text"], reply_markup=inlinekeyboard_markup(
            keyboard_context=f_context['keyboard']))


@inline_answer_handler(return_state=ConversationHandler.END)
def end(update: Update, context: CallbackContext):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    f_context = function_handlers["commands"]['start']['handlers'][1][1]
    query = update.callback_query
    query.edit_message_text(text=f_context["text"])


#
# Message's h
#

def echo_bot(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text)


#
# Menu definition
#

function_handlers = {"commands": {
    'start': {
        'start_handler': {
            "handler": start,
            "text": "Start handler, Choose a route",
            "keyboard": [
                {0: "GROUPS / CHANNELS SIDE LOOK", },
                {1: "BOT SIDE LOOK", },
                {2: "MERCHANTS SIDE LOOK", },
            ]},
        'handlers': {
            0: {
                0: {"handler": one,
                    "text": "GROUPS / CHANNELS SIDE LOOK",
                    "keyboard": [
                        {0: "Contact Merchant", },
                        {1: "Competition & Lottery", 2: "Merchant Reviews", },
                        {3: "Sales & Discounts of Merchant", },
                        {4: "Settings", 5: "Kivunimmerkaz Bot", },
                        {6: "Contact Management", },
                    ]},
                1: {"handler": two,
                    "text": "BOT SIDE LOOK",
                    "keyboard": [
                        {0: "Secondhand Merkaz", },
                        {0: "Search By Type or Niche", },
                        {0: "Daily Sales & Discounts", },
                        {0: "Competitions & Lottery", },
                        {0: "Management", },
                    ]},
                2: {"handler": three,
                    "text": "MERCHANTS SIDE LOOK",
                    "keyboard": [
                        {0: "Post Product", },
                        {0: "Post Full Catalog with pictures", },
                        {0: "Post Contest", 1: "Post Lottery", },
                        {0: "Post Winners", },
                        {0: "Post Today’s Sale", 1: "Post Today’s Discount", },
                        {0: "See Statistics", },
                        {0: "Merchant Forum", },
                        {0: "Contact Management", },
                    ]},
            },
            1: {
                0: {"handler": start_over,
                    "text": "Start handler. Choose a route",
                    "keyboard": [
                        {0: "One", 1: "Two", },
                    ]},
                1: {"handler": end, "text": "See you next time!", },
            },
        }},
    "start_22": {  # "groups": {
        'start_handler': {
            },
        'handlers': {
            0: {
                0: {"handler": None,
                    "text": "Contact Merchant",
                    "keyboard": [{0: "Yes", }, ]},
                1: {"handler": None,
                    "text": "Competition & Lottery",
                    "keyboard": [{0: "Yes", }, ]},
                2: {"handler": None,
                    "text": "Merchant Reviews",
                    "keyboard": [{0: "Yes", }, ]},
                3: {"handler": None,
                    "text": "Sales & Discounts of Merchant",
                    "keyboard": [{0: "Yes", }, ]},
                4: {"handler": None,
                    "text": "Settings",
                    "keyboard": [{0: "Yes", }, ]},
                5: {"handler": None,
                    "text": "Kivunimmerkaz Bot",
                    "keyboard": [{0: "Yes", }, ]},
                6: {"handler": None,
                    "text": "Contact Management",
                    "keyboard": [{0: "Yes", }, ]},
            }
        },
    }
}}


def register_handlers(dispatcher: Dispatcher):
    """Register handlers to dispatcher."""

    #
    # Std
    #

    echo_handler = MessageHandler(
        Filters.text & (~Filters.command), echo_bot)
    dispatcher.add_handler(echo_handler)

    #
    # /start
    #

    handler_context = function_handlers["commands"]['start']
    dispatcher.add_handler(make_conversation(
        command_name='start', command_handler=handler_context[
            'start_handler']["handler"],
        function_handlers=handler_context['handlers']))


def main_poll() -> None:
    """Run the bot in poll mode."""

    if telegram_token is None:
        logger.warning("Telegram token not found in env.")
        return

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    register_handlers(dispatcher)

    #
    # Start the Bot (poll)
    #

    updater.start_polling()


def main_webhook():
    """Run the bot in webhook mode."""

    if telegram_token is None:
        logger.warning("Telegram token not found in env.")
        return

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    register_handlers(dispatcher)

    #
    # Start the Bot (webhook)
    #

    url_path = str(uuid4())  # url_path=telegram_token
    logger.info("webhook: {}".format((
        HEROKU_APPNAME, WEB_PORT, url_path)))

    updater.start_webhook(
        # listen="0.0.0.0",
        # port=int(WEB_PORT),
        url_path=url_path)
    updater.bot.setWebhook(
        'https://{}.herokuapp.com:{}/{}'.format(
            HEROKU_APPNAME, WEB_PORT, url_path))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if HEROKU_APPNAME is not None:
        main_webhook()
    else:
        main_poll()
