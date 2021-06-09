#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

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
from uuid import uuid4

from typing import Dict, List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)


# TELEGRAM_TOKEN
telegram_token = os.getenv('TELEGRAM_TOKEN', default=None)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)
SEVEN = str(uuid4())


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
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def inline_handler(return_state):
    def my_decorator(func):
        def wrapper(update: Update, context: CallbackContext):
            query = update.callback_query
            query.answer()
            func(update, context)
            return return_state
        return wrapper
    return my_decorator


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return FIRST


def one(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            #
            InlineKeyboardButton("7", callback_data=SEVEN),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def two(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def three(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
            #
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def seven(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you 7to1 next time!")
    return FIRST


def five(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you 5 next time!")
    return ConversationHandler.END


@inline_handler(return_state=ConversationHandler.END)
def five_dec2(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text="See you 5.2 next time!")


def six(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    #query.edit_message_text(text="See you 6 next time!")
    return SECOND


def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def ky5_start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ky5 User %s started the conversation.", user.first_name)

    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).

    f_context = function_handlers["commands"]['ky5']['start_handler']

    keyboard = [
        [InlineKeyboardButton(v, callback_data=str(k)) for k, v in x.items()]
        for x in f_context["keyboard"]]

    keyboard2 = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(f_context["text"], reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


function_handlers = {"commands": {
    'ky5': {
        'start_handler': {
            "function": ky5_start,
            "text": "Start handler, Ky5 ,Choose a route",
            "keyboard": [
                {ONE: "text2_", },
                {ONE: "text2_", TWO: "text3_", },
                {ONE: "text22", TWO: "text33", THREE: "43", },
                {ONE: "text22", },
            ]},
        'handlers': {
            0: {
                0: {
                    "function": one,
                    "k": [
                        {TWO: "text2_", THREE: "text3_", },
                        {TWO: "text22", THREE: "text33", },
                    ]
                },
                1: {"function": two, },
                2: {"function": three, },
                3: {"function": four, },
            },
            1: {
                0: {"function": start_over, },
                1: {"function": end, },
            },
        }}}}


def make_conversation(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: List[Dict] = []) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/examples/inlinekeyboard2.py
    """

    def cbqh(k, v) -> CallbackQueryHandler:
        return CallbackQueryHandler(v["function"], pattern='^' + str(k) + '$')

    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states={
            i: [cbqh(k, v) for k, v in function_handlers[i].items()]
            for i in range(len(function_handlers))})


def make_conversation_dict_dict(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: Dict[Dict, None] = {}) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/examples/inlinekeyboard2.py
    """

    def cbqh(k, v) -> CallbackQueryHandler:
        return CallbackQueryHandler(v["function"], pattern='^' + str(k) + '$')

    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states={
            state_id: [cbqh(k, v) for k, v in state_value.items()]
            for state_id, state_value in function_handlers.items()})


def make_conversation_list_dict(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: List[Dict] = []) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/examples/inlinekeyboard2.py
    """

    def cbqh(k, v) -> CallbackQueryHandler:
        return CallbackQueryHandler(v, pattern='^' + str(k) + '$')

    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states={
            i: [cbqh(k, v) for k, v in function_handlers[i].items()]
            for i in range(len(function_handlers))})


def make_conversation_list_list(
        command_name: str = 'start', command_handler: object = None,
        function_handlers: List[List[object]] = []) -> ConversationHandler:
    """
    Make conversation for inline buttons.

    Info:
        https://github.com/python-telegram-bot/python-telegram-bot/examples/inlinekeyboard2.py
    """

    def cbqh(f: object, i: int) -> CallbackQueryHandler:
        return CallbackQueryHandler(f, pattern='^' + str(i) + '$')

    return ConversationHandler(
        entry_points=[CommandHandler(command_name, command_handler)],
        fallbacks=[CommandHandler(command_name, command_handler)],
        states={i: [
            cbqh(function_handlers[i][j], j)
            for j in range(len(function_handlers[i]))]
            for i in range(len(function_handlers))})


def make_conversation_00_old(command_name: str = 'start'):
    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    def cb_pattern(v: int) -> str:
        return '^' + str(v) + '$'

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(command_name, start)],
        fallbacks=[CommandHandler(command_name, start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern=cb_pattern(v=ONE)),
                CallbackQueryHandler(two, pattern=cb_pattern(v=TWO)),
                CallbackQueryHandler(three, pattern=cb_pattern(v=THREE)),
                CallbackQueryHandler(four, pattern=cb_pattern(v=FOUR)),
                #
                CallbackQueryHandler(seven, pattern=cb_pattern(v=SEVEN)),

            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern=cb_pattern(v=ONE)),
                CallbackQueryHandler(end, pattern=cb_pattern(v=TWO)),
            ],
        }
    )
    return conv_handler


def main() -> None:
    """Run the bot."""

    if telegram_token is None:
        logger.warning("Telegram token not found in env.")
        return

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(make_conversation_00_old(
        command_name='start'))
    dispatcher.add_handler(make_conversation_list_list(
        command_name='ky2', command_handler=start,
        function_handlers=[
            [one, two, three, four, five_dec2, six, ],
            [start_over, end, ],
        ]))
    dispatcher.add_handler(make_conversation_list_dict(
        command_name='ky3', command_handler=start,
        function_handlers=[
            {ONE: one, TWO: two, THREE: three, FOUR: four, },
            {ONE: start_over, TWO: end, },
        ]))

    dispatcher.add_handler(make_conversation_dict_dict(
        command_name='ky5', command_handler=function_handlers["commands"][
            'ky5']['start_handler']["function"],
        function_handlers=function_handlers["commands"][
            'ky5']['handlers']))

    # Start the Bot
    updater.start_polling()


if __name__ == '__main__':
    main()
