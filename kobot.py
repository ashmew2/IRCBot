#Todo: 

from willie.module import commands
import willie.module

users=[]
helpmsg = 'Welcome to #KolibriOS. Ask KolibriOS|Yogev for more help! (Or use !cmd)'

@commands('sethelp')
def sethelp(bot, trigger):
    if not trigger.group(2):
        return

    if trigger.admin:
        global helpmsg
        bot.reply('Setting helpmsg to : ' + trigger.group(2))
        helpmsg = trigger.group(2);
    else:
        bot.reply('You do not have privileges for this command.')

@commands('help')
def help(bot, trigger):
    bot.reply(helpmsg)

@commands('logs')
def logs(bot, trigger):    
    bot.reply('Check out (temporary) logs at http://pastebin.com/18S9gwpX')

@commands('cmd')
def cmd(bot, trigger):
    bot.reply('Supported commands : !info !logs !wiki !help !cmd !sethelp')

@commands('info')
def info(bot, trigger):
    bot.reply('Visit the KolibriOS board at board.kolibrios.org')
    
@commands('wiki')
def wiki(bot, trigger):
    bot.reply('Visit KolibriOS wiki at http://wiki.kolibrios.org/')

#trigger.group contains the entire thing.
@willie.module.rule('.*')
def print_help(bot, trigger):
    if trigger.nick not in users:
          users.append(trigger.nick)
          if trigger.group()!='!help':
              bot.reply(helpmsg)
    
#GSoC related stuff comes later. Below this part.
@commands('addtask')
def addtask(bot, trigger):
    if trigger.admin:
        bot.say('As you wish.')
    else:
        bot.say('You dont have permissions sadly.')
