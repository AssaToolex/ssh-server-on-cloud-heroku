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
            {"Post Product": {"See Function in Word doc": None, }, },
            {"Post Full Catalog with pictures": {
                "A chat that is dedicated to full catalog 1 post = 1 product": None, }, },
            {"Post Contest": {
                "Post with Text and Vid / Pic": None, },
             "Post Lottery": None, },
            {"Post Winners": None, },
            {"Post Today’s Sale": {
                "Post with Text and Vid / Pic": None, },
             "Post Today’s Discount": None, },
            {"See Statistics": None, },
            {"Merchant Forum": {"See Function in Word doc": None, }, },
            {"Contact Management": {"See Function in Word doc": None, }, },
        ],
    }
]
handler_states = {}
inline_keyboards = {}
conversation_id = str(uuid4())
first_start_id = conversation_id  # Top level buttons
logger = logging.getLogger()


def start(update: Update, context: CallbackContext) -> str:
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")

    #
    # Top level buttons
    #

    # Ok # print(first_start_id)
    keyboard = [
        [InlineKeyboardButton(x[2], callback_data=x[1]) for x in bb]
        for bb in inline_keyboards[first_start_id]]  # Top level buttons
    update.message.reply_text(
        "Choose you level", reply_markup=InlineKeyboardMarkup(keyboard))

    return first_start_id  # Top level buttons


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text)


def main():

    logging.basicConfig(
        level=logging.INFO,  #
        # level=logging.DEBUG,  #
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    #echo_handler = MessageHandler(
    #    Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[CommandHandler('start', start)],
        states={k1: (
            CallbackQueryHandler(v2[0], pattern='^' + str(v2[1]) + '$')
            for v2 in v1) for k1, v1 in handler_states.items()},
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def empty_function(update: Update, context: CallbackContext) -> str:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    logger.info("Empty function.")
    return first_start_id  # Top level buttons


def gen_one_state(state=None):
    """Return: are_append, ((func_id, str_pattern, str_button), ). ???."""

    global conversation_id

    if state is None:
        return False, ((None, None, None), )
    elif isinstance(state, str):  # Str ""  # Button without handler
        return True, ((empty_function, str(uuid4()), state), )
    elif isinstance(state, int):  # Int ""  # Button without handler
        return True, ((empty_function, str(uuid4()), str(state)), )
    elif isinstance(state, list) or isinstance(state, tuple):  # List []
        # New state of conversations
        new_state = []
        new_keyboards = []
        for query_value in state:
            are_append, info_id = gen_one_state(state=query_value)
            if are_append is True:
                new_state.extend(info_id)
                new_keyboards.append(info_id)
        if len(new_state) > 0:
            handler_states[conversation_id] = new_state
            inline_keyboards[conversation_id] = new_keyboards
            conversation_id = str(uuid4())
        return False, ((None, None, None), )
    elif isinstance(state, dict):  # Dick {}
        # Append sates of conversations
        append_state = []
        for button_text, query_value in state.items():
            if callable(query_value):
                append_state.append((query_value, str(uuid4()), str(button_text), ))
            elif query_value is None:
                append_state.append((empty_function, str(uuid4()), str(button_text), ))
            else:
                append_state.append(("DictValue", str(uuid4()), str(button_text), ))
        return True, append_state
    return True, (("type not found", "!!!"+str(type(state)), "!!!", "type not found"), )


def generator_states():

    if False:
        top_zz = gen_one_state(
            state=[
                [
                    "sss",
                    {"Info 555": empty_function, "Info 777": None, "Info 888": None, },
                    3,
                ],
                [
                    "sss",
                    2,
                    {"sss": {1:2, }, },
                    1,
                    {"KY 555": None, "KY 777": None, "KY 888": None, },
                    None,

                ],
            ])
        import pprint
        pprint.pprint(handler_states)

    if False:
        top_zz = gen_one_state(
            state=keys_btn[0]['GROUPS / CHANNELS SIDE LOOK'])
        import pprint
        pprint.pprint(handler_states)

    if False:
        top_zz = gen_one_state(
            state=keys_btn[0]["BOT SIDE LOOK"])
        import pprint
        pprint.pprint(handler_states)

    if True:
        top_zz = gen_one_state(
            state=keys_btn[0]['MERCHANTS SIDE LOOK'])
        import pprint
        #pprint.pprint(handler_states)
        pprint.pprint(inline_keyboards)


if __name__ == '__main__':
    generator_states()
    main()
