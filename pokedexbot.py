import html
from pokebase.loaders import generation
from telegram.ext import *
from telegram import *
import botinfo
import pokebase as pb
import random
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# setting global vars

keyboard = [
    [
        InlineKeyboardButton("Data", callback_data='1'),
        InlineKeyboardButton("Randpoke", callback_data='2'),
        InlineKeyboardButton("Shiny", callback_data='3')
    ],
    [
        InlineKeyboardButton("Stats", callback_data='4'),
        InlineKeyboardButton("Move", callback_data='5'),
        InlineKeyboardButton("Coverage", callback_data='6')
    ]
]
reply_markup = InlineKeyboardMarkup(keyboard)
help_text = "Here's the commands that bot supports: "


def start(update, context):
    keyboard= [
    [InlineKeyboardButton("Add Pan to your group", url='http://t.me/Mr7PanBot?startgroup=true')],
    [InlineKeyboardButton("Support Group", url='https://t.me/bgmiofficial_1'),InlineKeyboardButton("Updates Channel", url='https://t.me/bgmiupdates')],
    [InlineKeyboardButton("Source code", url='https://github.com/aditya-yadav-27')],
    [InlineKeyboardButton("Help & commands", url='http://t.me/Mr7PanBot?start=help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.id)
    user = (update.message.from_user['first_name'])
    master = "<a href='https://t.me/aditya_yadav_27'>Aditya</a>"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('rotomdex.png', 'rb'),
                           caption=f"Hey {user}, I am The most advance pokedex bot of Telegram made by my master {master}\nType /help to see what I can do!!", reply_markup=reply_markup ,parse_mode=ParseMode.HTML)


def help(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s used help command", user.id)
    update.message.reply_text(
        text=help_text, reply_markup=reply_markup)


def button(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data='14'),

        ]
    ]
    reply_markup1 = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    choice = query.data

    if choice == '14':
        query.edit_message_text(
            text=help_text, reply_markup=reply_markup)
    elif choice == '1':
        query.edit_message_text(
            text=f"<code>/data {html.escape('<pokemon name or id>')}</code>: get data of the specified pokemon", reply_markup=reply_markup1, parse_mode=ParseMode.HTML)
    elif choice == '2':
        query.edit_message_text(
            text=f"<code>/randpoke</code>: get a random pokemon with its animated gif", reply_markup=reply_markup1, parse_mode=ParseMode.HTML)
    elif choice == '3':
        query.edit_message_text(
            text=f"<code>/shiny {html.escape('<pokemon name or id>')}</code>: get a shiny image of the specified pokemon", reply_markup=reply_markup1, parse_mode=ParseMode.HTML)
    elif choice == '4':
        query.edit_message_text(
            text=f"<code>/stats {html.escape('<pokemon name or id>')}</code>: get the stats of specified pokemon", reply_markup=reply_markup1, parse_mode=ParseMode.HTML)
    elif choice == '5':
        query.edit_message_text(
            text=f"<code>/move {html.escape('<move/pokemon name or id>')}</code>: get the details of the specified move or move that the specified pokemon can learn", reply_markup=reply_markup1, parse_mode=ParseMode.HTML)
    elif choice == '6':
        query.edit_message_text(
            text=f'Coming soon..', reply_markup=reply_markup1, parse_mode=ParseMode.HTML)


def data(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_says = ' '.join(context.args)
    logger.info(f"User %s used data command for pokemon {user_says}", user.id)
    try:
        msg = context.bot.send_message(
            chat_id=update.effective_chat.id, text="Fetching data...")
        p1 = pb.pokemon(user_says.casefold())
        abilities = ''
        types = ''
        for poketype in p1.types:
            types = ', '.join(poketype.type.name.capitalize()
                              for poketype in p1.types)
        for stat in p1.stats:
            result = ['{}: {}'.format(stat.stat.name.capitalize(), stat.base_stat)
                      for stat in p1.stats]
        for ability in p1.abilities:
            abilities = ', '.join(ability.ability.name.capitalize()
                                  for ability in p1.abilities)

        proper = user_says.split('-')
        proper1 = proper[0]
        bulba_link = f'https://bulbapedia.bulbagarden.net/wiki/{proper1.capitalize()}_(Pok%C3%A9mon)'
        bulba2 = f"<a href='{bulba_link}'>Bulbapedia</a>"
        caption = f'''<u><b>#{p1.id} {p1.name.capitalize()}</b></u>
        <b>Types</b>
        {types}

        <b>Abilities</b>
        {abilities}

        <b>Gender Ratio</b>                <b>Catch Rate</b>
        will add soon                      will add soon
                            <b>Breeding</b>
        <b>Egg groups</b>                  <b>Hatch Time</b>
        will add soon                      will add soon
               
        <b>Height/Weight</b>
        {p1.height/10}m/{p1.weight/10}kg

        <b>Base-exp</b>           <b>Base Freindship</b>
        {p1.base_experience}      will add soon

        <b>Evolution Line</b>
        will add soon 

        <b>Other Forms</b>
        will add soon

Read more about this pokemon on <b>{bulba2}</b>'''

        update.message.reply_document(
            f"https://img.pokemondb.net/artwork/{p1.name}.jpg", caption=caption, parse_mode=ParseMode.HTML)
        msg.delete()
    except Exception as e:
        update.message.reply_text(
            f"'{user_says}' is not a valid pokemon! try again")
        msg.delete()


def randpoke(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s used randpoke command", user.id)
    l = context.bot.send_message(
        chat_id=update.effective_chat.id, text='Selecting a random pokemon!...')
    k = random.randint(1, 898)
    p2 = pb.pokemon(k)
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=f"http://play.pokemonshowdown.com/sprites/xyani/{p2.name}.gif", caption=f"<b>{p2.name.capitalize()} | #{p2.id}</b>")
    l.delete()


def shiny(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_says = ' '.join(context.args)
    logger.info(f"User %s used shiny command for pokemon {user_says}", user.id)
    try:
        msg = context.bot.send_message(
            chat_id=update.effective_chat.id, text="Getting image...")
        p1 = pb.pokemon(user_says.casefold())
        update.message.reply_photo(
            f"https://img.pokemondb.net/sprites/home/shiny-2x/jpg/{user_says}.jpg", caption=f"<b>#{p1.id} | Shiny {p1.name.capitalize()}</b>")
        msg.delete()
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{user_says} is not a valid pokemon, try again!")
        msg.delete()


def stats(update: Update, context: CallbackContext):
    user_says = ' '.join(context.args)
    user = update.message.from_user
    logger.info(f"User %s used stats command for pokemon {user_says}", user.id)
    try:
        msg = context.bot.send_message(
            chat_id=update.effective_chat.id, text="Getting stats...")
        p1 = pb.pokemon(user_says.casefold())
        for stat in p1.stats:
            result = ['{}: {}'.format(stat.stat.name.capitalize(), stat.base_stat)
                      for stat in p1.stats]
        hp = result[0]
        attack = result[1]
        defense = result[2]
        sattack = result[3]
        sdefense = result[4]
        spd = result[5]
        thp = int(hp[4:8])
        tatk = int(attack[8:12])
        tdef = int(defense[9:13])
        tsat = int(sattack[16:20])
        tsdef = int(sdefense[17:21])
        tspd = int(spd[7:11])
        update.message.reply_text(f'''<b><u>#{p1.id} | {p1.name.capitalize()}</u></b>
            <code>{result[0]}
        {result[1]}
        {result[2]}
        {result[3]}
        {result[4]}
        {result[5]}</code>
        <b>Total: {thp+tatk+tdef+tsdef+tspd+tsat}</b>
            ''', parse_mode=ParseMode.HTML)
        msg.delete()
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'{user_says} is not a valid pokemon')
        msg.delete()


def move(update: Update, context: CallbackContext):
    user_says = ' '.join(context.args)
    user = update.message.from_user
    logger.info(
        f"User %s used move command for move/pokemon {user_says}", user.id)

    try:
        msg = context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Getting move details...')
        p1 = pb.move(user_says)
        generation = str(p1.generation).split('-')
        generation = generation[0].capitalize()+'-'+generation[1].upper()
        update.message.reply_text(f'''<b><u>{p1.id} | {str(p1.name.capitalize())} | {generation}</u></b>
        <b>Type</b>                               <b>Category</b>
        {str(p1.type.name).capitalize()}                             {str(p1.damage_class).capitalize()}

        <b>Power Points</b>                <b>Base Power</b>
        {p1.pp}                                      {p1.power}

        <b>Accuracy</b>                    <b>Target</b>
        {p1.accuracy}%                     {p1.target}

        <b>Contest</b>
        {str(p1.contest_type).capitalize()}
        ''', parse_mode=ParseMode.HTML)
        msg.delete()
    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'{user_says} is not a valid move try again {e}')
        msg.delete()


def main():
    updater = Updater(token=botinfo.token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('data', data))
    dispatcher.add_handler(CommandHandler('randpoke', randpoke))
    dispatcher.add_handler(CommandHandler('shiny', shiny))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('move', move))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
