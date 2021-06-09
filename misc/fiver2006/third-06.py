#!/usr/bin/env python

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
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


# TELEGRAM_TOKEN
telegram_token = os.getenv('TELEGRAM_TOKEN', default=None)

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def inline_handler(return_state):
    """Inline answer Decorator."""
    def my_decorator(func):
        def wrapper(update: Update, context: CallbackContext):
            query = update.callback_query
            query.answer()
            func(update, context)
            return return_state
        return wrapper
    return my_decorator


def inlinekeyboard_menu(context):
    keyboard = [
        [InlineKeyboardButton(v, callback_data=str(k)) for k, v in x.items()]
        for x in context["keyboard"]]
    print(keyboard)
    return InlineKeyboardMarkup(keyboard)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(0)),
            InlineKeyboardButton("2", callback_data=str(1)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return 0



@inline_handler(return_state=0)
def one(update: Update, context: CallbackContext):
    f_context = function_handlers["commands"]['start']['handlers'][0][0]
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(inlinekeyboard_menu(f_context))
    query.edit_message_text(text=f_context["text"], reply_markup=reply_markup)


@inline_handler(return_state=0)
def two(update: Update, context: CallbackContext):
    f_context = function_handlers["commands"]['start']['handlers'][0][1]
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(inlinekeyboard_menu(f_context))
    query.edit_message_text(text=f_context["text"], reply_markup=reply_markup)


@inline_handler(return_state=1)
def three(update: Update, context: CallbackContext):
    f_context = function_handlers["commands"]['start']['handlers'][0][2]
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(inlinekeyboard_menu(f_context))
    query.edit_message_text(text=f_context["text"], reply_markup=reply_markup)


@inline_handler(return_state=0)
def four(update: Update, context: CallbackContext):
    f_context = function_handlers["commands"]['start']['handlers'][0][3]
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(inlinekeyboard_menu(f_context))
    query.edit_message_text(text=f_context["text"], reply_markup=reply_markup)


@inline_handler(return_state=0)
def start_over(update: Update, context: CallbackContext):
    f_context = function_handlers["commands"]['start']['handlers'][1][0]
    query = update.callback_query
    user = update.message.from_user
    logger.info("User %s started over the conversation.", user.first_name)
    reply_markup = InlineKeyboardMarkup(inlinekeyboard_menu(f_context))
    query.edit_message_text(text=f_context["text"], reply_markup=reply_markup)


@inline_handler(return_state=ConversationHandler.END)
def end(update: Update, context: CallbackContext):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    f_context = function_handlers["commands"]['start']['handlers'][1][1]
    query = update.callback_query
    query.edit_message_text(text=f_context["text"])


function_handlers = {"commands": {
    'start': {
        'start_handler': {
            "handler": start,
            "text": "Start handler, Choose a route",
            "keyboard": [
                {0: "1.1", 1: "2.2", },
            ]},
        'handlers': {
            0: {
                0: {"handler": one,
                    "text": "First CallbackQueryHandler, 00, Choose a route",
                    "keyboard": [
                        {2: "3.3", 3: "4.4", },
                    ]},
                1: {"handler": two,
                    "text": "Second CallbackQueryHandler, 01, Choose a route",
                    "keyboard": [
                        {0: "1.1", 2: "3.3", },
                    ]},
                2: {"handler": three,
                    "text": "Third CallbackQueryHandler. 02, Do want to start over?",
                    "keyboard": [
                        {0: "Yes, let's do it again!", 1: "Nah, I've had enough ...", },
                    ]},
                3: {"handler": four,
                    "text": "Fourth CallbackQueryHandler, 03, Choose a route",
                    "keyboard": [
                        {1: "2.2", 2: "3.3", },
                    ]},
            },
            1: {
                0: {"handler": start_over,
                    "text": "Start handler, ky5, Choose a route",
                    "keyboard": [
                        {0: "1.1", 1: "2.2", },
                    ]},
                1: {"handler": end, "text": "See you next time!", },
            },
        }}}}


def make_conversation(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: dict[dict, None] = {}) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/
        examples/inlinekeyboard2.py
    """

    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states={state_id: [
            CallbackQueryHandler(v["handler"], pattern='^' + str(k) + '$')
            for k, v in state_value.items()]
            for state_id, state_value in function_handlers.items()})


def main() -> None:
    """Run the bot."""

    if telegram_token is None:
        logger.warning("Telegram token not found in env.")
        return

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    command_name = 'start'
    handler_context = function_handlers["commands"][command_name]
    dispatcher.add_handler(make_conversation(
        command_name=command_name, command_handler=handler_context[
            'start_handler']["handler"],
        function_handlers=handler_context['handlers']))

    # Start the Bot
    updater.start_polling()


if __name__ == '__main__':
    main()
