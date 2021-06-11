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

from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, Update,
)
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, CommandHandler,
    ConversationHandler, Updater,
)


#
# TELEGRAM_TOKEN from os environment
#
telegram_token = os.getenv('TELEGRAM_TOKEN', default=None)

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
# Menu definition
#

function_handlers = {"commands": {
    'start': {
        'start_handler': {
            "handler": start,
            "text": "Start handler, Choose a route",
            "keyboard": [
                {0: "One", 1: "Two", },
            ]},
        'handlers': {
            0: {
                0: {"handler": one,
                    "text": (
                        "First CallbackQueryHandler."
                        " Choose a route"),
                    "keyboard": [
                        {2: "Three", 3: "Four", },
                    ]},
                1: {"handler": two,
                    "text": (
                        "Second CallbackQueryHandler."
                        " Choose a route"),
                    "keyboard": [
                        {0: "One", 2: "Three", },
                    ]},
                2: {"handler": three,
                    "text": (
                        "Third CallbackQueryHandler."
                        " Do want to start over?"),
                    "keyboard": [
                        {
                            0: "Yes, let's do it again!",
                            1: "Nah, I've had enough ...", },
                    ]},
                3: {"handler": four,
                    "text": (
                        "Fourth CallbackQueryHandler."
                        " Choose a route"),
                    "keyboard": [
                        {1: "Two", 2: "Three", },
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
        }}}}


def main() -> None:
    """Run the bot."""

    if telegram_token is None:
        logger.warning("Telegram token not found in env.")
        return

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    #
    # /start
    #

    handler_context = function_handlers["commands"]['start']
    dispatcher.add_handler(make_conversation(
        command_name='start', command_handler=handler_context[
            'start_handler']["handler"],
        function_handlers=handler_context['handlers']))

    #
    # Start the Bot (poll)
    #

    updater.start_polling()


if __name__ == '__main__':
    main()
