from telegram import *
from telegram.ext import *
import telegram, telegram.ext, logging, datetime, html, uuid



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
u = Updater('TOKEN', use_context=True)

#setting vars
j = u.job_queue
items={}
users=[]
users = list(dict.fromkeys(users))


def start(update: Update, context:CallbackContext):
    if update.effective_chat.type!='private': 
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hey! I am alive :) PM me for any kind of help 😉")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'''🎉 All about <b>GiveawayBot</b> 🎉

<b>Hold giveaways quickly and easily!</b>

Hello! I'm <b>GiveawayBot</b>, and I'm here to make it as easy as possible to hold giveaways on your Telegram group/channel! I was created by <a href='tg://user?id=1383570275'>Aditya</a> <code>(1383570275)</code> using the <a href='https://github.com/python-telegram-bot/python-telegram-bot'>Python-telegram-bot</a> library (13.7) Check out my commands by typing /ghelp''', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
def ghelp(update: Update, context:CallbackContext):
    if update.effective_chat.type=='private': 
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'''Here's the commands that the bot supports: 
<b>!gstart {html.escape('<time>')} [winners]w [prize]</b> - starts a giveaway
<b>!gend [messageId]</b> - ends (picks a winner for) the specified or latest giveaway in the current channel
<b>!greroll [messageId]</b> - re-rolls the specified or latest giveaway in the current channel
<b>!glist</b> - lists active giveaways on the server
Do not include {html.escape('<>')} nor [] - {html.escape('<>')} means required and [] means optional.
''', parse_mode=ParseMode.HTML)
    else:
        keyboard=[[InlineKeyboardButton(text='Click here for help!', url='http://t.me/dctggiveawaybot?start=ghelp')]]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Contact me in PM to get the list of available commands.", reply_markup=InlineKeyboardMarkup(keyboard))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    choice = query.data
    if choice=='1':
        members=context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.callback_query.from_user.id)
        if members.status==telegram.ChatMemberAdministrator or telegram.ChatMemberOwner or telegram.ChatMemberMember or telegram.ChatMemberRestricted:
            users.append(update.callback_query.from_user.id)
            update.callback_query.answer(text='Prticipation successful!', show_alert=True)
        else:
            update.callback_query.answer(text='Join the group to participate', show_alert=True)
        print(members.status)


#giveaway start
def gstart(update: Update, context: CallbackContext):
    if update.effective_chat.type=='private':
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"💥 This command cannot be used in Private Messages!")
    else:
        user_says=' '.join(context.args)
        user_says=user_says.split(' ')
        keyboard=[[InlineKeyboardButton('🎉', callback_data='1')]]
        now=datetime.datetime.now()
        seconds=False
        minutes=False
        hours=False
        days=False
        chat_id=update.effective_chat.id
        uid=uuid.uuid4()
        try:
            tym=user_says[0]
            winners=user_says[1]
            items[uid] = {"id": chat_id, "item": user_says[2:]}
            item=str(items[uid]["item"])
            item=item.replace('[', '')
            item=item.replace(']', '')
            item=item.replace("'", '')

        except:
            context.bot.send_message(chat_id=chat_id, text=f'''💥 Please include a length of time, and a number of winners and a prize! Example usage: <code>/gstart 30m 5w Awesome T-Shirt</code>''', parse_mode=ParseMode.HTML)
        try:
            #winner
            if winners.endswith('w' or 'W'):
                winners=winners.split('w' or 'W')
                winners=int(winners[0])
            elif winners<1:
                context.bot.send_message(chat_id=chat_id, text=f'''Winners cannot be less than 1''', parse_mode=ParseMode.HTML)
        except:    
            context.bot.send_message(chat_id=chat_id, text=f'''💥 Failed to parse winners from <code>{winners}</code>
Example usage: <code>/gstart 30m 5w Awesome T-Shirt</code>''', parse_mode=ParseMode.HTML)
        try:
            #time
            if tym.endswith('s' or 'S'):
                seconds=True
                tym=tym.split('s' or 'S')
                added=now+datetime.timedelta(seconds=int(tym[0]))
                tym1=tym[0]
                tym=f'{tym[0]} Seconds'
            elif tym.endswith('m' or 'M'):
                minutes=True
                tym=tym.split('m' or 'M')
                added=now+datetime.timedelta(minutes=int(tym[0]))
                tym1=tym[0]
                tym=f'{tym[0]} Minutes'
            elif tym.endswith('h' or 'H'):
                hours=True
                tym=tym.split('h' or 'H')
                added=now+datetime.timedelta(hours=int(tym[0]))
                tym1=tym[0]
                tym=f'{tym[0]} Hours'
            elif tym.endswith('d' or 'D'):
                days=True
                tym=tym.split('d' or 'D')
                added=now+datetime.timedelta(days=int(tym[0]))
                tym1=tym[0]
                tym=f'{tym[0]} days'
        except:
            context.bot.send_message(chat_id=chat_id, text=f'''💥 Failed to parse time from <code>{tym}</code>
Example usage: <code>/gstart 30m 5w Awesome T-Shirt</code>''', parse_mode=ParseMode.HTML)
        try:
            if now.strftime('%d %m %Y')==added.strftime('%d %m %Y'):
                end=added.strftime('Today at %I:%M %p')
            else:
                end=added.strftime('%m/%d/%Y')
        
            context.bot.send_message(chat_id=chat_id, text=f'''🎉 GIVEAWAY 🎉
<b>{item}</b>
React with 🎉 to enter!
Ends: in {tym} ({added.strftime("%B %d, %Y %I:%M %p")})
Hosted by: @{update.effective_user.username}
{winners} Winner(s) | Ends at • {end}
Giveaway id: <code>{uid}</code>
        ''', parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
            tym1=int(tym1)
            if seconds==True:
                j.run_once(callback, tym1, context=uid)
            elif minutes==True:
                j.run_once(callback, tym1*60, context=uid)
            elif hours==True:
                j.run_once(callback, tym1*60*60, context=uid)
            elif days==True:
                j.run_once(callback, tym1*60*60*24, context=uid)
            else:
                pass
            print('successful')
        except Exception as e:
            print(f'unsuccesful {e}')

  
#giveaway end result
def callback(context: telegram.ext.CallbackContext):
    uid = context.job.context
    chat_id = items[uid]["id"]
    item=str(items[uid]["item"])
    item=item.replace('[', '')
    item=item.replace(']', '')
    item=item.replace("'", '')
    context.bot.send_message(chat_id=chat_id, text=f'Great you won {item}')
    del items[uid]

if __name__ == '__main__':
    dp = u.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ghelp', ghelp))
    dp.add_handler(CommandHandler('gstart', gstart))
    dp.add_handler(CallbackQueryHandler(button))
    u.start_polling()
    u.idle()
