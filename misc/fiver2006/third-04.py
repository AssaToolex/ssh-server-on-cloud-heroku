#
#
#

import logging
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler,
    Filters, MessageHandler, Updater, )


telegram_token = '1746726955:AAHqpPxDse8bSrSQQHQNk0Q3LCH3-ItTias'

# list = top/bottom buttons
# dict = left/right buttons
keys_btn = [
    {
        "GROUPS / CHANNELS SIDE LOOK": [
            {"Contact Merchant": None, },
            {"Competition & Lottery": None, "Merchant Reviews": None, },
            {"Sales & Discounts of Merchant": None, },
            {"Settings": None, "Kivunimmerkaz Bot": None, },
            {"Contact Management": None, },
        ],
        "BOT SIDE LOOK": [
            {"Secondhand Merkaz": {"By Area": {
                "Group / Channel": None, }, }, },
            {"Search By Type or Niche": {"By Area": {
                "Type or Niche": None, }, }, },
            {"Daily Sales & Discounts": {"By Area": {
                "Sales & Discounts": None, }, }, },
            {"Competitions & Lottery": {"By Area": {
                "Competitions & Lottery": None, }, }, },
            {"Management": {
                "Management Menu": None, }, },
        ],
        "MERCHANTS SIDE LOOK": [
            {
                "Post Product": {"See Function in Word doc": None, }, },
            {
                "Post Full Catalog with pictures": {
                    "A chat that is dedicated to full catalog 1 post = 1 product": None, }, },
            {
                "Post Contest": {
                    "Post with Text and Vid / Pic": None, },
                "Post Lottery": None, },
            {
                "Post Winners": None, },
            {
                "Post Today’s Sale": {
                    "Post with Text and Vid / Pic": None, },
                "Post Today’s Discount": None, },
            {
                "See Statistics": None, },
            {
                "Merchant Forum": {"See Function in Word doc": None, }, },
            {
                "Contact Management": {"See Function in Word doc": None, }, },
        ],
    }
]

logger = logging.getLogger()
callbacks = {}


def match_callback(k, v):
    new_uuid = str(uuid4())  # random
    callbacks[new_uuid] = {"v": v, "k": k, }
    return str(new_uuid)


def start(update, context):
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")

    if False:

        # Stages
        FIRST, SECOND = range(2)
        # Callback data
        ONE, TWO, THREE, FOUR = range(4)

        # Build InlineKeyboard where each button has a displayed text
        # and a string as callback_data
        # The keyboard is a list of button rows, where each row is in turn
        # a list (hence `[[...]]`).
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data=str(ONE)),
                InlineKeyboardButton("2", callback_data=str(TWO)),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(
            "Start handler, Choose a route",
            reply_markup=reply_markup)

    #
    # Top level buttons
    #

    buttons_dict = keys_btn[0]
    keyboard = [
        [InlineKeyboardButton(k, callback_data=match_callback(k, v)), ]
        for k, v in buttons_dict.items()]
    update.message.reply_text(
        "Choose you level", reply_markup=InlineKeyboardMarkup(keyboard))


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text)


def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(
        Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


handler_states = {}


def empty_function():
    pass


def gen_one_state(state=None):
    """Return: are_append, func_id, str_pattern, str_button. ???."""
    if state is None:
        return False, None, None, None
    elif isinstance(state, str):  # Str ""  # Button without handler
        return True, "empty_function", str(uuid4()), str
    elif isinstance(state, int):  # Int ""  # Button without handler
        return True, "empty_function", str(uuid4()), str(str)
    elif isinstance(state, list) or isinstance(state, tuple):  # List []
        # New state of conversations
        new_state = []
        for query_value in state:
            are_append, func_id, str_pattern, str_button = gen_one_state(query_value)
            if are_append is True:
                new_state.append(
                    {"function": func_id, "key_pattern": str_pattern, "text_button": str(query_value), }
                )
        if len(new_state) > 0:
            conversation_id = str(uuid4())  # random
            handler_states[conversation_id] = new_state
        return False, None, None, None
    elif isinstance(state, dict):  # Dick {}
        s = ""
        for k, v in state.items():
            f = match_callback(k, v)
            s = s + ", " + k + ": {=->" + gen_one_state(v) + "<-=}"
        return "Dict"+s
    return True, "type not found", "!!!"+str(type(state)), "!!!", "type not found"


def gen_st():

    import pprint

    top_zz = gen_one_state(
          [
            [
                "sss",
                None,
                3,
            ],
            [
                "sss",
                2,
                "sss",
                1,
                None,
                None,

            ],
          ]

        )

    pprint.pprint(handler_states)

    # keyboard = [
    #        [InlineKeyboardButton(k, callback_data=match_callback(k, v)), ]
    #        for k, v in buttons_dict.items()]


if __name__ == '__main__':
    # main()
    gen_st()
